"""
Module 3 · Script 01 – Concept of Series & Creating Series using Pandas
=======================================================================

A Series = values (a NumPy array) + index (labels) + optional name.
Covers creating Series from lists, NumPy arrays, dicts, scalars and ranges.
"""

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def anatomy() -> None:
    """Look inside a Series."""
    section("1️⃣  Anatomy of a Series")
    s = pd.Series([250, 180, 320], index=["pizza", "burger", "biryani"], name="price")
    print(s)
    print("\ns.values :", s.values, type(s.values).__name__)
    print("s.index  :", list(s.index))
    print("s.name   :", s.name)
    print("s.dtype  :", s.dtype)
    print("s.shape  :", s.shape, "| s.size:", s.size)


def creation_methods() -> None:
    """All the common ways of building a Series."""
    section("2️⃣  From a list (default index 0..n-1)")
    print(pd.Series([10, 20, 30]))

    section("3️⃣  From a list with a custom index")
    print(pd.Series([90, 75, 60], index=["Aadil", "Yaana", "Sama"]))

    section("4️⃣  From a NumPy array")
    print(pd.Series(np.linspace(0, 1, 4)))

    section("5️⃣  From a dictionary (keys become the index)")
    capitals = {"India": "New Delhi", "Japan": "Tokyo", "France": "Paris"}
    print(pd.Series(capitals))

    section("6️⃣  From a scalar (value repeated for each index label)")
    print(pd.Series(5, index=["a", "b", "c"]))

    section("7️⃣  With an explicit dtype, a name and a date index")
    s = pd.Series([1, 2, 3], dtype="float64", name="growth")
    print(s)
    dates = pd.date_range("2025-01-01", periods=4, freq="D")
    print(pd.Series([100, 102, 99, 105], index=dates, name="stock_price"))

    section("8️⃣  Mixed types become 'object' dtype")
    print(pd.Series([1, "two", 3.0, True]))


if __name__ == "__main__":
    anatomy()
    creation_methods()
