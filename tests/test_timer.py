"""Tests for terminal timer helpers."""

from __future__ import annotations

import pytest

from cali.timer import countdown, format_time


@pytest.mark.unit
@pytest.mark.parametrize(
    ('seconds', 'expected'),
    [
        (0, '00:00'),
        (5, '00:05'),
        (65, '01:05'),
        (600, '10:00'),
    ],
)
def test_format_time(seconds: int, expected: str) -> None:
    """format_time should render MM:SS."""
    assert format_time(seconds) == expected


@pytest.mark.unit
def test_countdown_completes_without_keypress(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """countdown should complete when no key is pressed."""
    monkeypatch.setattr('cali.timer.clear_screen', lambda: None)
    monkeypatch.setattr('cali.timer.print_header', lambda: None)
    monkeypatch.setattr('cali.timer.read_key_nonblocking', lambda: None)
    monkeypatch.setattr('cali.timer.time.sleep', lambda seconds: None)

    assert countdown('Test', 1) is True


@pytest.mark.unit
def test_countdown_quits_on_q(monkeypatch: pytest.MonkeyPatch) -> None:
    """countdown should return False when q is pressed."""
    monkeypatch.setattr('cali.timer.clear_screen', lambda: None)
    monkeypatch.setattr('cali.timer.print_header', lambda: None)
    monkeypatch.setattr('cali.timer.read_key_nonblocking', lambda: 'q')
    monkeypatch.setattr('cali.timer.time.sleep', lambda seconds: None)

    assert countdown('Test', 30) is False


@pytest.mark.unit
def test_countdown_skips_on_s(monkeypatch: pytest.MonkeyPatch) -> None:
    """countdown should return True when s is pressed."""
    monkeypatch.setattr('cali.timer.clear_screen', lambda: None)
    monkeypatch.setattr('cali.timer.print_header', lambda: None)
    monkeypatch.setattr('cali.timer.read_key_nonblocking', lambda: 's')
    monkeypatch.setattr('cali.timer.time.sleep', lambda seconds: None)

    assert countdown('Test', 30) is True
