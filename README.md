# 📊 Data Science Smart Calculator

A modern, professional desktop calculator built with **Python**, **Tkinter**, and **ttkbootstrap** It combines a normal calculator with a scientific calculator, a full statistics/data-science toolkit (powered by **NumPy**), and a graph plotter (powered by **Matplotlib**) — all in one clean, tabbed dashboard.

---

## 🖼️ Screenshots

| Basic Calculator | Scientific Calculator |
|---|---|
| ![Basic](assets/screenshots/01_basic_calculator.png) | ![Scientific](assets/screenshots/02_scientific_calculator.png) |

| Data Science Statistics | Graph Plotter |
|---|---|
| ![Data Science](assets/screenshots/03_data_science.png) | ![Graph](assets/screenshots/04_graph.png) |

| History Panel | Dark Theme |
|---|---|
| ![History](assets/screenshots/05_history.png) | ![Dark Theme](assets/screenshots/06_dark_theme.png) |

*(All screenshots above are real captures of the running application.)*

---

## ✨ Project Overview

This project is a single desktop application organized into five tabs:

1. **🧮 Basic** — everyday arithmetic (add, subtract, multiply, divide, %, power, square, square root, cube, cube root, modulus) plus memory buttons (M+, M-, MR, MC) and a Copy button.
2. **🔬 Scientific** — sin, cos, tan, log, ln, factorial, π, e, and absolute value.
3. **📊 Data Science** — enter a list of numbers (e.g. `10,20,30,40,50`) and instantly compute mean, median, mode, variance, standard deviation, min, max, range, quartiles, IQR, sum, and count — one at a time or all at once.
4. **📈 Graph** — type an expression like `y = x^2` (or `sin(x)`, `ln(x)`, etc.) and see it plotted live inside the app.
5. **🕘 History** — every calculation from every tab is logged with a timestamp, and can be cleared, saved to a text file, or exported to CSV.

The app also has a splash/loading screen, a full menu bar, a live status bar (clock, ready message, active theme), keyboard shortcuts, and 4 switchable themes (Light, Dark, Blue, Green) that are remembered the next time you open the app.

---

## 🚀 Features

### 1. Modern GUI
- Clean dashboard built with `ttkbootstrap` (a themed layer on top of Tkinter)
- Professional color palette, rounded/flat buttons, tab icons (emoji)
- Responsive layout that resizes with the window
- Dark / Light / Blue / Green theme toggle (remembered between sessions)
- Large calculator display at the top of the window

### 2. Basic Calculator
Addition, Subtraction, Multiplication, Division, Percentage, Power, Square, Square Root, Cube, Cube Root, Modulus.

### 3. Scientific Calculator
sin, cos, tan, log (base 10), ln (natural log), factorial, π, e, absolute value.

### 4. Data Science Calculator
Mean, Median, Mode, Variance, Standard Deviation, Minimum, Maximum, Range, Quartiles (Q1/Q2/Q3), Interquartile Range (IQR), Sum, Count — computed from a single comma-separated list such as `10,20,30,40,50`.

### 5. NumPy Integration
All statistical calculations (`statistics.py`) use **NumPy** (`np.mean`, `np.median`, `np.std`, `np.var`, `np.percentile`, etc.) for fast, accurate, industry-standard computation.

### 6. History Panel
Every calculation (from Basic, Scientific, Data Science, or Graph tabs) is recorded, e.g.:
```
[14:03:21] 12 + 5 = 17
[14:03:40] Mean(10,20,30) = 20
```
You can **Clear History**, **Save History** (as a `.txt` file) or **Export History to CSV**.

### 7. Graph Feature
Type an expression such as `y = x^2` or `sin(x) + 2`, pick an X range, and click **Plot Graph** — the chart is rendered live inside the app using Matplotlib embedded in Tkinter.

### 8. Themes
Light, Dark, Blue, and Green themes, selectable from the **View** menu. The last-used theme is saved to `assets/config.json` and automatically restored on the next launch.

### 9. Error Handling
Friendly, non-crashing messages for:
- Division by zero
- Invalid / non-numeric input
- Empty input fields
- Invalid statistical lists (e.g. text mixed with numbers)
- Invalid graph expressions

### 10. Menu Bar
- **File** → New, Save History, Export CSV, Exit
- **Edit** → Copy Result, Paste, Clear
- **View** → Dark Mode, Light Mode, Blue Theme, Green Theme
- **Help** → About

### 11. Status Bar
Shows the current time (updating every second), a "Calculator Ready" / status message, and the currently active theme.

