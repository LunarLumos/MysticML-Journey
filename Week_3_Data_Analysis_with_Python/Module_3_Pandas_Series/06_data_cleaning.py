"""
Module 3 · Script 06 – Data Cleaning: Duplicates and Missing Values
===================================================================

Covers:
  * detecting & removing duplicates (duplicated, drop_duplicates, keep=)
  * detecting missing values (isna / notna / hasnans)
  * dropping (dropna) and filling (fillna with value/mean/median/mode,
    ffill, bfill) and interpolate()
"""

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def duplicates() -> None:
    """Find and remove repeated values."""
    cities = pd.Series(["Delhi", "Mumbai", "Delhi", "Pune", "Mumbai", "Delhi", "Goa"])
    section("1️⃣  Detecting duplicates")
    print(pd.DataFrame({"city": cities, "duplicated()": cities.duplicated()}))
    print("Number of duplicates:", cities.duplicated().sum())

    section("2️⃣  keep= controls which copy counts as 'original'")
    print("keep='first':", cities.duplicated(keep="first").tolist())
    print("keep='last' :", cities.duplicated(keep="last").tolist())
    print("keep=False  :", cities.duplicated(keep=False).tolist(), "(flag ALL copies)")

    section("3️⃣  Removing duplicates")
    print("drop_duplicates()          :", cities.drop_duplicates().tolist())
    print("drop_duplicates(keep='last'):", cities.drop_duplicates(keep="last").tolist())
    print("keep=False (only uniques)  :", cities.drop_duplicates(keep=False).tolist())
    print("reset_index after dropping:\n", cities.drop_duplicates().reset_index(drop=True))


def missing_values() -> None:
    """Find, drop and fill NaN values."""
    temps = pd.Series([22.5, np.nan, 24.0, None, 26.5, np.nan, 25.0],
                      index=pd.date_range("2025-07-01", periods=7), name="temp_c")
    section("4️⃣  Detecting missing values")
    print(temps)
    print("isna()  :", temps.isna().tolist())
    print("notna() :", temps.notna().tolist())
    print("hasnans :", temps.hasnans, "| isna().sum():", temps.isna().sum())
    print(f"% missing: {temps.isna().mean() * 100:.1f}%")

    section("5️⃣  Dropping missing values")
    print(temps.dropna())

    section("6️⃣  Filling missing values")
    print("fillna(0)        :", temps.fillna(0).tolist())
    print("fillna(mean)     :", temps.fillna(temps.mean()).round(2).tolist())
    print("fillna(median)   :", temps.fillna(temps.median()).tolist())
    print("fillna(mode)     :", temps.fillna(temps.mode()[0]).tolist())
    print("ffill (forward)  :", temps.ffill().tolist())
    print("bfill (backward) :", temps.bfill().tolist())
    print("interpolate()    :", temps.interpolate().tolist())

    section("7️⃣  Text data: None, empty strings and 'N/A'")
    raw = pd.Series(["Aadil", "", "N/A", None, "Sama", "Aadil"])
    cleaned = raw.replace({"": np.nan, "N/A": np.nan})
    print("raw      :", raw.tolist())
    print("cleaned  :", cleaned.tolist())
    print("filled   :", cleaned.fillna("Unknown").tolist())
    print("full pipe:", cleaned.dropna().drop_duplicates().tolist())


if __name__ == "__main__":
    duplicates()
    missing_values()
