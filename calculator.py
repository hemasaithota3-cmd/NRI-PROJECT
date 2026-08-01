"""
calculator.py
-------------
Core arithmetic and scientific calculator engine.

This module purposefully has NO Tkinter/GUI imports. It is a pure
"business logic" layer, which makes it easy to unit test and reuse
(e.g. in a CLI tool or a web backend) independently of the GUI.

Classes:
    Calculator: performs basic arithmetic, scientific functions, and
                provides simple memory (M+, M-, MR, MC) support.
"""

import math
from utils import CalculatorError


class Calculator:
    """Performs basic and scientific calculator operations.

    All public methods validate their inputs and raise a
    `CalculatorError` with a friendly message on invalid operations
    (e.g. division by zero, square root of a negative number).
    """

    def __init__(self):
        # Memory register used by M+, M-, MR, MC
        self._memory = 0.0

    # ------------------------------------------------------------------
    # Basic arithmetic
    # ------------------------------------------------------------------
    def add(self, a, b):
        """Return a + b."""
        return a + b

    def subtract(self, a, b):
        """Return a - b."""
        return a - b

    def multiply(self, a, b):
        """Return a * b."""
        return a * b

    def divide(self, a, b):
        """Return a / b. Raises CalculatorError on division by zero."""
        if b == 0:
            raise CalculatorError("Cannot divide by zero.")
        return a / b

    def percentage(self, a, b):
        """Return a as a percentage of b i.e. (a * b) / 100.

        This mirrors the common physical-calculator behaviour where
        pressing '%' after `a` and `b` computes a percent of b.
        """
        return (a * b) / 100

    def power(self, a, b):
        """Return a raised to the power b (a ** b)."""
        try:
            return math.pow(a, b)
        except (ValueError, OverflowError) as exc:
            raise CalculatorError(f"Invalid power operation: {exc}") from exc

    def square(self, a):
        """Return a squared (a ** 2)."""
        return a * a

    def square_root(self, a):
        """Return the square root of a. Raises CalculatorError if a < 0."""
        if a < 0:
            raise CalculatorError("Cannot take the square root of a negative number.")
        return math.sqrt(a)

    def cube(self, a):
        """Return a cubed (a ** 3)."""
        return a ** 3

    def cube_root(self, a):
        """Return the cube root of a (supports negative numbers)."""
        if a < 0:
            return -((-a) ** (1 / 3))
        return a ** (1 / 3)

    def modulus(self, a, b):
        """Return a % b. Raises CalculatorError if b == 0."""
        if b == 0:
            raise CalculatorError("Cannot perform modulus by zero.")
        return a % b

    # ------------------------------------------------------------------
    # Scientific functions
    # ------------------------------------------------------------------
    def sin(self, a, degrees=True):
        """Return sin(a). `a` is treated as degrees by default."""
        value = math.radians(a) if degrees else a
        return math.sin(value)

    def cos(self, a, degrees=True):
        """Return cos(a). `a` is treated as degrees by default."""
        value = math.radians(a) if degrees else a
        return math.cos(value)

    def tan(self, a, degrees=True):
        """Return tan(a). `a` is treated as degrees by default."""
        value = math.radians(a) if degrees else a
        return math.tan(value)

    def log(self, a):
        """Return log base 10 of a. Raises CalculatorError if a <= 0."""
        if a <= 0:
            raise CalculatorError("Logarithm is undefined for values <= 0.")
        return math.log10(a)

    def ln(self, a):
        """Return the natural logarithm (base e) of a."""
        if a <= 0:
            raise CalculatorError("Natural log is undefined for values <= 0.")
        return math.log(a)

    def factorial(self, a):
        """Return a! (factorial). Requires a non-negative integer."""
        if a < 0 or not float(a).is_integer():
            raise CalculatorError("Factorial requires a non-negative integer.")
        return math.factorial(int(a))

    def pi(self):
        """Return the mathematical constant pi."""
        return math.pi

    def e(self):
        """Return the mathematical constant e."""
        return math.e

    def absolute(self, a):
        """Return the absolute value of a."""
        return abs(a)

    # ------------------------------------------------------------------
    # Memory functions: M+, M-, MR, MC
    # ------------------------------------------------------------------
    def memory_add(self, value):
        """Add `value` to the memory register (M+)."""
        self._memory += value
        return self._memory

    def memory_subtract(self, value):
        """Subtract `value` from the memory register (M-)."""
        self._memory -= value
        return self._memory

    def memory_recall(self):
        """Return the current memory value (MR)."""
        return self._memory

    def memory_clear(self):
        """Reset the memory register to zero (MC)."""
        self._memory = 0.0
        return self._memory
