"""Tests for cali data models."""

from __future__ import annotations

import pytest

from cali.models import Exercise, Workout


@pytest.mark.unit
def test_exercise_defaults() -> None:
    """Exercise should default notes to an empty string."""
    exercise = Exercise(name='Squat', duration_seconds=45)

    assert exercise.name == 'Squat'
    assert exercise.duration_seconds == 45
    assert exercise.notes == ''


@pytest.mark.unit
def test_workout_defaults() -> None:
    """Workout should use expected default rest durations."""
    workout = Workout(
        name='Test Workout',
        rounds=1,
        exercises=[Exercise('Squat', 45)],
    )

    assert workout.name == 'Test Workout'
    assert workout.rounds == 1
    assert len(workout.exercises) == 1
    assert workout.rest_between_exercises == 30
    assert workout.rest_between_rounds == 75


@pytest.mark.unit
def test_models_are_frozen() -> None:
    """Models should be immutable after creation."""
    exercise = Exercise(name='Squat', duration_seconds=45)

    with pytest.raises(AttributeError):
        exercise.name = 'Push-up'  # type: ignore[misc]
