"""Data models for cali-workout."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Exercise:
    """A timed workout movement."""

    name: str
    duration_seconds: int
    notes: str = ''


@dataclass(frozen=True)
class Workout:
    """A workout containing one or more rounds of exercises."""

    name: str
    rounds: int
    exercises: list[Exercise]
    rest_between_exercises: int = 30
    rest_between_rounds: int = 75
