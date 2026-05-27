"""Tests for the command-line interface."""

from __future__ import annotations

from argparse import ArgumentParser
from typing import TYPE_CHECKING

import pytest

from cali.cli import build_parser, main

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.unit
def test_build_parser_returns_argument_parser() -> None:
    """build_parser should return an ArgumentParser."""
    parser = build_parser()

    assert isinstance(parser, ArgumentParser)
    assert parser.prog == 'cali-workout'


@pytest.mark.unit
def test_generate_beep_flag(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI should generate beep and exit when --generate-beep is passed."""
    fake_beep = tmp_path / 'beep.wav'

    monkeypatch.setattr('sys.argv', ['cali-workout', '--generate-beep'])
    monkeypatch.setattr('cali.cli.ensure_beep_file', lambda: fake_beep)

    exit_code = main()

    captured = capsys.readouterr()
    assert exit_code == 0
    assert str(fake_beep) in captured.out


@pytest.mark.integration
def test_main_runs_app_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """CLI should run the app when no special flags are passed."""
    monkeypatch.setattr('sys.argv', ['cali-workout'])
    monkeypatch.setattr('cali.cli.run_app', lambda: 0)

    assert main() == 0
