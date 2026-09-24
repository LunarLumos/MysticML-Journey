"""
Module 4 · Script 03 – Dropping Columns / Rows from a DataFrame
===============================================================

Covers: drop(columns=...), drop(index=...), axis=0/1, inplace vs
re-assignment, dropping by condition, errors='ignore', del and pop().
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_products() -> pd.DataFrame:
    """A small product catalogue."""
    return pd.DataFrame({
        "product": ["Laptop", "Phone", "Tablet", "Watch", "Camera"],
        "brand": ["Dell", "Apple", "Samsung", "Fitbit", "Canon"],
        "price": [65000, 80000, 30000, 15000, 55000],
        "stock": [10, 0, 25, 40, 0],
        "internal_code": ["X1", "X2", "X3", "X4", "X5"],
        "notes": [None, "hot", None, None, "old model"],
    }, index=["p1", "p2", "p3", "p4", "p5"])


def main() -> None:
    """Demonstrate all the ways of dropping data."""
    df = make_products()
    section("Original")
    print(df)

    section("1️⃣  Drop one column  -> df.drop(columns='notes')")
    print(df.drop(columns="notes"))

    section("2️⃣  Drop several columns (axis=1 style)")
    print(df.drop(["internal_code", "notes"], axis=1))

    section("3️⃣  Drop rows by index label  -> df.drop(index=['p2', 'p5'])")
    print(df.drop(index=["p2", "p5"]))

    section("4️⃣  Drop rows by position (look up the labels first)")
    print(df.drop(df.index[[0, 1]]))

    section("5️⃣  Drop rows by condition (out of stock)")
    out_of_stock = df[df["stock"] == 0].index
    print("labels to drop:", out_of_stock.tolist())
    print(df.drop(out_of_stock))
    print("…or simply keep the others:\n", df[df["stock"] > 0])

    section("6️⃣  errors='ignore' – no crash if a label doesn't exist")
    print(df.drop(columns=["does_not_exist"], errors="ignore").columns.tolist())

    section("7️⃣  inplace=True vs re-assigning")
    df_copy = df.copy()
    result = df_copy.drop(columns="notes", inplace=True)
    print("inplace returns:", result, "| columns now:", df_copy.columns.tolist())
    df_copy = df_copy.drop(columns="internal_code")  # preferred style
    print("after re-assignment:", df_copy.columns.tolist())

    section("8️⃣  del and pop()")
    df_copy = df.copy()
    del df_copy["notes"]
    popped = df_copy.pop("internal_code")  # removes AND returns the column
    print("popped column:", popped.tolist())
    print("remaining    :", df_copy.columns.tolist())

    section("9️⃣  Drop duplicate rows")
    dup = pd.concat([df, df.iloc[[0]]])
    print("rows before:", len(dup), "| after drop_duplicates():", len(dup.drop_duplicates()))


if __name__ == "__main__":
    main()
