"""Shared pytest fixtures for cali-workout tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path


@pytest.fixture
def beep_path(tmp_path: Path) -> Path:
    """Return a temporary beep path."""
    return tmp_path / 'beep.wav'


@pytest.fixture(autouse=True)
def no_real_sound(monkeypatch: pytest.MonkeyPatch) -> Generator[None]:
    """Disable real sound playback during tests."""
    monkeypatch.setattr('cali.audio.play_sound', lambda *args, **kwargs: None)
    monkeypatch.setattr('cali.timer.play_sound', lambda *args, **kwargs: None)
    monkeypatch.setattr('cali.workout_app.play_sound', lambda *args, **kwargs: None)
    yield
