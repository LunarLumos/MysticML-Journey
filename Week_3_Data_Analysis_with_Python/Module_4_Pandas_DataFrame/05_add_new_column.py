"""
Module 4 · Script 05 – Add a New Column to a DataFrame
======================================================

Covers: constant columns, list columns, computed columns, np.where
conditional columns, apply/map, insert() at a position, assign()
(method chaining), pd.cut bins, and adding a new row for completeness.
"""

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main() -> None:
    """Show all the common ways of adding columns."""
    df = pd.DataFrame({
        "item": ["Rice", "Milk", "Soap", "Bread", "Juice"],
        "qty": [2, 3, 5, 1, 4],
        "unit_price": [60.0, 28.0, 35.0, 45.0, 99.0],
    })
    section("Original")
    print(df)

    section("1️⃣  A constant value")
    df["store"] = "MysticMart"
    print(df)

    section("2️⃣  From a list (length must match the rows)")
    df["category"] = ["Grocery", "Dairy", "Home", "Bakery", "Drinks"]
    print(df)

    section("3️⃣  Computed from other columns (vectorised)")
    df["total"] = df["qty"] * df["unit_price"]
    print(df[["item", "qty", "unit_price", "total"]])

    section("4️⃣  Conditional column with np.where")
    df["big_order"] = np.where(df["total"] > 150, "yes", "no")
    print(df[["item", "total", "big_order"]])

    section("5️⃣  Using map() with a dictionary and apply() with a function")
    gst_rate = {"Grocery": 0.05, "Dairy": 0.0, "Home": 0.18, "Bakery": 0.05, "Drinks": 0.12}
    df["gst_rate"] = df["category"].map(gst_rate)
    df["label"] = df.apply(lambda row: f"{row['item']} x{row['qty']}", axis=1)
    print(df[["item", "category", "gst_rate", "label"]])

    section("6️⃣  insert() at a specific position")
    df.insert(0, "sku", [f"SKU{i:03d}" for i in range(1, len(df) + 1)])
    print(df.columns.tolist())

    section("7️⃣  assign() – returns a NEW DataFrame (great for chaining)")
    result = (df.assign(tax=lambda d: d["total"] * d["gst_rate"])
                .assign(grand_total=lambda d: (d["total"] + d["tax"]).round(2)))
    print(result[["item", "total", "tax", "grand_total"]])

    section("8️⃣  Binning numbers into categories with pd.cut")
    df["price_band"] = pd.cut(df["unit_price"], bins=[0, 40, 70, np.inf],
                              labels=["cheap", "medium", "premium"])
    print(df[["item", "unit_price", "price_band"]])

    section("9️⃣  Bonus – adding a new ROW with loc / concat")
    df.loc[len(df)] = ["SKU006", "Eggs", 12, 6.0, "MysticMart", "Dairy", 72.0,
                       "no", 0.0, "Eggs x12", "cheap"]
    print(df[["sku", "item", "qty", "total"]].tail(2))


if __name__ == "__main__":
    main()
