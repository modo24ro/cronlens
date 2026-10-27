"""Parser for standard 5-field cron expressions (minute hour day-of-month month day-of-week).

Supported syntax per field: ``*``, single values, ranges (``1-5``), lists (``1,3,5``),
steps (``*/15``, ``10-50/10``) and English month/weekday names (``JAN``, ``MON``).
Macros (``@daily``), Quartz extensions (``L``, ``W``, ``#``, ``?``) and seconds are not
supported yet; see ROADMAP.md.
"""

from __future__ import annotations

from dataclasses import dataclass

MONTH_NAMES = {
    name: index
    for index, name in enumerate(
        ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
        start=1,
    )
}
WEEKDAY_NAMES = {
    name: index for index, name in enumerate(["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"])
}


class CronSyntaxError(ValueError):
    """Raised when an expression cannot be parsed. ``field`` names the offending field."""

    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__(message)
        self.field = field


@dataclass(frozen=True)
class FieldSpec:
    name: str
    minimum: int
    maximum: int
    aliases: dict[str, int]


FIELD_SPECS: tuple[FieldSpec, ...] = (
    FieldSpec("minute", 0, 59, {}),
    FieldSpec("hour", 0, 23, {}),
    FieldSpec("day_of_month", 1, 31, {}),
    FieldSpec("month", 1, 12, MONTH_NAMES),
    # 7 is accepted as an alias for Sunday and normalised to 0.
    FieldSpec("day_of_week", 0, 7, WEEKDAY_NAMES),
)


@dataclass(frozen=True)
class CronField:
    name: str
    source: str
    values: frozenset[int]
    is_wildcard: bool

    def __contains__(self, value: int) -> bool:
        return value in self.values


@dataclass(frozen=True)
class CronExpression:
    source: str
    minute: CronField
    hour: CronField
    day_of_month: CronField
    month: CronField
    day_of_week: CronField

    @property
    def fields(self) -> tuple[CronField, ...]:
        return (self.minute, self.hour, self.day_of_month, self.month, self.day_of_week)


def _parse_value(token: str, spec: FieldSpec) -> int:
    upper = token.upper()
    if upper in spec.aliases:
        return spec.aliases[upper]
    if not token.isdigit():
        raise CronSyntaxError(f"invalid value {token!r} in {spec.name}", spec.name)
    value = int(token)
    if not spec.minimum <= value <= spec.maximum:
        raise CronSyntaxError(
            f"{spec.name} value {value} is outside {spec.minimum}-{spec.maximum}", spec.name
        )
    return value


def _parse_part(part: str, spec: FieldSpec) -> set[int]:
    base, slash, step_text = part.partition("/")
    step = 1
    if slash:
        if not step_text.isdigit() or int(step_text) == 0:
            raise CronSyntaxError(f"invalid step {step_text!r} in {spec.name}", spec.name)
        step = int(step_text)

    if base == "*":
        start, end = spec.minimum, spec.maximum
    elif "-" in base:
        start_text, _, end_text = base.partition("-")
        start, end = _parse_value(start_text, spec), _parse_value(end_text, spec)
        if start > end:
            raise CronSyntaxError(f"range {base!r} in {spec.name} is reversed", spec.name)
    else:
        start = _parse_value(base, spec)
        # "5/10" means "from 5 to the maximum, every 10", as in Vixie cron.
        end = spec.maximum if slash else start

    return set(range(start, end + 1, step))


def _parse_field(text: str, spec: FieldSpec) -> CronField:
    if not text:
        raise CronSyntaxError(f"empty {spec.name} field", spec.name)
    values: set[int] = set()
    for part in text.split(","):
        if not part:
            raise CronSyntaxError(f"empty list item in {spec.name}", spec.name)
        values |= _parse_part(part, spec)
    if spec.name == "day_of_week" and 7 in values:
        values.discard(7)
        values.add(0)
    return CronField(spec.name, text, frozenset(values), is_wildcard=text == "*")


def parse(expression: str) -> CronExpression:
    """Parse a 5-field cron expression or raise :class:`CronSyntaxError`."""
    parts = expression.split()
    if len(parts) != len(FIELD_SPECS):
        raise CronSyntaxError(f"expected 5 fields, got {len(parts)}")
    fields = [_parse_field(text, spec) for text, spec in zip(parts, FIELD_SPECS, strict=True)]
    return CronExpression(" ".join(parts), *fields)
