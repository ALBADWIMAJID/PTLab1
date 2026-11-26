import pytest

from src.CalcRating import CalcRating
from src.SecondQuartile import SecondQuartile


@pytest.mark.parametrize(
    "ratings, expected",
    [
        ({}, {}),
        ({"A": 80.0}, {}),
        ({"A": 60.0, "B": 90.0}, {}),
        (
            {"A": 50.0, "B": 60.0, "C": 70.0, "D": 80.0},
            {"B": 60.0},
        ),
        (
            {"A": 50.0, "B": 60.0, "C": 70.0,
             "D": 80.0, "E": 90.0},
            {"C": 70.0},
        ),
        (
            {"A": 50.0, "B": 60.0, "C": 70.0,
             "D": 70.0, "E": 80.0, "F": 90.0},
            {"C": 70.0, "D": 70.0},
        ),
        (
            {"A": 80.0, "B": 80.0, "C": 80.0, "D": 80.0},
            {},
        ),
        (
            {"D": 80.0, "B": 60.0, "A": 50.0, "C": 70.0},
            {"B": 60.0},
        ),
        (
            {"A": 50.5, "B": 60.5, "C": 70.5, "D": 80.5},
            {"B": 60.5},
        ),
    ],
    ids=[
        "empty",
        "single-student",
        "two-students",
        "even-count",
        "exclude-q1-include-q2",
        "include-all-tied-students",
        "all-equal",
        "unsorted-input",
        "fractional-ratings",
    ],
)
def test_second_quartile(ratings, expected):
    original = ratings.copy()

    assert SecondQuartile(ratings).calc() == expected
    assert ratings == original


def test_second_quartile_uses_calculated_ratings():
    data = {
        "A": [("math", 40), ("physics", 60)],
        "B": [("math", 50), ("physics", 70)],
        "C": [("math", 60), ("physics", 80)],
        "D": [("math", 70), ("physics", 90)],
    }

    ratings = CalcRating(data).calc()

    assert SecondQuartile(ratings).calc() == {"B": 60.0}
