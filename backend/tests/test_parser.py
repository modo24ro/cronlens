import pytest

from cronlens.parser import CronSyntaxError, parse


def test_wildcards_expand_to_full_range():
    expr = parse("* * * * *")
    assert expr.minute.values == frozenset(range(60))
    assert expr.day_of_week.values == frozenset(range(7))
    assert all(field.is_wildcard for field in expr.fields)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("5", {5}),
        ("1-3", {1, 2, 3}),
        ("1,3,5", {1, 3, 5}),
        ("*/20", {0, 20, 40}),
        ("10-30/10", {10, 20, 30}),
        ("50/5", {50, 55}),
    ],
)
def test_minute_syntax(source, expected):
    assert parse(f"{source} * * * *").minute.values == frozenset(expected)


def test_names_are_case_insensitive():
    expr = parse("0 0 * jan-Mar mon,FRI")
    assert expr.month.values == frozenset({1, 2, 3})
    assert expr.day_of_week.values == frozenset({1, 5})


def test_sunday_seven_is_normalised_to_zero():
    assert parse("0 0 * * 7").day_of_week.values == frozenset({0})


def test_extra_whitespace_is_ignored():
    assert parse("  0   12 * * *  ").source == "0 12 * * *"


@pytest.mark.parametrize(
    ("source", "field"),
    [
        ("60 * * * *", "minute"),
        ("* 24 * * *", "hour"),
        ("* * 0 * *", "day_of_month"),
        ("* * * 13 *", "month"),
        ("* * * * 8", "day_of_week"),
        ("*/0 * * * *", "minute"),
        ("5-1 * * * *", "minute"),
        ("1,,2 * * * *", "minute"),
        ("x * * * *", "minute"),
    ],
)
def test_invalid_values_name_the_field(source, field):
    with pytest.raises(CronSyntaxError) as info:
        parse(source)
    assert info.value.field == field


@pytest.mark.parametrize("source", ["", "* * * *", "* * * * * *"])
def test_wrong_field_count(source):
    with pytest.raises(CronSyntaxError, match="expected 5 fields"):
        parse(source)
