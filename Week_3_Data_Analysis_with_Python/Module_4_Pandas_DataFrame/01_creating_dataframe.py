"""
Module 4 · Script 01 – What is a DataFrame & Creating DataFrames
================================================================

A DataFrame is a 2-D labelled table: rows (index) x columns, where every
column is a pandas Series. It is THE workhorse of data analysis in Python.

Covers creating DataFrames from: dict of lists, list of dicts, list of
lists, NumPy arrays, dict of Series, and files (read_csv on an in-memory
string so the script needs no external files).
"""

from io import StringIO

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main() -> None:
    """Show every common way of creating a DataFrame."""
    section("1️⃣  From a dict of lists (keys -> column names)")
    df = pd.DataFrame({
        "name": ["Aadil", "Yaana", "Sama"],
        "age": [25, 30, 35],
        "city": ["Delhi", "Paris", "London"],
    })
    print(df)

    section("2️⃣  From a list of dicts (one dict per row – like JSON records)")
    records = [
        {"product": "Laptop", "price": 65000, "stock": 12},
        {"product": "Mouse", "price": 800},          # missing 'stock' -> NaN
        {"product": "Monitor", "price": 12000, "stock": 5},
    ]
    print(pd.DataFrame(records))

    section("3️⃣  From a list of lists + column names")
    rows = [["Mon", 31, 60], ["Tue", 29, 72], ["Wed", 33, 55]]
    print(pd.DataFrame(rows, columns=["day", "temp_c", "humidity"]))

    section("4️⃣  From a NumPy array with custom index & columns")
    rng = np.random.default_rng(0)
    arr = rng.integers(40, 100, size=(3, 4))
    print(pd.DataFrame(arr, index=["Aadil", "Yaana", "Sama"],
                       columns=["maths", "physics", "chemistry", "english"]))

    section("5️⃣  From a dict of Series (aligned on the index)")
    population = pd.Series({"Delhi": 32.9, "Mumbai": 21.3, "Pune": 7.4})
    area = pd.Series({"Delhi": 1484, "Mumbai": 603, "Goa": 3702})
    print(pd.DataFrame({"population_m": population, "area_km2": area}))

    section("6️⃣  From CSV text (same as reading a file)")
    csv_text = "id,item,qty\n1,pen,10\n2,book,3\n3,bag,1\n"
    print(pd.read_csv(StringIO(csv_text)))

    section("7️⃣  Empty DataFrame, then add rows with pd.concat")
    empty = pd.DataFrame(columns=["task", "done"])
    print("empty.shape:", empty.shape, "| empty.empty:", empty.empty)
    new_rows = pd.DataFrame([{"task": "Learn pandas", "done": True}])
    print(pd.concat([empty, new_rows], ignore_index=True))

    section("8️⃣  Why use a DataFrame?")
    print("* Labelled rows & columns  * Mixed column types  * Built-in stats")
    print("* Handles missing data     * SQL-like filtering, grouping, joining")
    print("* Reads/writes CSV, Excel, SQL, JSON ...")


if __name__ == "__main__":
    main()
