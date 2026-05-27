"""Command-line interface for cali-workout."""

from __future__ import annotations

import argparse

from cali import __version__
from cali.audio import ensure_beep_file
from cali.workout_app import run_app


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        prog='cali-workout',
        description='Run a terminal-based calisthenics workout timer.',
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'cali-workout {__version__}',
    )

    parser.add_argument(
        '--generate-beep',
        action='store_true',
        help='Generate ~/beep.wav and exit.',
    )

    return parser


def main() -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.generate_beep:
        path = ensure_beep_file()
        print(f'Generated or found beep file: {path}')
        return 0

    return run_app()
