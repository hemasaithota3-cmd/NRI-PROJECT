"""
statistics.py
-------------
Data Science statistical calculations, powered by NumPy.

This module defines the `DataStatistics` class which takes a list of
numbers and can compute every statistic required by the Data Science
tab of the calculator: mean, median, mode, variance, standard
deviation, min, max, range, quartiles, IQR, sum, and count.

Keeping this in its own module (separate from the GUI and from the
basic Calculator class) mirrors how a real data-science toolkit is
organized: raw arithmetic vs. statistical/analytical functions.
"""

from collections import Counter

import numpy as np

from utils import CalculatorError, parse_number_list


class DataStatistics:
    """Computes descriptive statistics for a list of numeric values.

    Example:
        >>> stats = DataStatistics("10, 20, 30, 40, 50")
        >>> stats.mean()
        30.0
    """

    def __init__(self, raw_text):
        """Create a DataStatistics object from a raw comma/space separated string.

        Args:
            raw_text (str): e.g. "10,20,30,40,50"

        Raises:
            CalculatorError: if the input cannot be parsed into numbers.
        """
        numbers = parse_number_list(raw_text)
        self.data = np.array(numbers, dtype=float)

    # ------------------------------------------------------------------
    # Core statistics
    # ------------------------------------------------------------------
    def mean(self):
        """Return the arithmetic mean (average) of the data."""
        return float(np.mean(self.data))

    def median(self):
        """Return the median (middle value) of the data."""
        return float(np.median(self.data))

    def mode(self):
        """Return the most frequently occurring value(s).

        NumPy has no built-in mode function, so we use collections.Counter.
        If multiple values are tied for the highest frequency, all of
        them are returned as a comma-separated string.
        """
        counts = Counter(self.data.tolist())
        highest_freq = max(counts.values())
        modes = sorted([value for value, freq in counts.items() if freq == highest_freq])

        if len(modes) == len(self.data):
            # Every value appears equally often -> no meaningful mode
            return "No unique mode"

        return ", ".join(str(int(m) if float(m).is_integer() else m) for m in modes)

    def variance(self):
        """Return the (population) variance of the data."""
        return float(np.var(self.data))

    def std_dev(self):
        """Return the (population) standard deviation of the data."""
        return float(np.std(self.data))

    def minimum(self):
        """Return the smallest value in the data."""
        return float(np.min(self.data))

    def maximum(self):
        """Return the largest value in the data."""
        return float(np.max(self.data))

    def data_range(self):
        """Return the range (max - min) of the data."""
        return float(np.max(self.data) - np.min(self.data))

    def quartiles(self):
        """Return a tuple (Q1, Q2, Q3) - the 25th, 50th and 75th percentiles."""
        q1 = float(np.percentile(self.data, 25))
        q2 = float(np.percentile(self.data, 50))
        q3 = float(np.percentile(self.data, 75))
        return q1, q2, q3

    def iqr(self):
        """Return the Interquartile Range (Q3 - Q1)."""
        q1, _, q3 = self.quartiles()
        return q3 - q1

    def sum(self):
        """Return the sum of all values."""
        return float(np.sum(self.data))

    def count(self):
        """Return the number of values in the data."""
        return int(self.data.size)

    def summary(self):
        """Return a dictionary containing every statistic at once.

        Useful for the GUI to display an "all stats" report in a
        single call instead of calling each method individually.
        """
        if self.count() < 1:
            raise CalculatorError("Cannot compute statistics on an empty dataset.")

        q1, q2, q3 = self.quartiles()
        return {
            "Count": self.count(),
            "Sum": self.sum(),
            "Mean": self.mean(),
            "Median": self.median(),
            "Mode": self.mode(),
            "Variance": self.variance(),
            "Std Dev": self.std_dev(),
            "Minimum": self.minimum(),
            "Maximum": self.maximum(),
            "Range": self.data_range(),
            "Q1 (25%)": q1,
            "Q2 (50%)": q2,
            "Q3 (75%)": q3,
            "IQR": self.iqr(),
        }
