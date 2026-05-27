"""Audio helpers for cali-workout."""

from __future__ import annotations

import math
import shutil
import struct
import subprocess
import wave

from pathlib import Path

DEFAULT_BEEP_PATH = Path.home() / 'beep.wav'


def ensure_beep_file(
    path: Path = DEFAULT_BEEP_PATH,
    *,
    sample_rate: int = 44_100,
    duration_seconds: float = 0.25,
    frequency_hz: float = 880.0,
    amplitude: float = 0.4,
) -> Path:
    """Create a beep WAV file if it does not already exist.

    Args:
        path: Output path for the WAV file.
        sample_rate: WAV sample rate.
        duration_seconds: Length of the sound.
        frequency_hz: Tone frequency.
        amplitude: Tone amplitude from 0.0 to 1.0.

    Returns:
        Path to the existing or newly created WAV file.
    """
    if path.exists():
        return path

    path.parent.mkdir(parents=True, exist_ok=True)

    with wave.open(str(path), 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        total_samples = int(sample_rate * duration_seconds)

        for index in range(total_samples):
            sample = int(32767 * amplitude * math.sin(2 * math.pi * frequency_hz * index / sample_rate))
            wav_file.writeframes(struct.pack('<h', sample))

    return path


def has_mpv() -> bool:
    """Return whether mpv is available on PATH."""
    return shutil.which('mpv') is not None


def play_sound(path: Path = DEFAULT_BEEP_PATH) -> None:
    """Play a sound file with mpv.

    The sound is launched with Popen so timers do not block. If mpv is missing
    or the sound file cannot be played, the function falls back to a terminal
    bell, which may be silent in some terminals.
    """
    if path.exists() and has_mpv():
        try:
            subprocess.Popen(
                [
                    'mpv',
                    '--no-video',
                    '--really-quiet',
                    str(path),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        except OSError:
            pass

    print('\a', end='', flush=True)
