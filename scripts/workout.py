#!/usr/bin/env python3
"""
Morning calisthenics workout timer.

Dependency-free except for optional mpv sound playback.

Expected sound file:
    ~/beep.wav

Controls during timers:
    p = pause/resume
    s = skip current exercise/rest
    q = quit
"""

from __future__ import annotations

import datetime as dt
import os
import select
import subprocess
import sys
import termios
import time
import tty

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Exercise:
    name: str
    duration_seconds: int
    notes: str = ''


@dataclass(frozen=True)
class Workout:
    name: str
    rounds: int
    exercises: list[Exercise]
    rest_between_exercises: int = 30
    rest_between_rounds: int = 75


WARMUP = Workout(
    name='Warm-up',
    rounds=1,
    rest_between_exercises=5,
    rest_between_rounds=0,
    exercises=[
        Exercise('March in place', 30),
        Exercise('Arm circles', 30),
        Exercise('Hip circles', 30),
        Exercise('Bodyweight good mornings', 30),
        Exercise('Knee circles / ankle rolls', 30),
        Exercise('Step jacks or jumping jacks', 30),
        Exercise('Shoulder taps from knees or wall', 30),
        Exercise('Easy squats', 30),
        Exercise('Light lunges', 30),
        Exercise('Deep breathing', 30),
    ],
)


COOLDOWN = Workout(
    name='Cooldown',
    rounds=1,
    rest_between_exercises=5,
    rest_between_rounds=0,
    exercises=[
        Exercise('Hamstring stretch', 30),
        Exercise('Quad stretch', 30),
        Exercise('Chest / shoulder stretch', 30),
        Exercise("Child's pose", 30),
        Exercise('Deep breathing', 30),
    ],
)


WORKOUTS: dict[str, Workout] = {
    'Monday': Workout(
        name='Full Body Strength C',
        rounds=3,
        exercises=[
            Exercise('Reverse lunges', 45, '6 reps per leg'),
            Exercise('Incline push-ups', 45, '10 reps'),
            Exercise('Wall sit', 30, '20-30 seconds'),
            Exercise('Glute bridges', 45, '15 reps'),
            Exercise('Plank', 30, '20-30 seconds'),
        ],
    ),
    'Tuesday': Workout(
        name='Mobility + Core',
        rounds=3,
        exercises=[
            Exercise('Cat-cow', 40, '10 reps'),
            Exercise('Bird dogs', 45, '8 per side'),
            Exercise('Side plank from knees - left', 20),
            Exercise('Side plank from knees - right', 20),
            Exercise('Reverse lunges', 45, '6 per leg'),
            Exercise('Slow mountain climbers', 45, '10 per side'),
        ],
        rest_between_exercises=25,
        rest_between_rounds=60,
    ),
    'Wednesday': Workout(
        name='Full Body Strength B',
        rounds=3,
        exercises=[
            Exercise('Sit-to-stand squats', 45, '10 reps'),
            Exercise('Incline push-ups', 45, '8-10 reps'),
            Exercise('Step-ups', 50, '8 per leg'),
            Exercise('Supermans', 40, '10 reps'),
            Exercise('Hollow hold or dead bug hold', 30, '15-20 seconds'),
        ],
    ),
    'Thursday': Workout(
        name='Conditioning Day',
        rounds=5,
        exercises=[
            Exercise('Step jacks or jumping jacks', 30),
            Exercise('Bodyweight squats', 30),
            Exercise('Slow mountain climbers', 30),
        ],
        rest_between_exercises=30,
        rest_between_rounds=30,
    ),
    'Friday': Workout(
        name='Full Body Strength A',
        rounds=3,
        exercises=[
            Exercise('Squats', 45, '10 reps'),
            Exercise('Incline push-ups', 45, '8 reps'),
            Exercise('Glute bridges', 45, '12 reps'),
            Exercise('Dead bugs', 45, '8 per side'),
            Exercise('Plank', 25, '20 seconds'),
        ],
    ),
    'Saturday': Workout(
        name='Longer Easy Session',
        rounds=1,
        exercises=[
            Exercise('Easy walk', 600, '10 minutes minimum; 20-40 preferred'),
            Exercise('Squats', 45, '2 sets of 10 reps'),
            Exercise('Incline push-ups', 45, '2 sets of 8 reps'),
            Exercise('Plank', 25, '2 sets of 20 seconds'),
            Exercise('Stretch', 300, '5 minutes'),
        ],
        rest_between_exercises=30,
        rest_between_rounds=0,
    ),
    'Sunday': Workout(
        name='Recovery / Reset',
        rounds=1,
        exercises=[
            Exercise('Easy walk', 600, '10-20 minutes'),
            Exercise('Light stretching', 300),
        ],
        rest_between_exercises=30,
        rest_between_rounds=0,
    ),
}


