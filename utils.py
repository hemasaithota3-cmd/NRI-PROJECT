"""
utils.py
--------
Utility/helper functions shared across the Data Science Smart Calculator.

This module intentionally contains NO GUI code. It only contains:
    * Input validation helpers
    * Number / list parsing helpers
    * A small ThemeManager class that remembers the user's last
      selected theme between runs (saved as a small JSON file).

Keeping these helpers in one place makes the rest of the codebase
(cleaner, more testable, and reusable) and follows the DRY principle.
"""

import json
import os

# Path used to persist the user's last chosen theme
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", "config.json")


class CalculatorError(Exception):
    """Base exception for all calculator related errors.

    Using a custom exception lets the GUI layer catch a single,
    predictable error type and show a friendly message box instead
    of crashing on raw Python exceptions (ZeroDivisionError,
    ValueError, etc.).
    """
    pass


def is_number(text):
    """Return True if `text` can be converted to a float.

    Args:
        text (str): the text to check.

    Returns:
        bool: True if convertible to float, False otherwise.
    """
    if text is None:
        return False
    text = str(text).strip()
    if text == "":
        return False
    try:
        float(text)
        return True
    except ValueError:
        return False


def parse_number_list(text):
    """Parse a comma / space separated string of numbers into a list of floats.

    Example:
        "10,20,30, 40 50" -> [10.0, 20.0, 30.0, 40.0, 50.0]

    Args:
        text (str): raw text entered by the user.

    Raises:
        CalculatorError: if the text is empty or contains no valid numbers.

    Returns:
        list[float]: the parsed numbers.
    """
    if text is None or str(text).strip() == "":
        raise CalculatorError("Please enter at least one numeric value.")

    # Allow both comma and whitespace as separators
    raw_parts = text.replace(",", " ").split()
    numbers = []
    for part in raw_parts:
        if not is_number(part):
            raise CalculatorError(f"'{part}' is not a valid number.")
        numbers.append(float(part))

    if len(numbers) == 0:
        raise CalculatorError("No valid numbers were found in the input.")

    return numbers


def format_result(value):
    """Format a numeric result for display.

    Removes unnecessary trailing zeros for floats that are effectively
    whole numbers (e.g. 20.0 -> "20") while keeping useful precision
    for non-whole numbers (rounded to 6 decimal places).

    Args:
        value (float | int): the value to format.

    Returns:
        str: a nicely formatted string representation.
    """
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int,)):
        return str(value)
    try:
        if float(value).is_integer():
            return str(int(value))
        return f"{round(float(value), 6)}"
    except (TypeError, ValueError, OverflowError):
        return str(value)


class ThemeManager:
    """Handles saving and loading the user's preferred theme to disk.

    ttkbootstrap ships several named themes (e.g. 'darkly', 'flatly',
    'cosmo', 'superhero'). This class persists the chosen theme name
    to a small JSON config file inside the assets/ folder so the
    calculator remembers the user's preference the next time it runs.
    """

    DEFAULT_THEME = "flatly"

    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

    def load_theme(self):
        """Load the last saved theme name, or the default if none exists."""
        if not os.path.exists(self.config_path):
            return self.DEFAULT_THEME
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("theme", self.DEFAULT_THEME)
        except (json.JSONDecodeError, OSError):
            return self.DEFAULT_THEME

    def save_theme(self, theme_name):
        """Save the given theme name to the config file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"theme": theme_name}, f)
        except OSError:
            # Non-fatal: the app can keep running even if saving fails
            pass
