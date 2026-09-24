"""
Module 5 · Script 03 – Filter Data with AND (&) and OR (|) Operations
====================================================================

Rules to remember:
  * use  &  (AND),  |  (OR),  ~  (NOT)  – NOT the Python words and/or/not
  * wrap EVERY condition in parentheses: (cond1) & (cond2)
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """Employee table."""
    return pd.DataFrame({
        "name": ["Aadil", "Yaana", "Sama", "Lilith", "Rohan", "Meera", "Kabir", "Zoya"],
        "dept": ["Eng", "Mkt", "Eng", "HR", "Fin", "Eng", "Sales", "Mkt"],
        "city": ["Delhi", "Mumbai", "Pune", "Delhi", "Mumbai", "Pune", "Delhi", "Pune"],
        "age": [28, 32, 25, 41, 36, 30, 27, 29],
        "salary": [85000, 62000, 72000, 58000, 91000, 98000, 45000, 54000],
    })


def main() -> None:
    """AND, OR, NOT and combinations."""
    df = make_df()
    section("Original")
    print(df)

    section("1️⃣  AND (&) – both conditions true")
    print("Engineers earning > 80k:")
    print(df[(df["dept"] == "Eng") & (df["salary"] > 80000)])

    section("2️⃣  OR (|) – at least one condition true")
    print("In Delhi OR younger than 28:")
    print(df[(df["city"] == "Delhi") | (df["age"] < 28)])

    section("3️⃣  NOT (~)")
    print("Everyone NOT in Pune:")
    print(df[~(df["city"] == "Pune")][["name", "city"]])

    section("4️⃣  Combining AND + OR (use brackets to control order)")
    cond = ((df["dept"] == "Eng") | (df["dept"] == "Mkt")) & (df["age"] < 30)
    print("(Eng OR Mkt) AND age < 30:")
    print(df[cond])

    section("5️⃣  Named masks make complex filters readable")
    is_senior = df["age"] >= 30
    high_pay = df["salary"] >= 60000
    metro = df["city"].isin(["Delhi", "Mumbai"])
    print("senior & high_pay & metro:")
    print(df[is_senior & high_pay & metro])

    section("6️⃣  Same filters with query() (uses the words and / or / not)")
    print(df.query("dept == 'Eng' and salary > 80000"))
    print(df.query("city == 'Delhi' or age < 28")[["name"]].T)

    section("7️⃣  Common mistake")
    try:
        df[df["age"] > 30 and df["salary"] > 60000]
    except ValueError as err:
        print("Using `and` raises ValueError:", str(err)[:60], "...")
    try:
        df[df["age"] > 30 & df["salary"] > 60000]
    except (TypeError, ValueError) as err:
        print("Forgetting brackets also fails:", type(err).__name__)


if __name__ == "__main__":
    main()
