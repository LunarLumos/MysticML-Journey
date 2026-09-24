"""
Module 2 · Script 04 – Reading Data from CSV and TXT Files
==========================================================

Covers: pd.read_csv with common options, reading delimited .txt files,
reading a plain text file line by line, and writing data back out.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def read_csv_basic() -> pd.DataFrame:
    """The simplest possible read."""
    section("1️⃣  pd.read_csv – basic")
    df = pd.read_csv(DATA_DIR / "employees.csv")
    print(df.head())
    print("shape:", df.shape)
    return df


def read_csv_options() -> None:
    """The options you will use most often."""
    section("2️⃣  pd.read_csv – useful options")
    df = pd.read_csv(
        DATA_DIR / "employees.csv",
        usecols=["emp_id", "name", "department", "salary", "join_date"],  # only these
        index_col="emp_id",            # use a column as the row index
        parse_dates=["join_date"],     # convert text -> datetime
        nrows=5,                       # read only the first 5 rows
        dtype={"department": "category"},
    )
    print(df)
    print("\ndtypes:\n", df.dtypes)


def read_txt_files() -> None:
    """Delimited .txt files are just CSVs with a different separator."""
    section("3️⃣  Reading a pipe-delimited .txt file")
    df = pd.read_csv(DATA_DIR / "employees.txt", sep="|")
    print(df)

    section("4️⃣  Reading a free-text .txt file line by line")
    lines = pd.read_csv(DATA_DIR / "notes.txt", sep="\t", header=None, names=["line"])
    print(lines)
    print("Number of lines:", len(lines))
    # Alternative with plain Python:
    text = (DATA_DIR / "notes.txt").read_text(encoding="utf-8").splitlines()
    print("Same with pathlib ->", len(text), "lines")


def write_files(df: pd.DataFrame) -> None:
    """Save DataFrames back to disk (into outputs/)."""
    section("5️⃣  Writing CSV / TXT")
    OUTPUT_DIR.mkdir(exist_ok=True)
    csv_path = OUTPUT_DIR / "engineering.csv"
    txt_path = OUTPUT_DIR / "engineering.txt"
    engineering = df[df["department"] == "Engineering"]
    engineering.to_csv(csv_path, index=False)
    engineering.to_csv(txt_path, sep="\t", index=False)
    print(f"Saved {len(engineering)} rows -> {csv_path}")
    print(f"Saved tab-separated copy -> {txt_path}")
    print("Round trip check:", pd.read_csv(csv_path).shape)


if __name__ == "__main__":
    employees = read_csv_basic()
    read_csv_options()
    read_txt_files()
    write_files(employees)
