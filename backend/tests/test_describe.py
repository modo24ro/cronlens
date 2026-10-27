import pytest

from cronlens.describe import describe
from cronlens.parser import parse


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("* * * * *", "Every minute."),
        ("*/15 * * * *", "Every 15 minutes."),
        ("0 9 * * 1-5", "At 09:00, on Monday through Friday."),
        ("30 2 1 * *", "At 02:30, on day-of-month 1."),
        ("0 0 1 1,7 *", "At 00:00, on day-of-month 1, in January and July."),
        ("0 8-17 * * *", "At minute 0 past hour 8 through 17."),
        ("0 0 15 * SUN", "At 00:00, on day-of-month 15 or on Sunday."),
    ],
)
def test_describe(source, expected):
    assert describe(parse(source)) == expected
