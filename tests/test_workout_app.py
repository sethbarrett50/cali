"""Tests for workout application flow."""

from __future__ import annotations

import pytest

from cali.models import Exercise, Workout
from cali.workout_app import run_workout, show_today_plan


@pytest.mark.unit
def test_show_today_plan_prints_expected_content(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """show_today_plan should print the selected workout details."""
    workout = Workout(
        name='Test Workout',
        rounds=1,
        exercises=[Exercise('Test Exercise', 10, 'Do it carefully')],
    )

    monkeypatch.setattr('cali.workout_app.clear_screen', lambda: None)
    monkeypatch.setattr('cali.workout_app.has_mpv', lambda: True)

    show_today_plan('Monday', workout)

    captured = capsys.readouterr()
    assert 'Today:   Monday' in captured.out
    assert 'Workout: Test Workout' in captured.out
    assert 'Test Exercise' in captured.out
    assert 'Do it carefully' in captured.out


@pytest.mark.unit
def test_run_workout_completes(monkeypatch: pytest.MonkeyPatch) -> None:
    """run_workout should return True when all countdowns complete."""
    workout = Workout(
        name='Test Workout',
        rounds=1,
        exercises=[
            Exercise('Exercise 1', 1),
            Exercise('Exercise 2', 1),
        ],
        rest_between_exercises=1,
        rest_between_rounds=0,
    )

    countdown_calls: list[str] = []

    def fake_countdown(label: str, seconds: int, notes: str = '') -> bool:
        countdown_calls.append(label)
        return True

    monkeypatch.setattr('cali.workout_app.clear_screen', lambda: None)
    monkeypatch.setattr('cali.workout_app.print_header', lambda: None)
    monkeypatch.setattr('cali.workout_app.countdown', fake_countdown)

    assert run_workout(workout) is True
    assert len(countdown_calls) == 3
    assert 'Exercise 1' in countdown_calls[0]
    assert countdown_calls[1] == 'Rest'
    assert 'Exercise 2' in countdown_calls[2]


@pytest.mark.unit
def test_run_workout_returns_false_when_countdown_quits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """run_workout should return False if countdown returns False."""
    workout = Workout(
        name='Test Workout',
        rounds=1,
        exercises=[Exercise('Exercise 1', 1)],
    )

    monkeypatch.setattr('cali.workout_app.clear_screen', lambda: None)
    monkeypatch.setattr('cali.workout_app.print_header', lambda: None)
    monkeypatch.setattr('cali.workout_app.countdown', lambda *args, **kwargs: False)

    assert run_workout(workout) is False
