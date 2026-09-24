"""
Module 5 · Script 07 – Rename Index Labels or Columns in Pandas
===============================================================

Covers: rename(columns=dict), rename(index=dict), rename with a function,
assigning df.columns directly, add_prefix/add_suffix, set_axis,
rename_axis (name of the index) and cleaning messy column names.
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """A table with deliberately messy column names."""
    return pd.DataFrame({
        " Student Name ": ["Aadil", "Yaana", "Sama"],
        "Maths Marks": [88, 92, 79],
        "SCIENCE-marks": [91, 85, 73],
    }, index=["a", "b", "c"])


def main() -> None:
    """Rename columns and index labels in several ways."""
    df = make_df()
    section("Original")
    print(df)
    print("columns:", df.columns.tolist())

    section("1️⃣  rename(columns={old: new})")
    print(df.rename(columns={"Maths Marks": "maths", "SCIENCE-marks": "science"}))

    section("2️⃣  rename(index={old: new})")
    print(df.rename(index={"a": "r01", "b": "r02", "c": "r03"}))

    section("3️⃣  rename with a function (applies to every label)")
    print(df.rename(columns=str.upper).columns.tolist())
    print(df.rename(index=lambda label: f"row_{label}").index.tolist())

    section("4️⃣  Clean messy column names with the .str accessor")
    clean = df.copy()
    clean.columns = (clean.columns.str.strip()
                                  .str.lower()
                                  .str.replace(r"[\s\-]+", "_", regex=True))
    print(clean.columns.tolist())

    section("5️⃣  Assign all column names at once")
    whole = df.copy()
    whole.columns = ["name", "maths", "science"]
    print(whole)

    section("6️⃣  set_axis – same idea, returns a new DataFrame")
    print(whole.set_axis(["x", "y", "z"], axis=0))

    section("7️⃣  add_prefix / add_suffix")
    print(whole[["maths", "science"]].add_suffix("_2025"))
    print(whole[["maths", "science"]].add_prefix("score_").columns.tolist())

    section("8️⃣  rename_axis – give the index (or columns) a name")
    named = whole.rename_axis("roll_no").rename_axis("field", axis=1)
    print(named)

    section("9️⃣  inplace=True vs re-assignment")
    whole.rename(columns={"name": "student"}, inplace=True)
    print("after inplace rename:", whole.columns.tolist())


if __name__ == "__main__":
    main()
