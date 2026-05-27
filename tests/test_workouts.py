"""Tests for workout definitions."""

from __future__ import annotations

import pytest

from cali.workouts import COOLDOWN, WARMUP, WORKOUTS


@pytest.mark.unit
def test_all_weekdays_are_defined() -> None:
    """Workout definitions should cover every day of the week."""
    expected_days = {
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
    }

    assert set(WORKOUTS) == expected_days


@pytest.mark.unit
def test_workouts_are_non_empty() -> None:
    """Each workout should have at least one round and one exercise."""
    for day, workout in WORKOUTS.items():
        assert workout.rounds >= 1, day
        assert workout.exercises, day

        for exercise in workout.exercises:
            assert exercise.name.strip(), day
            assert exercise.duration_seconds > 0, exercise.name


@pytest.mark.unit
def test_warmup_and_cooldown_are_valid() -> None:
    """Warm-up and cooldown should contain valid timed exercises."""
    for workout in [WARMUP, COOLDOWN]:
        assert workout.rounds == 1
        assert workout.exercises

        for exercise in workout.exercises:
            assert exercise.name.strip()
            assert exercise.duration_seconds > 0
