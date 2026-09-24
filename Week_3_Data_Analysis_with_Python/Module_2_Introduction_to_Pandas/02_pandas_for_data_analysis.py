"""
Module 2 · Script 02 – Use of Pandas for Data Analysis
======================================================

A mini end-to-end analysis on data/employees.csv showing the typical
workflow:  load -> inspect -> clean -> transform -> analyse -> summarise.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "employees.csv"


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def load() -> pd.DataFrame:
    """Step 1 – load the data (parse the date column as real dates)."""
    section("1️⃣  Load")
    df = pd.read_csv(DATA_FILE, parse_dates=["join_date"])
    print(f"Loaded {len(df)} rows x {df.shape[1]} columns from {DATA_FILE.name}")
    return df


def inspect(df: pd.DataFrame) -> None:
    """Step 2 – get to know the data."""
    section("2️⃣  Inspect")
    print(df.head())
    print("\n.info():")
    df.info()
    print("\n.describe():\n", df.describe().round(2))
    print("\nMissing values per column:\n", df.isna().sum())


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Step 3 – fix missing values."""
    section("3️⃣  Clean")
    df = df.copy()
    # Fill a missing salary with the median salary of that department.
    df["salary"] = df["salary"].fillna(
        df.groupby("department")["salary"].transform("median"))
    df["rating"] = df["rating"].fillna(df["rating"].mean()).round(1)
    print("Missing values after cleaning:", int(df.isna().sum().sum()))
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Step 4 – derive new columns."""
    section("4️⃣  Transform")
    df = df.copy()
    df["join_year"] = df["join_date"].dt.year
    df["experience_yrs"] = 2025 - df["join_year"]
    df["salary_band"] = pd.cut(df["salary"], bins=[0, 50000, 80000, float("inf")],
                               labels=["Low", "Mid", "High"])
    print(df[["name", "salary", "salary_band", "join_year", "experience_yrs"]])
    return df


def analyse(df: pd.DataFrame) -> None:
    """Step 5 – answer questions with groupby / sorting / counting."""
    section("5️⃣  Analyse")
    print("Average salary per department:")
    print(df.groupby("department")["salary"].mean().sort_values(ascending=False).round(0))
    print("\nHeadcount per city:\n", df["city"].value_counts())
    print("\nTop 3 earners:\n", df.nlargest(3, "salary")[["name", "department", "salary"]])
    print("\nPivot – mean rating by department & salary band:")
    print(df.pivot_table(index="department", columns="salary_band", values="rating",
                         aggfunc="mean", observed=False).round(2))


if __name__ == "__main__":
    data = load()
    inspect(data)
    data = clean(data)
    data = transform(data)
    analyse(data)
