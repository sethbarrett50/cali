"""Terminal timer utilities."""

from __future__ import annotations

import os
import select
import sys
import time

from cali.audio import play_sound


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('clear')


def format_time(seconds: int) -> str:
    """Format seconds as MM:SS."""
    minutes, remaining_seconds = divmod(seconds, 60)
    return f'{minutes:02d}:{remaining_seconds:02d}'


def read_key_nonblocking() -> str | None:
    """Read one key from stdin if available."""
    ready, _, _ = select.select([sys.stdin], [], [], 0)

    if ready:
        return sys.stdin.read(1).lower()

    return None


def print_header() -> None:
    """Print the application header."""
    print('Morning Calisthenics Timer')
    print('=' * 32)


def countdown(label: str, seconds: int, notes: str = '') -> bool:
    """Run a countdown timer.

    Args:
        label: Timer display label.
        seconds: Number of seconds to count down.
        notes: Optional notes to display.

    Returns:
        True if completed or skipped.
        False if the user quits.
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
