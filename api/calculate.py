# calculate.py
from typing import Iterable, List
import math


class Calculator:
    """Calculator class that computes sum, product, and mean."""

    def __init__(self, numbers: Iterable[float]):
        self.numbers = self._validate_numbers(numbers)

    @staticmethod
    def _validate_numbers(numbers: Iterable[float]) -> List[float]:
        try:
            vals = [float(x) for x in numbers]
        except Exception as e:
            raise ValueError(f"All items in 'numbers' must be numeric. Error: {e}")

        if not vals:
            raise ValueError("The 'numbers' list cannot be empty.")

        if any(not math.isfinite(v) for v in vals):
            raise ValueError("Numbers must all be finite (no NaN/inf).")

        return vals

    def total(self) -> float:
        """Return the sum of numbers."""
        return sum(self.numbers)

    def product(self) -> float:
        """Return the product of numbers."""
        prod = 1.0
        for v in self.numbers:
            prod *= v
        return prod

    def mean(self) -> float:
        """Return the mean of numbers."""
        return self.total() / len(self.numbers)

    def summary(self) -> dict:
        """Return all stats in a dictionary."""
        return {
            "numbers": self.numbers,
            "sum": self.total(),
            "product": self.product(),
            "mean": self.mean(),
        }
