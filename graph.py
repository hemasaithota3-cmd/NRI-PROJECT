"""
graph.py
--------
Graphing feature for the Data Science Smart Calculator.

Lets the user type an expression such as:
    y = x^2
    y = sin(x) + 2
    y = x**3 - 3*x

and renders the plot inside the Tkinter window using
matplotlib's FigureCanvasTkAgg backend.

Only a restricted, whitelisted set of names is passed into `eval`
(no builtins) so arbitrary/unsafe code cannot be executed - this
keeps the "type your own formula" feature safe for a classroom app.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")  # safe default backend; GUI code swaps this at runtime if needed
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from utils import CalculatorError

# Names that are allowed to be used inside a user-typed expression.
_SAFE_NAMES = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "sqrt": np.sqrt, "log": np.log10, "ln": np.log,
    "abs": np.abs, "pi": np.pi, "e": np.e, "exp": np.exp,
}


def _normalize_expression(expression):
    """Convert a user-friendly expression into valid Python/NumPy syntax.

    - Strips a leading "y=" or "y =" if present.
    - Replaces the caret '^' (common exponent notation) with Python's '**'.

    Args:
        expression (str): raw text typed by the user, e.g. "y = x^2".

    Returns:
        str: a normalized expression string, e.g. "x**2".
    """
    expr = expression.strip()
    if expr.lower().startswith("y"):
        # Strip a leading "y" and optional "="
        expr = expr[1:].lstrip()
        if expr.startswith("="):
            expr = expr[1:].lstrip()
    expr = expr.replace("^", "**")
    return expr


class GraphPlotter:
    """Builds a matplotlib Figure for a given y = f(x) expression."""

    def build_figure(self, expression, x_min=-10, x_max=10, num_points=400):
        """Create and return a matplotlib Figure plotting y = f(x).

        Args:
            expression (str): e.g. "y = x^2" or "sin(x)".
            x_min (float): lower bound of the x range.
            x_max (float): upper bound of the x range.
            num_points (int): how many sample points to plot.

        Raises:
            CalculatorError: if the expression is invalid or unsafe.

        Returns:
            matplotlib.figure.Figure: ready to embed in Tkinter.
        """
        if x_min >= x_max:
            raise CalculatorError("Minimum x must be less than maximum x.")

        expr = _normalize_expression(expression)
        if expr == "":
            raise CalculatorError("Please enter an expression, e.g. y = x^2")

        x = np.linspace(x_min, x_max, num_points)
        local_scope = dict(_SAFE_NAMES)
        local_scope["x"] = x

        try:
            # No builtins are exposed -> only whitelisted math functions and x are usable
            y = eval(expr, {"__builtins__": {}}, local_scope)
        except ZeroDivisionError:
            raise CalculatorError("Expression caused a division by zero.")
        except Exception as exc:  # noqa: BLE001 - surfaced as a friendly message
            raise CalculatorError(f"Invalid expression: {exc}")

        y = np.asarray(y, dtype=float)
        if y.shape != x.shape:
            # e.g. a constant expression like "5" -> broadcast to a flat line
            y = np.full_like(x, fill_value=float(np.atleast_1d(y)[0]))

        figure = Figure(figsize=(5.5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(x, y, linewidth=2, color="#2C7BE5")
        ax.axhline(0, color="gray", linewidth=0.8)
        ax.axvline(0, color="gray", linewidth=0.8)
        ax.set_title(f"y = {expr}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True, linestyle="--", alpha=0.4)
        figure.tight_layout()
        return figure

    def build_scatter_figure(self, x_values, y_values):
        """Create a scatter plot Figure for two raw lists of numbers.

        Used when the user wants to plot explicit x and y value lists
        instead of typing a formula.

        Args:
            x_values (list[float]): the x coordinates.
            y_values (list[float]): the y coordinates (same length as x).

        Raises:
            CalculatorError: if the lists are empty or mismatched in length.

        Returns:
            matplotlib.figure.Figure
        """
        if not x_values or not y_values:
            raise CalculatorError("Both X and Y value lists must be non-empty.")
        if len(x_values) != len(y_values):
            raise CalculatorError("X and Y value lists must be the same length.")

        figure = Figure(figsize=(5.5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.scatter(x_values, y_values, color="#2C7BE5")
        ax.plot(x_values, y_values, linestyle="--", alpha=0.5, color="#2C7BE5")
        ax.set_title("Scatter Plot of Provided Values")
        ax.set_xlabel("X values")
        ax.set_ylabel("Y values")
        ax.grid(True, linestyle="--", alpha=0.4)
        figure.tight_layout()
        return figure
