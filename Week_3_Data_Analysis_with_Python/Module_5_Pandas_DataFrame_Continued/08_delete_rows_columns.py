"""
Module 5 · Script 08 – Delete Rows or Columns in Pandas
=======================================================

Module 4 introduced drop(); here we go further: deleting by position,
by condition, by index range, by dtype, by missing-value share,
duplicate rows, and using del / pop / truncate.
"""

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """Sensor readings with some junk columns and rows."""
    return pd.DataFrame({
        "sensor": ["A", "B", "C", "D", "E", "F", "C"],
        "temp": [22.1, 23.4, -999.0, 21.8, 24.0, 22.9, -999.0],
        "humidity": [45, 50, 48, np.nan, 52, 47, 48],
        "unused": [np.nan, np.nan, np.nan, np.nan, 1, np.nan, np.nan],
        "debug_flag": [0, 0, 1, 0, 0, 0, 1],
    }, index=range(10, 17))


def main() -> None:
    """Delete rows and columns in many different ways."""
    df = make_df()
    section("Original")
    print(df)

    section("1️⃣  Delete columns by name")
    print(df.drop(columns=["debug_flag"]).columns.tolist())

    section("2️⃣  Delete columns by position")
    print(df.drop(columns=df.columns[[3, 4]]).columns.tolist())

    section("3️⃣  Delete columns that are mostly empty (> 50% NaN)")
    keep = df.columns[df.isna().mean() <= 0.5]
    print("kept:", keep.tolist())

    section("4️⃣  Delete columns by dtype (keep only numeric)")
    print(df.select_dtypes(include="number").columns.tolist())

    section("5️⃣  Delete rows by label and by position")
    print(df.drop(index=[10, 11]).index.tolist())
    print(df.drop(df.index[-2:]).index.tolist(), "<- last two removed")

    section("6️⃣  Delete rows by condition (bad sensor value -999)")
    cleaned = df[df["temp"] != -999.0]
    print(cleaned)

    section("7️⃣  Delete rows with missing values in a column")
    print(df.dropna(subset=["humidity"]).index.tolist())

    section("8️⃣  Delete duplicate rows (based on some columns)")
    print(df.drop_duplicates(subset=["sensor", "temp"]))

    section("9️⃣  Delete a range of rows with truncate / slicing")
    print("truncate(before=12, after=14):", df.truncate(before=12, after=14).index.tolist())
    print("df.iloc[2:] (drop first 2)  :", df.iloc[2:].index.tolist())

    section("🔟  del and pop (in place)")
    df_copy = df.copy()
    del df_copy["unused"]
    flags = df_copy.pop("debug_flag")
    print("popped flags sum:", flags.sum(), "| remaining:", df_copy.columns.tolist())


if __name__ == "__main__":
    main()
