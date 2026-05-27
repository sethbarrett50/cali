"""Workout application flow."""

from __future__ import annotations

import datetime as dt
import termios
import tty

from typing import TYPE_CHECKING

from cali.audio import ensure_beep_file, has_mpv, play_sound
from cali.timer import clear_screen, countdown, format_time, print_header
from cali.workouts import COOLDOWN, WARMUP, WORKOUTS

if TYPE_CHECKING:
    from cali.models import Workout


def run_workout(workout: Workout) -> bool:
    """Run a workout.

    Args:
        workout: Workout to run.

    Returns:
        True if completed.
        False if the user quits.
    """
    clear_screen()
    print_header()
    print(f'\nStarting: {workout.name}')
    play_sound()

    for round_number in range(1, workout.rounds + 1):
        for exercise_index, exercise in enumerate(workout.exercises, start=1):
            label = (
                f'{workout.name} | '
                f'Round {round_number}/{workout.rounds} | '
                f'{exercise_index}/{len(workout.exercises)} | '
                f'{exercise.name}'
            )

            if not countdown(label, exercise.duration_seconds, exercise.notes):
                return False

            is_last_exercise = exercise_index == len(workout.exercises)

            if not is_last_exercise and workout.rest_between_exercises > 0:
                if not countdown('Rest', workout.rest_between_exercises):
                    return False

        is_last_round = round_number == workout.rounds

        if not is_last_round and workout.rest_between_rounds > 0:
            if not countdown('Longer rest between rounds', workout.rest_between_rounds):
                return False

    return True


def show_today_plan(today: str, workout: Workout) -> None:
    """Print today's workout plan."""
    clear_screen()
    print_header()
    print(f'\nToday:   {today}')
    print(f'Workout: {workout.name}')
    print('\nSound:   ~/beep.wav through mpv when available')

    if not has_mpv():
        print('Warning: mpv was not found. Install mpv for sound alerts.')

    print('\nPlan:')

    print('\nWarm-up:')
    for exercise in WARMUP.exercises:
        print(f'  - {exercise.name}: {format_time(exercise.duration_seconds)}')

    print(f'\nMain workout: {workout.rounds} round(s)')
    for exercise in workout.exercises:
        note = f' - {exercise.notes}' if exercise.notes else ''
        print(f'  - {exercise.name}: {format_time(exercise.duration_seconds)}{note}')

    print('\nCooldown:')
    for exercise in COOLDOWN.exercises:
        print(f'  - {exercise.name}: {format_time(exercise.duration_seconds)}')

    print('\nControls during timers:')
    print('  p = pause/resume')
    print('  s = skip')
    print('  q = quit')

    print('\nPress Enter to start...')


def run_app() -> int:
    """Run the workout application.

    Returns:
        Process exit code.
    """
    ensure_beep_file()

    today = dt.datetime.now().strftime('%A')
    workout = WORKOUTS[today]

    show_today_plan(today, workout)
    input()

    original_terminal_settings = termios.tcgetattr(0)

    try:
        tty.setcbreak(0)

        if not run_workout(WARMUP):
            clear_screen()
            print('Workout quit during warm-up.')
            return 1

        if not run_workout(workout):
            clear_screen()
            print('Workout quit.')
            return 1

        if not run_workout(COOLDOWN):
            clear_screen()
            print('Workout quit during cooldown.')
            return 1

        clear_screen()
        print_header()
        play_sound()
        print('\nWorkout complete. Nice work.')
        return 0

    finally:
        termios.tcsetattr(0, termios.TCSADRAIN, original_terminal_settings)
