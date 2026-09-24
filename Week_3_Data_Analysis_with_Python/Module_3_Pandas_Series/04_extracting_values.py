"""
Module 3 · Script 04 – Extracting Values from Series
====================================================

Covers: [] with labels, .loc (label-based), .iloc (position-based),
.at / .iat (single values), slicing, boolean masks, .get() with a default,
.where/.mask, and converting to Python objects.
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main() -> None:
    """Walk through every way of pulling values out of a Series."""
    marks = pd.Series([88, 72, 95, 61, 79, 90],
                      index=["Aadil", "Yaana", "Sama", "Lilith", "Rohan", "Meera"],
                      name="marks")
    print(marks)

    section("1️⃣  Single value")
    print("marks['Sama']       :", marks["Sama"])
    print("marks.loc['Sama']   :", marks.loc["Sama"], "(label)")
    print("marks.iloc[2]       :", marks.iloc[2], "(position)")
    print("marks.at['Sama']    :", marks.at["Sama"], "(fast label scalar)")
    print("marks.iat[2]        :", marks.iat[2], "(fast position scalar)")
    print("marks.get('Zoya', 0):", marks.get("Zoya", 0), "(default if missing)")

    section("2️⃣  Several values")
    print("marks[['Aadil', 'Meera']]:\n", marks[["Aadil", "Meera"]])
    print("marks.iloc[[0, -1]]:\n", marks.iloc[[0, -1]])

    section("3️⃣  Slicing")
    print("marks.iloc[1:4]  (stop EXCLUDED):\n", marks.iloc[1:4])
    print("marks.loc['Yaana':'Lilith']  (stop INCLUDED):\n", marks.loc["Yaana":"Lilith"])
    print("marks.iloc[::2]:\n", marks.iloc[::2])

    section("4️⃣  Boolean masks")
    print("marks[marks >= 85]:\n", marks[marks >= 85])
    print("marks[(marks > 70) & (marks < 90)]:\n", marks[(marks > 70) & (marks < 90)])
    print("marks[marks.index.str.startswith('R')]:\n",
          marks[marks.index.str.startswith("R")])

    section("5️⃣  where / mask (keep shape, replace others)")
    print("where(marks >= 75) :", marks.where(marks >= 75).tolist())
    print("mask(marks < 75, 0):", marks.mask(marks < 75, 0).tolist())

    section("6️⃣  Top / bottom values")
    print("nlargest(2) :", marks.nlargest(2).to_dict())
    print("nsmallest(2):", marks.nsmallest(2).to_dict())

    section("7️⃣  Converting to Python objects")
    print("to_list():", marks.to_list())
    print("to_dict():", marks.to_dict())
    print("to_numpy():", marks.to_numpy())
    print("'Sama' in marks:", "Sama" in marks, "(checks the INDEX)")
    print("95 in marks.values:", 95 in marks.values)


if __name__ == "__main__":
    main()
