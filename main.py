"""
main.py
-------
Entry point and GUI layer for the "Data Science Smart Calculator".

Project flow
============
1. `main()` creates a splash screen (SplashScreen) while the app "loads".
2. Once the splash closes, the main window (CalculatorApp) is built:
       - A menu bar (File / Edit / View / Help)
       - A top display showing the current expression/result
       - A tabbed Notebook with 4 tabs: Basic, Scientific, Data Science, Graph
       - A History panel (its own tab) showing every past calculation
       - A status bar at the bottom (clock, ready message, active theme)
3. Every button click ultimately calls into `calculator.py`,
   `statistics.py`, or `graph.py` to perform the real computation,
   then records the result in `history.py` and updates the display.
4. Keyboard shortcuts mirror the on-screen buttons (numbers, +-*/,
   Enter = "=", Escape = clear, Backspace = delete last character).

This file is intentionally the only file that imports Tkinter /
ttkbootstrap - all other modules are GUI-agnostic business logic.
"""

import csv
import time
import tkinter as tk
from tkinter import messagebox, filedialog

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from calculator import Calculator
from statistics import DataStatistics
from graph import GraphPlotter
from history import HistoryManager
from utils import CalculatorError, is_number, format_result, ThemeManager

APP_TITLE = "Data Science Smart Calculator"

# Named themes offered in the View menu / theme selector.
# ttkbootstrap ships these as built-in bootstyle themes.
THEMES = {
    "Light": "flatly",
    "Dark": "darkly",
    "Blue": "cosmo",
    "Green": "minty",
}


