"""
Module 2 · Script 01 – Installing Pandas & Pandas Introduction
==============================================================

Install Pandas (run once in your terminal / virtual environment):

    pip install pandas

Pandas is built on top of NumPy and gives us two labelled data structures:
  * Series    – a 1-D labelled array (one column)
  * DataFrame – a 2-D labelled table (many columns, like a spreadsheet / SQL table)
"""

import sys

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_install() -> None:
    """Show versions – the first thing to check when something breaks."""
    section("1️⃣  Checking the installation")
    print("Python :", sys.version.split()[0])
    print("pandas :", pd.__version__)
    print("numpy  :", np.__version__, "(pandas is built on NumPy)")


def first_look() -> None:
    """Create a tiny Series and DataFrame to see what they look like."""
    section("2️⃣  A first Series")
    temperatures = pd.Series([31, 29, 35, 33], index=["Mon", "Tue", "Wed", "Thu"],
                             name="temp_c")
    print(temperatures)
    print("temperatures['Wed'] ->", temperatures["Wed"])

    section("3️⃣  A first DataFrame")
    df = pd.DataFrame({
        "city": ["Delhi", "Mumbai", "Pune"],
        "population_m": [32.9, 21.3, 7.4],
        "coastal": [False, True, False],
    })
    print(df)
    print("\nEach column of a DataFrame is a Series:", type(df["city"]))


def display_options() -> None:
    """Handy display settings when printing big tables."""
    section("4️⃣  Useful display options")
    pd.set_option("display.max_columns", 20)
    pd.set_option("display.width", 120)
    pd.set_option("display.precision", 2)
    print("display.max_columns =", pd.get_option("display.max_columns"))
    print("display.precision   =", pd.get_option("display.precision"))
    print("(Use pd.reset_option('all') to go back to defaults.)")


if __name__ == "__main__":
    check_install()
    first_look()
    display_options()
