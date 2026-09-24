"""
Module 4 · Script 02 – DataFrame Different Functions
====================================================

Covers: head/tail/sample, shape/size/ndim/columns/index/dtypes, info,
describe, statistics along axes, nunique/value_counts, groupby/agg,
corr, copy, transpose, astype and memory usage.
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_students() -> pd.DataFrame:
    """A small student results table used throughout the script."""
    return pd.DataFrame({
        "name": ["Aadil", "Yaana", "Sama", "Lilith", "Rohan", "Meera", "Kabir", "Zoya"],
        "gender": ["M", "F", "F", "F", "M", "F", "M", "F"],
        "section": ["A", "B", "A", "B", "A", "B", "A", "B"],
        "maths": [88, 92, 79, 65, 95, 70, 55, 84],
        "science": [91, 85, 73, 70, 89, 77, 60, 90],
        "english": [75, 95, 81, 88, 68, 92, 72, 79],
    })


def inspection(df: pd.DataFrame) -> None:
    """First look at a DataFrame."""
    section("1️⃣  head / tail / sample")
    print(df.head(3))
    print(df.tail(2))
    print(df.sample(2, random_state=1))

    section("2️⃣  Structure attributes")
    print("shape  :", df.shape)
    print("size   :", df.size)
    print("ndim   :", df.ndim)
    print("columns:", df.columns.tolist())
    print("index  :", df.index)
    print("dtypes :\n", df.dtypes)

    section("3️⃣  info() and describe()")
    df.info()
    print(df.describe())
    print(df.describe(exclude="number"))  # text columns (works in pandas 2 & 3)


def statistics(df: pd.DataFrame) -> None:
    """Row- and column-wise statistics."""
    subjects = ["maths", "science", "english"]
    section("4️⃣  Column statistics (axis=0, default)")
    print("mean:\n", df[subjects].mean().round(2))
    print("max:\n", df[subjects].max())

    section("5️⃣  Row statistics (axis=1)")
    totals = df[subjects].sum(axis=1)
    print(pd.DataFrame({"name": df["name"], "total": totals,
                        "average": df[subjects].mean(axis=1).round(1)}))

    section("6️⃣  Counting")
    print("nunique():\n", df.nunique())
    print("gender value_counts():\n", df["gender"].value_counts())

    section("7️⃣  groupby + agg")
    print(df.groupby("section")[subjects].mean().round(1))
    print(df.groupby("gender").agg(students=("name", "count"),
                                   best_maths=("maths", "max"),
                                   avg_english=("english", "mean")))

    section("8️⃣  Correlation between subjects")
    print(df[subjects].corr().round(2))


def utilities(df: pd.DataFrame) -> None:
    """copy, transpose, astype, memory usage."""
    section("9️⃣  copy(), T, astype(), memory_usage()")
    backup = df.copy()  # independent copy – changes won't affect df
    backup.loc[0, "maths"] = 0
    print("original maths[0] still:", df.loc[0, "maths"])
    print("Transposed (first 3 rows):\n", df.head(3).T)
    converted = df.astype({"section": "category", "maths": "float64"})
    print("After astype:\n", converted.dtypes)
    print("Memory (bytes):", int(df.memory_usage(deep=True).sum()))


if __name__ == "__main__":
    students = make_students()
    inspection(students)
    statistics(students)
    utilities(students)
