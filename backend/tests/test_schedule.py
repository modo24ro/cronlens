from datetime import datetime

from cronlens.parser import parse
from cronlens.schedule import next_runs

START = datetime(2026, 1, 1, 0, 0)  # a Thursday


def test_every_fifteen_minutes():
    runs = next_runs(parse("*/15 * * * *"), START, 3)
    assert runs == [
        datetime(2026, 1, 1, 0, 15),
        datetime(2026, 1, 1, 0, 30),
        datetime(2026, 1, 1, 0, 45),
    ]


def test_runs_are_strictly_after_start():
    runs = next_runs(parse("0 0 * * *"), START, 1)
    assert runs == [datetime(2026, 1, 2, 0, 0)]


def test_weekdays_only():
    runs = next_runs(parse("0 9 * * MON-FRI"), START, 3)
    assert runs == [
        datetime(2026, 1, 1, 9, 0),  # Thu
        datetime(2026, 1, 2, 9, 0),  # Fri
        datetime(2026, 1, 5, 9, 0),  # Mon
    ]


def test_day_of_month_or_day_of_week():
    # Both restricted: runs on the 15th OR on Mondays.
    runs = next_runs(parse("0 0 15 * MON"), START, 3)
    assert runs == [
        datetime(2026, 1, 5),
        datetime(2026, 1, 12),
        datetime(2026, 1, 15),
    ]


def test_month_rollover_into_next_year():
    runs = next_runs(parse("0 0 1 1 *"), datetime(2026, 6, 1), 1)
    assert runs == [datetime(2027, 1, 1)]


def test_leap_day():
    runs = next_runs(parse("0 0 29 2 *"), START, 1)
    assert runs == [datetime(2028, 2, 29)]


def test_impossible_schedule_returns_empty():
    assert next_runs(parse("0 0 31 2 *"), START, 5) == []
