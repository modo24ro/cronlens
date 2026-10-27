"""Compute upcoming run times for a parsed cron expression."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timedelta

from cronlens.parser import CronExpression

# Give up after this many years without a match (e.g. "0 0 31 2 *" never fires).
SEARCH_LIMIT_YEARS = 5


def _day_matches(expr: CronExpression, moment: datetime) -> bool:
    # Python: Monday=0; cron: Sunday=0.
    cron_weekday = (moment.weekday() + 1) % 7
    dom_ok = moment.day in expr.day_of_month
    dow_ok = cron_weekday in expr.day_of_week
    # Standard cron quirk: when both day fields are restricted, either one may match.
    if not expr.day_of_month.is_wildcard and not expr.day_of_week.is_wildcard:
        return dom_ok or dow_ok
    return dom_ok and dow_ok


def iter_runs(expr: CronExpression, after: datetime) -> Iterator[datetime]:
    """Yield run times strictly after ``after``. Datetimes are naive and treated as wall time."""
    moment = after.replace(second=0, microsecond=0) + timedelta(minutes=1)
    limit = after.replace(tzinfo=None) + timedelta(days=366 * SEARCH_LIMIT_YEARS)
    while moment.replace(tzinfo=None) <= limit:
        if moment.month not in expr.month:
            year = moment.year + (moment.month == 12)
            month = moment.month % 12 + 1
            moment = moment.replace(year=year, month=month, day=1, hour=0, minute=0)
            continue
        if not _day_matches(expr, moment):
            moment = (moment + timedelta(days=1)).replace(hour=0, minute=0)
            continue
        if moment.hour not in expr.hour:
            moment = (moment + timedelta(hours=1)).replace(minute=0)
            continue
        if moment.minute not in expr.minute:
            moment += timedelta(minutes=1)
            continue
        yield moment
        moment += timedelta(minutes=1)


def next_runs(expr: CronExpression, after: datetime, count: int) -> list[datetime]:
    runs: list[datetime] = []
    for run in iter_runs(expr, after):
        runs.append(run)
        if len(runs) >= count:
            break
    return runs
