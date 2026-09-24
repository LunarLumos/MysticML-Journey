"""
Module 4 · Script 04 – Display Particular Columns (Subset of a DataFrame)
=========================================================================

Covers: single column (Series) vs [[ ]] (DataFrame), several columns,
reordering, filter(like/regex), select_dtypes, loc/iloc column slices,
and combining row + column selection.
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_employees() -> pd.DataFrame:
    """Employee table with mixed column types."""
    return pd.DataFrame({
        "emp_id": [101, 102, 103, 104, 105],
        "name": ["Aadil", "Yaana", "Sama", "Lilith", "Rohan"],
        "dept": ["Eng", "Mkt", "Eng", "HR", "Fin"],
        "salary_2024": [80000, 60000, 70000, 55000, 90000],
        "salary_2025": [85000, 62000, 72000, 58000, 91000],
        "remote": [True, False, True, False, True],
    })


def main() -> None:
    """Every common way of selecting columns."""
    df = make_employees()
    section("Original")
    print(df)

    section("1️⃣  One column -> Series")
    print(df["name"])
    print("dot notation df.dept works too:", df.dept.tolist())

    section("2️⃣  One column as a DataFrame -> df[['name']]")
    print(df[["name"]])

    section("3️⃣  Several columns (and in any order you like)")
    print(df[["salary_2025", "name", "dept"]])

    section("4️⃣  filter() by name pattern")
    print(df.filter(like="salary"))
    print(df.filter(regex=r"^(name|dept)$"))

    section("5️⃣  select_dtypes()")
    print("numbers only:\n", df.select_dtypes(include="number"))
    print("text only:\n", df.select_dtypes(exclude=["number", "bool"]))

    section("6️⃣  loc / iloc column slices")
    print("df.loc[:, 'name':'salary_2024']:\n", df.loc[:, "name":"salary_2024"])
    print("df.iloc[:, [1, -1]]:\n", df.iloc[:, [1, -1]])

    section("7️⃣  Rows AND columns together")
    print(df.loc[df["dept"] == "Eng", ["name", "salary_2025"]])
    print(df.iloc[:3, :2])

    section("8️⃣  Drop-the-rest approach and column lists")
    wanted = [col for col in df.columns if col != "emp_id"]
    print("columns except emp_id:", wanted)
    print(df[wanted].head(2))


if __name__ == "__main__":
    main()