def clear_screen() -> None:
    os.system('clear')


def play_sound() -> None:
    """
    Play ~/beep.wav with mpv.

    Uses Popen so the timer does not block or freeze.
    Falls back to terminal bell if mpv or beep.wav is unavailable.
    """
    sound_file = Path.home() / 'beep.wav'

    if sound_file.exists():
        try:
            subprocess.Popen(
                [
                    'mpv',
                    '--no-video',
                    '--really-quiet',
                    str(sound_file),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        except FileNotFoundError:
            pass
        except OSError:
            pass

    print('\a', end='', flush=True)


def format_time(seconds: int) -> str:
    minutes, secs = divmod(seconds, 60)
    return f'{minutes:02d}:{secs:02d}'


def read_key_nonblocking() -> str | None:
    ready, _, _ = select.select([sys.stdin], [], [], 0)
    if ready:
        return sys.stdin.read(1).lower()
    return None


def print_header() -> None:
    print('Morning Calisthenics Timer')
    print('=' * 32)


def countdown(label: str, seconds: int, notes: str = '') -> bool:
    """
    Run a countdown.

    Returns:
        True if completed or skipped.
        False if user quit.
    """
    remaining = seconds
    paused = False

    play_sound()

    while remaining > 0:
        clear_screen()
        print_header()
        print(f'\nCurrent: {label}')

        if notes:
            print(f'Notes:   {notes}')

        print(f'Time:    {format_time(remaining)}')
        print('\nControls: [p] pause/resume  [s] skip  [q] quit')

        if paused:
            print('\nPAUSED')

        key = read_key_nonblocking()

        if key == 'q':
            return False

        if key == 's':
            clear_screen()
            print_header()
            print(f'\nSkipped: {label}')
            play_sound()
            time.sleep(0.5)
            return True

        if key == 'p':
            paused = not paused
            time.sleep(0.25)
            continue

        if paused:
            time.sleep(0.2)
            continue

        time.sleep(1)
        remaining -= 1

    clear_screen()
    print_header()
    print(f'\nComplete: {label}')
    play_sound()
    time.sleep(0.75)
    return True


def run_workout(workout: Workout) -> bool:
    clear_screen()
    print_header()
    print(f'\nStarting: {workout.name}')
    play_sound()
    time.sleep(1)

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
    clear_screen()
    print_header()
    print(f'\nToday:   {today}')
    print(f'Workout: {workout.name}')
    print('\nSound:   ~/beep.wav through mpv')
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


def main() -> None:
    today = dt.datetime.now().strftime('%A')
    workout = WORKOUTS[today]

    show_today_plan(today, workout)
    input()

    original_terminal_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())

        if not run_workout(WARMUP):
            clear_screen()
            print('Workout quit during warm-up.')
            return

        if not run_workout(workout):
            clear_screen()
            print('Workout quit.')
            return

        if not run_workout(COOLDOWN):
            clear_screen()
            print('Workout quit during cooldown.')
            return

        clear_screen()
        print_header()
        play_sound()
        print('\nWorkout complete. Nice work.')

    finally:
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            original_terminal_settings,
        )


if __name__ == '__main__':
    main()