# ==========================================================================
# Splash Screen
# ==========================================================================
class SplashScreen(tb.Window):
    """A brief animated splash/loading screen shown before the main app opens.

    This is its own small Tk root window (borderless) that is fully
    destroyed once loading finishes; `main()` then creates the real
    CalculatorApp root window.
    """

    def __init__(self, on_finish):
        super().__init__(themename="darkly")
        self.on_finish = on_finish
        self.overrideredirect(True)  # borderless window
        width, height = 420, 240
        self.geometry(self._center(width, height))
        self.configure(bg="#1F2937")

        tb.Label(
            self, text="📊", font=("Segoe UI Emoji", 40),
            background="#1F2937", foreground="white"
        ).pack(pady=(30, 5))

        tb.Label(
            self, text=APP_TITLE, font=("Segoe UI", 16, "bold"),
            background="#1F2937", foreground="white"
        ).pack()

        tb.Label(
            self, text="Loading your workspace...", font=("Segoe UI", 10),
            background="#1F2937", foreground="#9CA3AF"
        ).pack(pady=(2, 15))

        self.progress = tb.Progressbar(
            self, mode="determinate", bootstyle="success-striped", length=300
        )
        self.progress.pack(pady=10)

        self.after(50, self._animate, 0)

    def _center(self, width, height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        return f"{width}x{height}+{x}+{y}"

    def _animate(self, value):
        """Simple fake-loading animation from 0 -> 100%."""
        if value <= 100:
            self.progress["value"] = value
            self.after(12, self._animate, value + 4)
        else:
            self.destroy()
            self.on_finish()


# ==========================================================================
# Main Application
# ==========================================================================
class CalculatorApp(tb.Window):
    """The main application window for the Data Science Smart Calculator."""

    def __init__(self):
        self.theme_manager = ThemeManager()
        saved_theme = self.theme_manager.load_theme()
        super().__init__(title=APP_TITLE, themename=saved_theme, size=(980, 680))
        self.minsize(880, 620)

        # ---- business-logic objects ----
        self.calc = Calculator()
        self.history = HistoryManager(csv_path="history.csv")
        self.plotter = GraphPlotter()

        # ---- state ----
        self.current_theme_name = self._theme_display_name(saved_theme)
        self.expression = ""       # the running expression string (Basic/Sci tabs)
        self.just_evaluated = False

        self._build_menu()
        self._build_display()
        self._build_notebook()
        self._build_status_bar()
        self._bind_keyboard()

        self._tick_clock()
        self.set_status("Calculator Ready")

    # ------------------------------------------------------------------
    # Menu bar
    # ------------------------------------------------------------------
    def _build_menu(self):
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.clear_display, accelerator="Esc")
        file_menu.add_command(label="Save History", command=self.save_history)
        file_menu.add_command(label="Export History to CSV", command=self.export_history_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Copy Result", command=self.copy_result)
        edit_menu.add_command(label="Paste", command=self.paste_into_display)
        edit_menu.add_command(label="Clear", command=self.clear_display)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Dark Mode", command=lambda: self.apply_theme("Dark"))
        view_menu.add_command(label="Light Mode", command=lambda: self.apply_theme("Light"))
        view_menu.add_command(label="Blue Theme", command=lambda: self.apply_theme("Blue"))
        view_menu.add_command(label="Green Theme", command=lambda: self.apply_theme("Green"))
        menubar.add_cascade(label="View", menu=view_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    # ------------------------------------------------------------------
    # Top display
    # ------------------------------------------------------------------
    def _build_display(self):
        display_frame = tb.Frame(self, padding=15)
        display_frame.pack(fill=X)

        tb.Label(
            display_frame, text=APP_TITLE, font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        ).pack(anchor=W)

        self.display_var = tk.StringVar(value="0")
        self.display_entry = tb.Entry(
            display_frame, textvariable=self.display_var, font=("Consolas", 26),
            justify=RIGHT, bootstyle="primary"
        )
        self.display_entry.pack(fill=X, pady=(10, 0), ipady=10)

    # ------------------------------------------------------------------
    # Notebook (tabs)
    # ------------------------------------------------------------------
    def _build_notebook(self):
        self.notebook = tb.Notebook(self, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES, padx=15, pady=10)

        self.basic_tab = tb.Frame(self.notebook, padding=10)
        self.sci_tab = tb.Frame(self.notebook, padding=10)
        self.ds_tab = tb.Frame(self.notebook, padding=10)
        self.graph_tab = tb.Frame(self.notebook, padding=10)
        self.history_tab = tb.Frame(self.notebook, padding=10)

        self.notebook.add(self.basic_tab, text="🧮 Basic")
        self.notebook.add(self.sci_tab, text="🔬 Scientific")
        self.notebook.add(self.ds_tab, text="📊 Data Science")
        self.notebook.add(self.graph_tab, text="📈 Graph")
        self.notebook.add(self.history_tab, text="🕘 History")

        self._build_basic_tab()
        self._build_scientific_tab()
        self._build_data_science_tab()
        self._build_graph_tab()
        self._build_history_tab()

    # ---------------- Basic tab ----------------
    def _build_basic_tab(self):
        # Memory row
        mem_row = tb.Frame(self.basic_tab)
        mem_row.pack(fill=X, pady=(0, 8))
        for label, cmd, style in [
            ("MC", self.memory_clear, "secondary"),
            ("MR", self.memory_recall, "secondary"),
            ("M+", self.memory_add, "secondary"),
            ("M-", self.memory_subtract, "secondary"),
            ("Copy", self.copy_result, "info"),
        ]:
            tb.Button(mem_row, text=label, bootstyle=style, command=cmd, width=6).pack(
                side=LEFT, padx=3
            )

        grid = tb.Frame(self.basic_tab)
        grid.pack(fill=BOTH, expand=YES)

        buttons = [
            ("C", "secondary", self.clear_display), ("⌫", "secondary", self.backspace),
            ("%", "warning", lambda: self.press_op("%")), ("÷", "warning", lambda: self.press_op("/")),

            ("7", "light", lambda: self.press_digit("7")), ("8", "light", lambda: self.press_digit("8")),
            ("9", "light", lambda: self.press_digit("9")), ("×", "warning", lambda: self.press_op("*")),

            ("4", "light", lambda: self.press_digit("4")), ("5", "light", lambda: self.press_digit("5")),
            ("6", "light", lambda: self.press_digit("6")), ("−", "warning", lambda: self.press_op("-")),

            ("1", "light", lambda: self.press_digit("1")), ("2", "light", lambda: self.press_digit("2")),
            ("3", "light", lambda: self.press_digit("3")), ("+", "warning", lambda: self.press_op("+")),

            ("x²", "info", lambda: self.press_unary("square")), ("√x", "info", lambda: self.press_unary("square_root")),
            ("x³", "info", lambda: self.press_unary("cube")), ("∛x", "info", lambda: self.press_unary("cube_root")),

            ("xʸ", "info", lambda: self.press_op("**")), ("Mod", "info", lambda: self.press_op("%%")),
            ("0", "light", lambda: self.press_digit("0")), (".", "light", lambda: self.press_digit(".")),
        ]

        for i in range(6):
            grid.rowconfigure(i, weight=1)
        for j in range(4):
            grid.columnconfigure(j, weight=1)

        for idx, (text, style, cmd) in enumerate(buttons):
            r, c = divmod(idx, 4)
            tb.Button(grid, text=text, bootstyle=style, command=cmd).grid(
                row=r, column=c, sticky=NSEW, padx=4, pady=4, ipady=10
            )

        equals_row = tb.Frame(self.basic_tab)
        equals_row.pack(fill=X, pady=(8, 0))
        tb.Button(
            equals_row, text="=  Calculate", bootstyle="success", command=self.evaluate_expression
        ).pack(fill=X, ipady=10)

    # ---------------- Scientific tab ----------------
    def _build_scientific_tab(self):
        tb.Label(
            self.sci_tab, text="Scientific Functions (applied to the current number)",
            font=("Segoe UI", 10, "italic")
        ).pack(anchor=W, pady=(0, 10))

        grid = tb.Frame(self.sci_tab)
        grid.pack(fill=BOTH, expand=YES)

        sci_buttons = [
            ("sin", lambda: self.press_unary("sin")), ("cos", lambda: self.press_unary("cos")),
            ("tan", lambda: self.press_unary("tan")), ("log", lambda: self.press_unary("log")),
            ("ln", lambda: self.press_unary("ln")), ("n!", lambda: self.press_unary("factorial")),
            ("π", self.insert_pi), ("e", self.insert_e),
            ("|x|", lambda: self.press_unary("absolute")), ("Clear", self.clear_display),
        ]

        for j in range(5):
            grid.columnconfigure(j, weight=1)

        for idx, (text, cmd) in enumerate(sci_buttons):
            r, c = divmod(idx, 5)
            tb.Button(grid, text=text, bootstyle="info-outline", command=cmd).grid(
                row=r, column=c, sticky=NSEW, padx=4, pady=4, ipady=14
            )

        note = (
            "Tip: type a number in the display above, then press a scientific "
            "function button (e.g. type 30 then press 'sin')."
        )
        tb.Label(self.sci_tab, text=note, wraplength=780, bootstyle="secondary").pack(
            anchor=W, pady=(15, 0)
        )

    # ---------------- Data Science tab ----------------
    def _build_data_science_tab(self):
        top = tb.Frame(self.ds_tab)
        top.pack(fill=X)

        tb.Label(top, text="Enter values (comma separated):", font=("Segoe UI", 10, "bold")).pack(
            anchor=W
        )
        self.ds_input_var = tk.StringVar()
        entry = tb.Entry(top, textvariable=self.ds_input_var, font=("Consolas", 13))
        entry.pack(fill=X, pady=(4, 8), ipady=6)
        entry.insert(0, "10, 20, 30, 40, 50")

        btn_row = tb.Frame(top)
        btn_row.pack(fill=X, pady=(0, 8))

        stat_buttons = [
            ("Mean", "mean"), ("Median", "median"), ("Mode", "mode"),
            ("Variance", "variance"), ("Std Dev", "std_dev"), ("Min", "minimum"),
            ("Max", "maximum"), ("Range", "data_range"), ("Quartiles", "quartiles"),
            ("IQR", "iqr"), ("Sum", "sum"), ("Count", "count"),
        ]

        grid = tb.Frame(top)
        grid.pack(fill=X)
        for j in range(6):
            grid.columnconfigure(j, weight=1)
        for idx, (label, method) in enumerate(stat_buttons):
            r, c = divmod(idx, 6)
            tb.Button(
                grid, text=label, bootstyle="primary-outline",
                command=lambda m=method, l=label: self.run_statistic(m, l)
            ).grid(row=r, column=c, sticky=NSEW, padx=3, pady=3, ipady=8)

        tb.Button(
            top, text="Compute ALL Statistics", bootstyle="success",
            command=self.run_all_statistics
        ).pack(fill=X, pady=(8, 8), ipady=6)

        # Output box
        tb.Label(self.ds_tab, text="Results:", font=("Segoe UI", 10, "bold")).pack(anchor=W)
        self.ds_output = tk.Text(self.ds_tab, height=10, font=("Consolas", 11), wrap="word")
        self.ds_output.pack(fill=BOTH, expand=YES, pady=(4, 0))

    # ---------------- Graph tab ----------------
    def _build_graph_tab(self):
        controls = tb.Frame(self.graph_tab)
        controls.pack(fill=X)

        tb.Label(controls, text="Expression (e.g. y = x^2, sin(x), ln(x)):").grid(
            row=0, column=0, columnspan=4, sticky=W
        )
        self.graph_expr_var = tk.StringVar(value="y = x^2")
        tb.Entry(controls, textvariable=self.graph_expr_var, font=("Consolas", 12)).grid(
            row=1, column=0, columnspan=4, sticky=EW, pady=(2, 8), ipady=5
        )

        tb.Label(controls, text="X min:").grid(row=2, column=0, sticky=W)
        self.graph_xmin_var = tk.StringVar(value="-10")
        tb.Entry(controls, textvariable=self.graph_xmin_var, width=8).grid(row=2, column=1, sticky=W, padx=5)

        tb.Label(controls, text="X max:").grid(row=2, column=2, sticky=W)
        self.graph_xmax_var = tk.StringVar(value="10")
        tb.Entry(controls, textvariable=self.graph_xmax_var, width=8).grid(row=2, column=3, sticky=W, padx=5)

        for c in range(4):
            controls.columnconfigure(c, weight=1)

        tb.Button(
            self.graph_tab, text="📈 Plot Graph", bootstyle="success", command=self.plot_graph
        ).pack(fill=X, pady=8, ipady=6)

        self.graph_canvas_frame = tb.Frame(self.graph_tab, bootstyle="secondary")
        self.graph_canvas_frame.pack(fill=BOTH, expand=YES)
        self._graph_canvas_widget = None

    # ---------------- History tab ----------------
    def _build_history_tab(self):
        btn_row = tb.Frame(self.history_tab)
        btn_row.pack(fill=X, pady=(0, 8))

        tb.Button(btn_row, text="Clear History", bootstyle="danger-outline",
                  command=self.clear_history).pack(side=LEFT, padx=3)
        tb.Button(btn_row, text="Save History (.txt)", bootstyle="secondary",
                  command=self.save_history).pack(side=LEFT, padx=3)
        tb.Button(btn_row, text="Export to CSV", bootstyle="secondary",
                  command=self.export_history_csv).pack(side=LEFT, padx=3)

        self.history_listbox = tk.Listbox(self.history_tab, font=("Consolas", 11))
        self.history_listbox.pack(fill=BOTH, expand=YES)

    # ------------------------------------------------------------------
    # Status bar
    # ------------------------------------------------------------------
    def _build_status_bar(self):
        bar = tb.Frame(self, padding=(10, 4), bootstyle="secondary")
        bar.pack(fill=X, side=BOTTOM)

        self.status_var = tk.StringVar(value="Calculator Ready")
        tb.Label(bar, textvariable=self.status_var, bootstyle="inverse-secondary").pack(side=LEFT)

        self.theme_status_var = tk.StringVar(value=f"Theme: {self.current_theme_name}")
        tb.Label(bar, textvariable=self.theme_status_var, bootstyle="inverse-secondary").pack(
            side=RIGHT, padx=(10, 0)
        )

        self.clock_var = tk.StringVar()
        tb.Label(bar, textvariable=self.clock_var, bootstyle="inverse-secondary").pack(side=RIGHT)

    def _tick_clock(self):
        self.clock_var.set(time.strftime("%Y-%m-%d  %H:%M:%S"))
        self.after(1000, self._tick_clock)

    def set_status(self, message):
        self.status_var.set(message)

    # ------------------------------------------------------------------
    # Keyboard support
    # ------------------------------------------------------------------
    def _bind_keyboard(self):
        for digit in "0123456789.":
            self.bind(digit, lambda e, d=digit: self.press_digit(d))
        for op, symbol in [("+", "+"), ("-", "-"), ("*", "*"), ("/", "/")]:
            self.bind(op, lambda e, s=symbol: self.press_op(s))
        self.bind("<Return>", lambda e: self.evaluate_expression())
        self.bind("=", lambda e: self.evaluate_expression())
        self.bind("<KP_Enter>", lambda e: self.evaluate_expression())
        self.bind("<Escape>", lambda e: self.clear_display())
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Delete>", lambda e: self.clear_display())

    # ------------------------------------------------------------------
    # Basic / Scientific calculator logic
    # ------------------------------------------------------------------
    def press_digit(self, digit):
        if self.just_evaluated:
            self.expression = ""
            self.just_evaluated = False
        self.expression += digit
        self.display_var.set(self.expression)

    def press_op(self, op):
        if self.expression == "" and op not in ("-",):
            return
        self.just_evaluated = False
        # store using human-readable symbols but keep python-evaluable expression
        self.expression += f" {op} "
        self.display_var.set(self.expression)

    def insert_pi(self):
        self._insert_constant(self.calc.pi())

    def insert_e(self):
        self._insert_constant(self.calc.e())

    def _insert_constant(self, value):
        if self.just_evaluated:
            self.expression = ""
            self.just_evaluated = False
        self.expression += format_result(value)
        self.display_var.set(self.expression)

    def backspace(self):
        self.expression = self.expression[:-1]
        self.display_var.set(self.expression if self.expression else "0")

    def clear_display(self):
        self.expression = ""
        self.display_var.set("0")
        self.set_status("Calculator Ready")

    def press_unary(self, func_name):
        """Apply a single-argument function (sin, cos, sqrt, ...) to the current display value."""
        text = self.display_var.get().strip()
        if not is_number(text):
            messagebox.showerror("Invalid Input", "Please enter a valid number first.")
            return
        try:
            value = float(text)
            func = getattr(self.calc, func_name)
            result = func(value)
            result_str = format_result(result)
            self.history.add_entry(f"{func_name}({format_result(value)})", result_str)
            self._refresh_history_list()
            self.expression = result_str
            self.display_var.set(result_str)
            self.just_evaluated = True
            self.set_status(f"{func_name} calculated successfully")
        except CalculatorError as exc:
            messagebox.showerror("Calculation Error", str(exc))
            self.set_status("Error: " + str(exc))

    def evaluate_expression(self):
        """Evaluate the running expression string (supports + - * / % ** %%)."""
        expr = self.expression.strip()
        if expr == "":
            return
        try:
            result = self._safe_eval(expr)
            result_str = format_result(result)
            self.history.add_entry(expr, result_str)
            self._refresh_history_list()
            self.display_var.set(result_str)
            self.expression = result_str
            self.just_evaluated = True
            self.set_status("Calculation complete")
        except CalculatorError as exc:
            messagebox.showerror("Calculation Error", str(exc))
            self.set_status("Error: " + str(exc))
        except ZeroDivisionError:
            messagebox.showerror("Calculation Error", "Cannot divide by zero.")
            self.set_status("Error: division by zero")
        except Exception:
            messagebox.showerror("Calculation Error", "Invalid expression.")
            self.set_status("Error: invalid expression")

    def _safe_eval(self, expr):
        """Safely evaluate a simple two-operand-at-a-time arithmetic expression.

        Supports chained expressions like "12 + 5 - 3" by evaluating them
        left to right through the Calculator class methods (rather than
        Python's `eval`, keeping full control over error handling).
        `%%` represents the modulus operator (to avoid clashing with '%').
        """
        # tokenize on spaces (press_op always inserts spaced operators)
        tokens = expr.split()
        if not tokens:
            raise CalculatorError("Nothing to calculate.")

        # First token must be a number (allow leading negative sign)
        if not is_number(tokens[0]):
            raise CalculatorError("Expression must start with a number.")

        result = float(tokens[0])
        i = 1
        while i < len(tokens):
            op = tokens[i]
            if i + 1 >= len(tokens) or not is_number(tokens[i + 1]):
                raise CalculatorError("Incomplete expression.")
            operand = float(tokens[i + 1])

            if op == "+":
                result = self.calc.add(result, operand)
            elif op == "-":
                result = self.calc.subtract(result, operand)
            elif op == "*":
                result = self.calc.multiply(result, operand)
            elif op == "/":
                result = self.calc.divide(result, operand)
            elif op == "%":
                result = self.calc.percentage(result, operand)
            elif op == "**":
                result = self.calc.power(result, operand)
            elif op == "%%":
                result = self.calc.modulus(result, operand)
            else:
                raise CalculatorError(f"Unknown operator '{op}'.")

            i += 2

        return result

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------
    def _current_value(self):
        text = self.display_var.get().strip()
        if not is_number(text):
            raise CalculatorError("Display does not contain a valid number.")
        return float(text)

    def memory_add(self):
        try:
            value = self.calc.memory_add(self._current_value())
            self.set_status(f"Added to memory. Memory = {format_result(value)}")
        except CalculatorError as exc:
            messagebox.showerror("Memory Error", str(exc))

    def memory_subtract(self):
        try:
            value = self.calc.memory_subtract(self._current_value())
            self.set_status(f"Subtracted from memory. Memory = {format_result(value)}")
        except CalculatorError as exc:
            messagebox.showerror("Memory Error", str(exc))

    def memory_recall(self):
        value = self.calc.memory_recall()
        self.expression = format_result(value)
        self.display_var.set(self.expression)
        self.just_evaluated = True
        self.set_status("Memory recalled")

    def memory_clear(self):
        self.calc.memory_clear()
        self.set_status("Memory cleared")

    def copy_result(self):
        self.clipboard_clear()
        self.clipboard_append(self.display_var.get())
        self.set_status("Result copied to clipboard")

    def paste_into_display(self):
        try:
            text = self.clipboard_get()
            if is_number(text.strip()):
                self.expression = text.strip()
                self.display_var.set(self.expression)
                self.set_status("Pasted from clipboard")
        except tk.TclError:
            self.set_status("Clipboard is empty")

    # ------------------------------------------------------------------
    # Data Science tab logic
    # ------------------------------------------------------------------
    def run_statistic(self, method_name, label):
        try:
            stats = DataStatistics(self.ds_input_var.get())
            method = getattr(stats, method_name)
            result = method()
            if isinstance(result, tuple):  # quartiles
                text = f"{label}: Q1={format_result(result[0])}, Q2={format_result(result[1])}, Q3={format_result(result[2])}\n"
                expr = f"Quartiles({self.ds_input_var.get()})"
                result_str = f"Q1={format_result(result[0])}, Q2={format_result(result[1])}, Q3={format_result(result[2])}"
            else:
                result_str = result if isinstance(result, str) else format_result(result)
                text = f"{label}: {result_str}\n"
                expr = f"{label}({self.ds_input_var.get()})"

            self.ds_output.insert(tk.END, text)
            self.ds_output.see(tk.END)
            self.history.add_entry(expr, result_str)
            self._refresh_history_list()
            self.set_status(f"{label} calculated successfully")
        except CalculatorError as exc:
            messagebox.showerror("Statistics Error", str(exc))
            self.set_status("Error: " + str(exc))

    def run_all_statistics(self):
        try:
            stats = DataStatistics(self.ds_input_var.get())
            summary = stats.summary()
            self.ds_output.delete("1.0", tk.END)
            self.ds_output.insert(tk.END, "===== Full Statistical Summary =====\n")
            for key, value in summary.items():
                value_str = value if isinstance(value, str) else format_result(value)
                self.ds_output.insert(tk.END, f"{key}: {value_str}\n")

            self.history.add_entry(f"AllStats({self.ds_input_var.get()})", "see summary")
            self._refresh_history_list()
            self.set_status("All statistics calculated successfully")
        except CalculatorError as exc:
            messagebox.showerror("Statistics Error", str(exc))
            self.set_status("Error: " + str(exc))

    # ------------------------------------------------------------------
    # Graph tab logic
    # ------------------------------------------------------------------
    def plot_graph(self):
        try:
            xmin = float(self.graph_xmin_var.get())
            xmax = float(self.graph_xmax_var.get())
        except ValueError:
            messagebox.showerror("Graph Error", "X min and X max must be numbers.")
            return

        try:
            figure = self.plotter.build_figure(self.graph_expr_var.get(), xmin, xmax)
        except CalculatorError as exc:
            messagebox.showerror("Graph Error", str(exc))
            self.set_status("Error: " + str(exc))
            return

        if self._graph_canvas_widget is not None:
            self._graph_canvas_widget.get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(figure, master=self.graph_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
        self._graph_canvas_widget = canvas

        self.history.add_entry(f"Plot({self.graph_expr_var.get()})", "graph rendered")
        self._refresh_history_list()
        self.set_status("Graph plotted successfully")

    # ------------------------------------------------------------------
    # History tab logic
    # ------------------------------------------------------------------
    def _refresh_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for line in self.history.get_display_lines():
            self.history_listbox.insert(tk.END, line)

    def clear_history(self):
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
            self.history.clear()
            self._refresh_history_list()
            self.set_status("History cleared")

    def save_history(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text file", "*.txt")], initialfile="history.txt"
        )
        if not path:
            return
        self.history.save_to_file(path)
        self.set_status(f"History saved to {path}")

    def export_history_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV file", "*.csv")], initialfile="history.csv"
        )
        if not path:
            return
        self.history.export_csv(path)
        self.set_status(f"History exported to {path}")

    # ------------------------------------------------------------------
    # Theme handling
    # ------------------------------------------------------------------
    def _theme_display_name(self, theme_key):
        for display_name, key in THEMES.items():
            if key == theme_key:
                return display_name
        return "Light"

    def apply_theme(self, display_name):
        theme_key = THEMES.get(display_name, "flatly")
        self.style.theme_use(theme_key)
        self.current_theme_name = display_name
        self.theme_status_var.set(f"Theme: {display_name}")
        self.theme_manager.save_theme(theme_key)
        self.set_status(f"Theme switched to {display_name}")

    # ------------------------------------------------------------------
    # Help
    # ------------------------------------------------------------------
    def show_about(self):
        messagebox.showinfo(
            "About",
            f"{APP_TITLE}\n\n"
            "A beginner-friendly, professional desktop calculator built for "
            "a Data Science class.\n\n"
            "Built with Python, Tkinter, ttkbootstrap, NumPy and Matplotlib.\n\n"
            "Features: basic + scientific calculator, statistical analysis, "
            "graph plotting, calculation history, and theme switching."
        )


def main():
    """Application entry point: show the splash screen, then launch the app."""

    def launch_main_app():
        app = CalculatorApp()
        app.mainloop()

    splash = SplashScreen(on_finish=launch_main_app)
    splash.mainloop()


if __name__ == "__main__":
    main()
