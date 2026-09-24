"""
Module 5 · Script 06 – Set New / Multiple Values for a Specific Cell or Row
===========================================================================

Covers: .at / .iat (single cell, fastest), .loc / .iloc (cells, rows,
columns), conditional updates, updating a whole row, adding a new row,
replace(), mask/where, and the chained-assignment pitfall.
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """Inventory table."""
    return pd.DataFrame({
        "item": ["Pen", "Notebook", "Bag", "Bottle", "Lamp"],
        "price": [10, 45, 800, 250, 600],
        "stock": [100, 50, 5, 20, 0],
        "status": ["ok", "ok", "low", "ok", "out"],
    }, index=["i1", "i2", "i3", "i4", "i5"])


def main() -> None:
    """Every common way of changing values."""
    df = make_df()
    section("Original")
    print(df)

    section("1️⃣  One cell with .at (label) and .iat (position)")
    df.at["i1", "price"] = 12
    df.iat[1, 2] = 55  # row 1 (i2), column 2 (stock)
    print(df)

    section("2️⃣  One cell with .loc / .iloc")
    df.loc["i4", "stock"] = 25
    df.iloc[2, 0] = "Backpack"
    print(df)

    section("3️⃣  Several cells in one row")
    df.loc["i5", ["stock", "status"]] = [30, "ok"]
    print(df.loc["i5"])

    section("4️⃣  A whole row at once")
    df.loc["i2"] = ["Diary", 60, 40, "ok"]
    print(df)

    section("5️⃣  Several rows × several columns")
    df.loc[["i1", "i2"], "price"] = [15, 65]
    df.iloc[0:2, 3] = "promo"
    print(df)

    section("6️⃣  Conditional update (all rows matching a condition)")
    df.loc[df["stock"] < 10, "status"] = "reorder"
    df.loc[df["price"] > 500, "price"] = df["price"] * 0.9  # 10% off expensive items
    print(df)

    section("7️⃣  Add a brand-new row / column via loc")
    df.loc["i6"] = ["Mug", 120, 15, "ok"]
    df.loc[:, "on_sale"] = df["status"] == "promo"
    print(df)

    section("8️⃣  replace() and mask()")
    print(df.replace({"status": {"ok": "in stock"}})[["item", "status"]])
    print(df["stock"].mask(df["stock"] > 30, 30).tolist(), "<- capped at 30")

    section("9️⃣  Pitfall: chained assignment")
    print("❌  df[df['item'] == 'Mug']['price'] = 99   (modifies a temporary copy)")
    print("✅  df.loc[df['item'] == 'Mug', 'price'] = 99")
    df.loc[df["item"] == "Mug", "price"] = 99
    print(df.loc["i6"].to_dict())


if __name__ == "__main__":
    main()
