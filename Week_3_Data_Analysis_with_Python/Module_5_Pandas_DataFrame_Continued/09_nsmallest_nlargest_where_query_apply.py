"""
Module 5 · Script 09 – .nsmallest(), .nlargest(), .where(), .query(), .apply()
==============================================================================

  nlargest / nsmallest -> top / bottom N rows by a column (faster than sort+head)
  where               -> keep values where condition is True, replace the rest
  query               -> filter with a readable string expression
  apply               -> run a function on each column (axis=0) or row (axis=1)
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """A small cricket-stats table."""
    return pd.DataFrame({
        "player": ["Virat", "Rohit", "Gill", "Rahul", "Pant", "Jadeja", "Hardik", "Surya"],
        "team": ["RCB", "MI", "GT", "LSG", "DC", "CSK", "MI", "MI"],
        "matches": [14, 14, 16, 13, 14, 15, 12, 14],
        "runs": [741, 417, 890, 520, 446, 267, 216, 605],
        "strike_rate": [154.7, 150.0, 157.8, 136.1, 155.4, 140.5, 143.0, 167.9],
    })


def top_bottom(df: pd.DataFrame) -> None:
    """nlargest / nsmallest."""
    section("1️⃣  nlargest(3, 'runs')")
    print(df.nlargest(3, "runs"))

    section("2️⃣  nsmallest(2, 'strike_rate')")
    print(df.nsmallest(2, "strike_rate"))

    section("3️⃣  Ties & multiple columns")
    print(df.nlargest(3, ["matches", "runs"]))
    print("\nkeep='all' keeps every tied row:")
    print(df.nlargest(1, "matches", keep="all")[["player", "matches"]])
    print("\nOn a Series:", df.set_index("player")["runs"].nlargest(2).to_dict())


def where_demo(df: pd.DataFrame) -> None:
    """where keeps the shape, replacing values that fail the condition."""
    section("4️⃣  where() on a column")
    print(df["runs"].where(df["runs"] >= 500).tolist(), "<- NaN where runs < 500")
    print(df["runs"].where(df["runs"] >= 500, other=0).tolist(), "<- replaced by 0")

    section("5️⃣  where() on a whole DataFrame")
    numeric = df[["runs", "strike_rate"]]
    print(numeric.where(numeric > 150, "-"))


def query_demo(df: pd.DataFrame) -> None:
    """Readable filtering with query strings."""
    section("6️⃣  query()")
    print(df.query("runs > 500"))
    print(df.query("team == 'MI' and strike_rate > 145"))
    print(df.query("team in ['CSK', 'DC']"))
    min_runs = 600
    print("Using a Python variable with @min_runs:")
    print(df.query("runs >= @min_runs")[["player", "runs"]])
    print(df.query("runs / matches > 40")[["player", "runs", "matches"]])


def classify(row: pd.Series) -> str:
    """Label a player from runs and strike rate."""
    if row["runs"] >= 600 and row["strike_rate"] >= 150:
        return "Star"
    if row["runs"] >= 400:
        return "Consistent"
    return "Developing"


def apply_demo(df: pd.DataFrame) -> None:
    """apply on a column, across columns, and across rows."""
    section("7️⃣  apply() on one column (Series)")
    print(df["player"].apply(str.upper).tolist())

    section("8️⃣  apply() on each column (axis=0)")
    print(df[["runs", "strike_rate"]].apply(lambda col: col.max() - col.min()))

    section("9️⃣  apply() on each row (axis=1)")
    out = df.copy()
    out["average"] = out.apply(lambda r: round(r["runs"] / r["matches"], 1), axis=1)
    out["category"] = out.apply(classify, axis=1)
    print(out[["player", "runs", "average", "category"]])

    section("🔟  Putting it together")
    result = (out.query("team == 'MI'")
                 .nlargest(2, "average")[["player", "average", "category"]])
    print("Top 2 MI players by average:\n", result)


if __name__ == "__main__":
    data = make_df()
    top_bottom(data)
    where_demo(data)
    query_demo(data)
    apply_demo(data)
