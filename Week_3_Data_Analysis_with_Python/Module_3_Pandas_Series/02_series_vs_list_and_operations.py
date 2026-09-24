"""
Module 3 · Script 02 – Series vs List, Series Operations
========================================================

Covers: how a Series differs from a Python list, vectorised arithmetic,
index alignment (the pandas super-power), comparison & boolean ops, and
string / datetime accessors.
"""

import time

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def series_vs_list() -> None:
    """Compare behaviour of a list and a Series."""
    section("1️⃣  Series vs List")
    prices_list = [100, 200, 300]
    prices = pd.Series(prices_list, index=["pen", "book", "bag"])

    print(f"{'Feature':<28}{'List':<28}{'Series'}")
    print("-" * 80)
    print(f"{'Labels':<28}{'positions only':<28}custom labels {list(prices.index)}")
    print(f"{'x * 2':<28}{str(prices_list * 2):<28}{prices.mul(2).tolist()}")
    print(f"{'Access by label':<28}{'not possible':<28}prices['book'] = {prices['book']}")
    print(f"{'Built-in stats':<28}{'sum() only':<28}mean={prices.mean()}, std={prices.std():.1f}")
    print(f"{'Missing values':<28}{'None (breaks math)':<28}NaN (skipped by stats)")
    print(f"{'Data types':<28}{'any mix':<28}one dtype ({prices.dtype})")

    n = 1_000_000
    big_list = list(range(n))
    big_series = pd.Series(big_list)
    t0 = time.perf_counter()
    _ = [x + 1 for x in big_list]
    t_list = time.perf_counter() - t0
    t0 = time.perf_counter()
    _ = big_series + 1
    t_series = time.perf_counter() - t0
    print(f"\nAdding 1 to {n:,} items -> list {t_list*1000:.1f} ms | Series {t_series*1000:.1f} ms")


def arithmetic() -> None:
    """Vectorised maths and index alignment."""
    section("2️⃣  Arithmetic (vectorised)")
    s = pd.Series([10, 20, 30, 40], index=list("abcd"))
    print("s + 5:\n", s + 5)
    print("s * s:\n", s * s)
    print("s.pow(2).sum():", s.pow(2).sum())

    section("3️⃣  Index alignment – values are matched by LABEL, not position")
    jan = pd.Series({"apples": 50, "bananas": 30, "cherries": 20})
    feb = pd.Series({"bananas": 25, "cherries": 10, "dates": 40})
    print("jan + feb (labels missing on one side -> NaN):\n", jan + feb)
    print("\njan.add(feb, fill_value=0):\n", jan.add(feb, fill_value=0))


def comparisons_and_accessors() -> None:
    """Boolean Series, .str and .dt accessors."""
    section("4️⃣  Comparisons -> boolean Series")
    ages = pd.Series([15, 22, 37, 17, 64], index=["A", "B", "C", "D", "E"])
    adults = ages >= 18
    print(adults)
    print("Adults:", ages[adults].to_dict())
    print("ages.between(18, 40):", ages.between(18, 40).tolist())
    print("ages.isin([15, 64]) :", ages.isin([15, 64]).tolist())

    section("5️⃣  .str accessor for text")
    names = pd.Series(["  aadil ", "YAANA", "sama khan"])
    print("strip + title :", names.str.strip().str.title().tolist())
    print("len           :", names.str.strip().str.len().tolist())
    print("contains 'a'  :", names.str.lower().str.contains("a").tolist())

    section("6️⃣  .dt accessor for dates")
    dates = pd.Series(pd.to_datetime(["2025-01-15", "2025-06-30", "2025-12-25"]))
    print("year     :", dates.dt.year.tolist())
    print("month    :", dates.dt.month_name().tolist())
    print("weekday  :", dates.dt.day_name().tolist())


if __name__ == "__main__":
    series_vs_list()
    arithmetic()
    comparisons_and_accessors()
