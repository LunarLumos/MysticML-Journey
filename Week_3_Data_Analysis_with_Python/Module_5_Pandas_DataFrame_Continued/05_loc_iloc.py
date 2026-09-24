"""
Module 5 · Script 05 – Retrieve Row Values Using loc and iloc
=============================================================

  loc  -> LABEL based    df.loc[row_labels, column_labels]   (slice end INCLUDED)
  iloc -> POSITION based df.iloc[row_positions, col_positions] (slice end EXCLUDED)
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """Student marks indexed by roll number."""
    return pd.DataFrame({
        "name": ["Aadil", "Yaana", "Sama", "Lilith", "Rohan", "Meera"],
        "maths": [88, 92, 79, 65, 95, 70],
        "science": [91, 85, 73, 70, 89, 77],
        "english": [75, 95, 81, 88, 68, 92],
    }, index=["R101", "R102", "R103", "R104", "R105", "R106"])


def loc_examples(df: pd.DataFrame) -> None:
    """Label-based access."""
    section("1️⃣  loc – one row (returns a Series)")
    print(df.loc["R103"])

    section("2️⃣  loc – several rows (returns a DataFrame)")
    print(df.loc[["R101", "R105"]])

    section("3️⃣  loc – slice of labels (end label INCLUDED)")
    print(df.loc["R102":"R104"])

    section("4️⃣  loc – rows AND columns")
    print(df.loc["R102":"R104", ["name", "maths"]])
    print("\nSingle cell df.loc['R105', 'science'] =", df.loc["R105", "science"])

    section("5️⃣  loc – boolean condition")
    print(df.loc[df["maths"] > 85, ["name", "maths"]])


def iloc_examples(df: pd.DataFrame) -> None:
    """Position-based access."""
    section("6️⃣  iloc – one row by position")
    print(df.iloc[0])
    print("\nLast row df.iloc[-1]['name'] =", df.iloc[-1]["name"])

    section("7️⃣  iloc – several rows / slices (end EXCLUDED)")
    print(df.iloc[[0, 2, 4]])
    print(df.iloc[1:3])

    section("8️⃣  iloc – rows AND columns")
    print(df.iloc[:3, 1:3])
    print("\nSingle cell df.iloc[4, 2] =", df.iloc[4, 2])

    section("9️⃣  loc vs iloc side by side")
    print("df.loc['R101':'R103'] ->", len(df.loc["R101":"R103"]), "rows (inclusive)")
    print("df.iloc[0:3]          ->", len(df.iloc[0:3]), "rows (exclusive end = 3)")
    print("Row values as a list  ->", df.loc["R104"].tolist())
    print("Row values as a dict  ->", df.iloc[3].to_dict())


if __name__ == "__main__":
    students = make_df()
    loc_examples(students)
    iloc_examples(students)
