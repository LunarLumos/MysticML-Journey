"""
Module 3 · Script 03 – Different Functions in Series & Sorting of Series
=======================================================================

Covers: head/tail, describe, statistical functions, idxmax/idxmin,
cumulative functions, unique/nunique, round/clip, astype, map/replace,
and sorting with sort_values / sort_index (incl. sort algorithms).
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def build_series() -> pd.Series:
    """Monthly rainfall (mm) – a small demo Series."""
    return pd.Series(
        [78.5, 12.0, 45.2, 101.3, 12.0, 66.7, 230.4, 190.1],
        index=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
        name="rainfall_mm",
    )


def useful_functions(s: pd.Series) -> None:
    """Common inspection and statistics functions."""
    section("1️⃣  Inspecting")
    print("head(3):\n", s.head(3))
    print("tail(2):\n", s.tail(2))
    print("describe():\n", s.describe().round(2))

    section("2️⃣  Statistics")
    print(f"sum={s.sum():.1f}  mean={s.mean():.2f}  median={s.median():.2f}")
    print(f"min={s.min()}  max={s.max()}  std={s.std():.2f}  var={s.var():.2f}")
    print("mode:", s.mode().tolist())
    print("quantile(0.9):", s.quantile(0.9).round(2))
    print("idxmax (wettest month):", s.idxmax(), "| idxmin:", s.idxmin())
    print("count (non-null):", s.count())

    section("3️⃣  Cumulative & change")
    print("cumsum:\n", s.cumsum().round(1).tolist())
    print("pct_change (first 4):", s.pct_change().round(2).head(4).tolist())

    section("4️⃣  Unique values & transformations")
    print("unique :", s.unique())
    print("nunique:", s.nunique())
    print("round(0):", s.round(0).tolist())
    print("clip(20, 150):", s.clip(20, 150).tolist())
    print("astype(int):", s.astype(int).tolist())
    level = s.map(lambda mm: "heavy" if mm > 100 else "normal")
    print("map ->", level.tolist())
    print("replace 12.0 -> 0:", s.replace(12.0, 0).tolist())


def sorting(s: pd.Series) -> None:
    """sort_values, sort_index, and sorting algorithms."""
    section("5️⃣  sort_values")
    print("ascending:\n", s.sort_values())
    print("descending (top 3):\n", s.sort_values(ascending=False).head(3))

    section("6️⃣  sort_index")
    print(s.sort_index())  # alphabetical month labels

    section("7️⃣  Missing values while sorting (na_position)")
    with_nan = pd.Series([3, None, 1, 2])
    print("na_position='last' :", with_nan.sort_values().tolist())
    print("na_position='first':", with_nan.sort_values(na_position="first").tolist())

    section("8️⃣  Sorting algorithms (kind=...)")
    for kind in ["quicksort", "mergesort", "heapsort", "stable"]:
        print(f"{kind:<10} -> {s.sort_values(kind=kind).index.tolist()}")
    print("'mergesort'/'stable' keep ties (Feb & May = 12.0) in original order.")

    section("9️⃣  rank()")
    print(s.rank(ascending=False).astype(int).sort_values())


if __name__ == "__main__":
    rainfall = build_series()
    useful_functions(rainfall)
    sorting(rainfall)
