"""
Module 5 · Script 01 – Different Sorting Algorithms in a DataFrame
==================================================================

Covers: sort_values (one / many columns, mixed directions, na_position),
sort_index (rows and columns), the `kind=` sorting algorithm
('quicksort', 'mergesort', 'heapsort', 'stable'), stability, a timing
comparison, and custom sort orders with `key=` and Categorical.
"""

import time

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """Employee table with ties and a missing value."""
    return pd.DataFrame({
        "name": ["Aadil", "Yaana", "Sama", "Lilith", "Rohan", "Meera", "Kabir"],
        "dept": ["Eng", "Mkt", "Eng", "HR", "Fin", "Eng", "Mkt"],
        "salary": [85000, 62000, 72000, 58000, np.nan, 72000, 62000],
        "level": ["Senior", "Junior", "Mid", "Mid", "Senior", "Mid", "Junior"],
    }, index=[3, 6, 1, 7, 2, 5, 4])


def basic_sorting(df: pd.DataFrame) -> None:
    """sort_values and sort_index."""
    section("1️⃣  sort_values by one column")
    print(df.sort_values("salary"))
    print("\nDescending, NaN first:\n", df.sort_values("salary", ascending=False,
                                                        na_position="first"))

    section("2️⃣  sort_values by several columns (mixed directions)")
    print(df.sort_values(["dept", "salary"], ascending=[True, False]))

    section("3️⃣  sort_index (rows) and sort_index(axis=1) (columns)")
    print(df.sort_index())
    print(df.sort_index(axis=1).head(3))


def algorithms(df: pd.DataFrame) -> None:
    """The kind= parameter and what 'stable' means."""
    section("4️⃣  kind= – choosing the sorting algorithm")
    print("""
 kind        | algorithm       | stable? | notes
-------------+-----------------+---------+-----------------------------------
 'quicksort' | introsort       |  no     | default, fast, in-place
 'mergesort' | merge/timsort   |  YES    | keeps ties in original order
 'heapsort'  | heapsort        |  no     | O(n log n) worst case, low memory
 'stable'    | radix/timsort   |  YES    | same guarantee as mergesort
""")
    print("NOTE: kind= only applies when sorting on a SINGLE column/label.")
    for kind in ["quicksort", "mergesort", "heapsort", "stable"]:
        order = df.sort_values("salary", kind=kind)["name"].tolist()
        print(f"{kind:<10} -> {order}")

    section("5️⃣  Stability demo – sort by name, then stable-sort by level")
    step1 = df.sort_values("name")
    step2 = step1.sort_values("level", kind="stable")
    print("Names stay alphabetical inside each level because 'stable' keeps ties:")
    print(step2[["level", "name"]])


def timing() -> None:
    """Rough speed comparison of the algorithms on 1 million rows."""
    section("6️⃣  Speed comparison (1,000,000 random numbers)")
    rng = np.random.default_rng(42)
    big = pd.DataFrame({"value": rng.integers(0, 1_000_000, size=1_000_000)})
    for kind in ["quicksort", "mergesort", "heapsort", "stable"]:
        start = time.perf_counter()
        big.sort_values("value", kind=kind)
        print(f"{kind:<10}: {(time.perf_counter() - start) * 1000:7.1f} ms")


def custom_orders(df: pd.DataFrame) -> None:
    """Sort using key= and a Categorical order."""
    section("7️⃣  Custom orders")
    print("key=str.lower (case-insensitive) on name:")
    print(df.sort_values("name", key=lambda s: s.str.lower())["name"].tolist())

    level_order = pd.CategoricalDtype(["Junior", "Mid", "Senior"], ordered=True)
    ordered = df.astype({"level": level_order}).sort_values(["level", "salary"])
    print("\nLogical level order Junior < Mid < Senior:\n", ordered)


if __name__ == "__main__":
    data = make_df()
    basic_sorting(data)
    algorithms(data)
    timing()
    custom_orders(data)
