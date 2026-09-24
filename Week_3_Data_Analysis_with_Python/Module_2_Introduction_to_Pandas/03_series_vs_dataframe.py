"""
Module 2 · Script 03 – Series vs DataFrames
===========================================

Side-by-side comparison of the two core pandas structures and how to
convert between them.
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def compare() -> None:
    """Show attributes of a Series and a DataFrame next to each other."""
    s = pd.Series([88, 92, 79], index=["Aadil", "Yaana", "Sama"], name="maths")
    df = pd.DataFrame({"maths": [88, 92, 79], "science": [91, 85, 73]},
                      index=["Aadil", "Yaana", "Sama"])

    section("1️⃣  Series (1-D)")
    print(s)
    section("2️⃣  DataFrame (2-D)")
    print(df)

    section("3️⃣  Attribute comparison")
    rows = [
        ("type", type(s).__name__, type(df).__name__),
        ("ndim", s.ndim, df.ndim),
        ("shape", s.shape, df.shape),
        ("size", s.size, df.size),
        ("index", list(s.index), list(df.index)),
        ("name / columns", s.name, list(df.columns)),
        ("dtype(s)", str(s.dtype), dict(df.dtypes.astype(str))),
    ]
    print(f"{'attribute':<16}{'Series':<30}{'DataFrame'}")
    print("-" * 80)
    for attr, s_val, df_val in rows:
        print(f"{attr:<16}{str(s_val):<30}{df_val}")


def convert() -> None:
    """Move between Series and DataFrame."""
    df = pd.DataFrame({"maths": [88, 92, 79], "science": [91, 85, 73]},
                      index=["Aadil", "Yaana", "Sama"])
    section("4️⃣  Converting between them")
    print("df['maths']   -> Series   :", type(df["maths"]).__name__)
    print("df[['maths']] -> DataFrame:", type(df[["maths"]]).__name__)
    print("df.loc['Sama'] (a row)    ->", type(df.loc["Sama"]).__name__)
    s = df["maths"]
    print("\nseries.to_frame():\n", s.to_frame())
    print("\nCombine Series into a DataFrame with pd.concat(axis=1):")
    english = pd.Series([70, 95, 81], index=df.index, name="english")
    print(pd.concat([s, english], axis=1))

    section("5️⃣  When to use which?")
    print("* Series    -> a single variable / column (e.g. all ages)")
    print("* DataFrame -> a full dataset with many variables (rows = records)")


if __name__ == "__main__":
    compare()
    convert()
