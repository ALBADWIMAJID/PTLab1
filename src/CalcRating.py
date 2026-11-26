from .Types import DataType, RatingType


class CalcRating:
    def __init__(self, data: DataType) -> None:
        self.data = data

    def calc(self) -> RatingType:
        ratings: RatingType = {}
        for student, grades in self.data.items():
            if not grades:
                raise ValueError(f"{student} has no grades")

            total = sum(score for _, score in grades)
            ratings[student] = total / len(grades)

        return ratings
