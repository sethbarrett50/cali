"""Tests for audio helpers."""

from __future__ import annotations

import wave

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from cali.audio import ensure_beep_file, has_mpv, play_sound

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.unit
def test_ensure_beep_file_creates_valid_wav(beep_path: Path) -> None:
    """ensure_beep_file should create a valid WAV file."""
    result = ensure_beep_file(beep_path)

    assert result == beep_path
    assert beep_path.exists()
    assert beep_path.stat().st_size > 0

    with wave.open(str(beep_path), 'rb') as wav_file:
        assert wav_file.getnchannels() == 1
        assert wav_file.getsampwidth() == 2
        assert wav_file.getframerate() == 44_100
        assert wav_file.getnframes() > 0


@pytest.mark.unit
def test_ensure_beep_file_does_not_overwrite_existing_file(beep_path: Path) -> None:
    """ensure_beep_file should preserve an existing file."""
    beep_path.write_bytes(b'existing')

    result = ensure_beep_file(beep_path)

    assert result == beep_path
    assert beep_path.read_bytes() == b'existing'


@pytest.mark.unit
def test_has_mpv_true(monkeypatch: pytest.MonkeyPatch) -> None:
    """has_mpv should return True when mpv exists."""
    monkeypatch.setattr('cali.audio.shutil.which', lambda command: '/usr/bin/mpv')

    assert has_mpv() is True


@pytest.mark.unit
def test_has_mpv_false(monkeypatch: pytest.MonkeyPatch) -> None:
    """has_mpv should return False when mpv is missing."""
    monkeypatch.setattr('cali.audio.shutil.which', lambda command: None)

    assert has_mpv() is False


@pytest.mark.unit
def test_play_sound_uses_mpv_when_available(
    beep_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """play_sound should call mpv when the file exists and mpv is available."""
    beep_path.write_bytes(b'fake-wav')

    popen_mock = Mock()
    monkeypatch.setattr('cali.audio.has_mpv', lambda: True)
    monkeypatch.setattr('cali.audio.subprocess.Popen', popen_mock)

    play_sound(beep_path)

    popen_mock.assert_called_once()
    args = popen_mock.call_args.args[0]

    assert args[0] == 'mpv'
    assert '--no-video' in args
    assert str(beep_path) in args


@pytest.mark.unit
def test_play_sound_falls_back_to_terminal_bell(
    beep_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """play_sound should print a terminal bell when mpv cannot be used."""
    monkeypatch.setattr('cali.audio.has_mpv', lambda: False)

    play_sound(beep_path)

    captured = capsys.readouterr()
    assert '\a' in captured.out
