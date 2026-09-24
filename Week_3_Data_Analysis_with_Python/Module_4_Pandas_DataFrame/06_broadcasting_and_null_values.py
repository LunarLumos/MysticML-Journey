"""
Module 4 · Script 06 – Broadcasting Operations & Dropping/Filling Null Values
=============================================================================

Broadcasting: an operation with a scalar (or a Series) is applied to every
matching cell automatically – no loops.

Null values: detect with isna(), remove with dropna(), replace with
fillna() / ffill() / bfill() / interpolate().
"""

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def broadcasting() -> None:
    """Scalar, Series (row-wise / column-wise) broadcasting."""
    prices = pd.DataFrame({"Q1": [100, 200, 150], "Q2": [110, 190, 160], "Q3": [120, 210, 155]},
                          index=["apple", "mango", "grape"])
    section("1️⃣  Scalar broadcasting")
    print(prices)
    print("\nprices * 1.18 (add 18% GST to every cell):\n", (prices * 1.18).round(1))
    print("\nprices - 10:\n", prices - 10)

    section("2️⃣  Broadcasting a Series across columns (row-wise match)")
    discount = pd.Series({"Q1": 0, "Q2": 5, "Q3": 10})
    print("discount per quarter:", discount.to_dict())
    print(prices - discount)  # aligned on COLUMN labels

    section("3️⃣  Broadcasting a Series down rows (axis=0)")
    fruit_tax = pd.Series({"apple": 1.05, "mango": 1.10, "grape": 1.00})
    print(prices.mul(fruit_tax, axis=0).round(1))  # aligned on ROW labels

    section("4️⃣  Broadcasting on a single column & comparisons")
    prices["Q4"] = prices["Q3"] + 5
    print(prices)
    print("\nprices > 150:\n", prices > 150)
    print("\nNormalise each column (x - mean) / std:\n",
          ((prices - prices.mean()) / prices.std()).round(2))


def null_values() -> None:
    """Detect, drop and fill missing values in a DataFrame."""
    df = pd.DataFrame({
        "name": ["Aadil", "Yaana", None, "Lilith", "Rohan", "Meera"],
        "age": [25, np.nan, 35, 40, np.nan, 29],
        "city": ["Delhi", "Paris", "London", None, "Pune", None],
        "score": [88.0, 92.0, np.nan, np.nan, 75.0, 81.0],
    })
    section("5️⃣  Detecting nulls")
    print(df)
    print("\nisna().sum():\n", df.isna().sum())
    print("rows with any null:", df.isna().any(axis=1).sum())
    print("total nulls       :", int(df.isna().sum().sum()))

    section("6️⃣  Dropping nulls")
    print("dropna() – drop rows with ANY null:\n", df.dropna())
    print("\ndropna(how='all') – only rows where ALL are null:", len(df.dropna(how="all")), "rows")
    print("\ndropna(subset=['name']):\n", df.dropna(subset=["name"]))
    print("\ndropna(thresh=3) – keep rows with >= 3 non-null values:\n", df.dropna(thresh=3))
    print("\ndropna(axis=1) – drop COLUMNS with nulls:", df.dropna(axis=1).columns.tolist())

    section("7️⃣  Filling nulls")
    print("fillna(0):\n", df.fillna(0))
    filled = df.fillna({
        "name": "Unknown",
        "age": df["age"].median(),
        "city": df["city"].mode()[0],
        "score": df["score"].mean(),
    })
    print("\nfillna with a dict (per-column strategy):\n", filled.round(1))
    print("\nffill():\n", df.ffill())
    print("\nbfill() on score:", df["score"].bfill().tolist())
    print("interpolate() on score:", df["score"].interpolate().tolist())


if __name__ == "__main__":
    broadcasting()
    null_values()