### 12. Keyboard Support
- Number keys `0-9` and `.`
- Operators `+ - * /`
- `Enter` / numeric keypad Enter → calculate (`=`)
- `Escape` / `Delete` → clear
- `Backspace` → delete last character

### 13. Bonus Features
- Memory functions: **M+**, **M-**, **MR**, **MC**
- **Copy** button to copy the current result to the clipboard, and **Paste** from the Edit menu
- Animated **splash screen** with a loading progress bar on startup
- Recent calculations always visible in the History tab

---

## 🗂️ Project Structure

```
calculator/
│
├── main.py            # GUI layer: windows, tabs, menu bar, status bar, events
├── calculator.py       # Basic + scientific arithmetic engine (no GUI code)
├── statistics.py       # NumPy-powered data-science statistics engine
├── graph.py            # Matplotlib graph builder (expression parser + plotting)
├── history.py           # Calculation history: store / save / export
├── utils.py            # Validation helpers, formatting, theme persistence
├── assets/
│   ├── config.json     # Auto-created; remembers your last selected theme
│   └── screenshots/    # Screenshots used in this README
├── requirements.txt
└── README.md
```

**Why split into separate files?** Each module has a single responsibility:
`calculator.py`, `statistics.py`, and `graph.py` are pure "business logic" with
**no Tkinter imports at all** — they could be reused in a command-line tool or
a web app tomorrow. `main.py` is the only file that touches the GUI, and it
imports the other modules to do the actual computation. `history.py` and
`utils.py` are small, focused helper modules shared by everything else.

---

## ⚙️ Requirements

- Python 3.9+
- `ttkbootstrap` (modern Tkinter theming)
- `numpy` (statistics)
- `matplotlib` (graphing)
- Tkinter (usually included with Python; on Linux you may need to install
  `python3-tk` via your package manager, e.g. `sudo apt install python3-tk`)

All Python package requirements are listed in `requirements.txt`.

---

## 📦 Installation

```bash
# 1. Clone / copy the project folder, then move into it
cd calculator

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python3 main.py
```

A splash screen will appear briefly, then the main calculator window will open.

---

## 🧠 Project Flow (How it all fits together)

1. `main.py` starts → shows `SplashScreen` with a fake loading animation.
2. Once loading finishes, `CalculatorApp` (also in `main.py`) is created:
   it builds the menu bar, the top display, a `ttkbootstrap.Notebook` with
   5 tabs, and a bottom status bar.
3. When you click a button (say, "7" then "+" then "5" then "="):
   - Digit/operator clicks build up a text expression (`self.expression`).
   - Pressing "=" calls `_safe_eval()`, which walks the expression and
     calls the matching method on a `Calculator` instance
     (`calculator.py`) for each operator — e.g. `calc.add(7, 5)`.
   - The result is formatted (`utils.format_result`), shown in the
     display, and logged via `HistoryManager.add_entry()`
     (`history.py`).
4. In the **Data Science** tab, typing `10,20,30` and clicking "Mean"
   creates a `DataStatistics` object (`statistics.py`), which parses the
   text into a NumPy array and calls `np.mean()` on it.
5. In the **Graph** tab, typing `y = x^2` calls `GraphPlotter.build_figure()`
   (`graph.py`), which safely evaluates the expression over a NumPy
   array of x-values and returns a Matplotlib `Figure`, embedded into
   the Tkinter window via `FigureCanvasTkAgg`.
6. Every action also updates the status bar and, where relevant, the
   History tab.

---

## 📚 Documentation

Every class and function in every file has a docstring explaining what
it does, its parameters, and what it returns or raises. Read `calculator.py`,
`statistics.py`, `graph.py`, `history.py`, and `utils.py` for the full
business-logic documentation, and `main.py` for how the GUI wires
everything together (see the module docstring at the top of `main.py`
for a full explanation of the "project flow").

---

## 🔮 Future Improvements

- Voice input/output for hands-free calculation
- Unit conversion tab (length, weight, currency, etc.)
- Chart export as PNG directly from the Graph tab
- Multi-line/expression history "replay" (click a history item to reload it)
- Support for matrices and linear algebra operations
- Packaging as a standalone `.exe` / `.app` using PyInstaller

---

## 👩‍💻 Author Notes

This project was built as a teaching-friendly example of **Object-Oriented
Programming** in Python: each concern (arithmetic, statistics, graphing,
history, utilities, GUI) lives in its own class/module, following PEP 8
formatting and clear docstrings throughout — making it easy for students
to read, extend, and learn from.
