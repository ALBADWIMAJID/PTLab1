from statistics import quantiles

from .Types import RatingType


class SecondQuartile:
    def __init__(self, ratings: RatingType) -> None:
        self.ratings = ratings

    def calc(self) -> RatingType:
        """Select ratings in (Q1, Q2] using inclusive quantiles."""
        if len(self.ratings) < 2:
            return {}

        q1, q2, _ = quantiles(
            self.ratings.values(),
            n=4,
            method="inclusive",
        )

        return {
            student: rating
            for student, rating in self.ratings.items()
            if q1 < rating <= q2
        }
