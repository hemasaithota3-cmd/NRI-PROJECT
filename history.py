"""
history.py
----------
Manages the calculation history for the Data Science Smart Calculator.

Every calculation performed anywhere in the app (basic, scientific,
or data-science tab) is recorded as a HistoryManager entry so the
user can review, save, or export their session.
"""

import csv
import os
from datetime import datetime


class HistoryManager:
    """Stores, saves, and exports a running log of calculations.

    Each entry is stored as a tuple: (timestamp, expression, result).
    """

    def __init__(self, csv_path="history.csv"):
        self.csv_path = csv_path
        self.entries = []  # list of (timestamp, expression, result)

    def add_entry(self, expression, result):
        """Record a new calculation.

        Args:
            expression (str): e.g. "12 + 5" or "Mean(10,20,30)"
            result (str | float): the computed result.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.entries.append((timestamp, str(expression), str(result)))

    def clear(self):
        """Remove all stored history entries."""
        self.entries = []

    def get_display_lines(self):
        """Return a list of human-readable strings for display in the GUI.

        Example: "[14:03:21] 12 + 5 = 17"
        """
        return [f"[{ts}] {expr} = {result}" for ts, expr, result in self.entries]

    def save_to_file(self, path=None):
        """Save the full history as a plain text file.

        Args:
            path (str, optional): destination path. Defaults to history.txt
                                   next to the CSV path.
        """
        path = path or os.path.splitext(self.csv_path)[0] + ".txt"
        with open(path, "w", encoding="utf-8") as f:
            for line in self.get_display_lines():
                f.write(line + "\n")
        return path

    def export_csv(self, path=None):
        """Export the history as a CSV file with Timestamp, Expression, Result columns.

        Args:
            path (str, optional): destination path. Defaults to self.csv_path.
        """
        path = path or self.csv_path
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Expression", "Result"])
            for row in self.entries:
                writer.writerow(row)
        return path
