import pytest

from src.CalcRating import CalcRating


def test_calc_returns_arithmetic_means():
    data = {
        "Иванов Иван Иванович": [
            ("математика", 80),
            ("программирование", 90),
            ("литература", 76),
        ],
        "Петров Петр Петрович": [
            ("математика", 100),
            ("социология", 90),
            ("химия", 61),
        ],
    }

    assert CalcRating(data).calc() == pytest.approx(
        {
            "Иванов Иван Иванович": 82.0,
            "Петров Петр Петрович": 83.66666666666667,
        }
    )


def test_calc_empty_data():
    assert CalcRating({}).calc() == {}


def test_calc_rejects_student_without_grades():
    with pytest.raises(ValueError, match="Иванов Иван"):
        CalcRating({"Иванов Иван": []}).calc()
