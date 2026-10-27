"""Turn a parsed cron expression into a short English sentence."""

from __future__ import annotations

from cronlens.parser import CronExpression, CronField

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]  # fmt: skip
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def _join(items: list[str]) -> str:
    if len(items) <= 2:
        return " and ".join(items)
    return ", ".join(items[:-1]) + f" and {items[-1]}"


def _compress(values: list[int]) -> list[tuple[int, int]]:
    """Group sorted values into consecutive runs: [1,2,3,5] -> [(1,3),(5,5)]."""
    runs: list[tuple[int, int]] = []
    for value in values:
        if runs and value == runs[-1][1] + 1:
            runs[-1] = (runs[-1][0], value)
        else:
            runs.append((value, value))
    return runs


def _list(field: CronField, label=str) -> str:
    parts = []
    for start, end in _compress(sorted(field.values)):
        if start == end:
            parts.append(label(start))
        elif end == start + 1:
            parts.extend([label(start), label(end)])
        else:
            parts.append(f"{label(start)} through {label(end)}")
    return _join(parts)


def _time_phrase(expr: CronExpression) -> str:
    minute, hour = expr.minute, expr.hour
    if len(minute.values) == 1 and len(hour.values) == 1:
        return f"At {next(iter(hour.values)):02d}:{next(iter(minute.values)):02d}"
    if minute.is_wildcard:
        minute_text = "Every minute"
    elif minute.source.startswith("*/"):
        minute_text = f"Every {minute.source[2:]} minutes"
    else:
        minute_text = f"At minute {_list(minute)}"
    if hour.is_wildcard:
        return minute_text
    return f"{minute_text} past hour {_list(hour)}"


def describe(expr: CronExpression) -> str:
    sentence = _time_phrase(expr)
    day_parts = []
    if not expr.day_of_month.is_wildcard:
        day_parts.append(f"on day-of-month {_list(expr.day_of_month)}")
    if not expr.day_of_week.is_wildcard:
        day_parts.append(f"on {_list(expr.day_of_week, lambda d: WEEKDAYS[d])}")
    if day_parts:
        sentence += ", " + " or ".join(day_parts)
    if not expr.month.is_wildcard:
        sentence += f", in {_list(expr.month, lambda m: MONTHS[m - 1])}"
    return sentence + "."
