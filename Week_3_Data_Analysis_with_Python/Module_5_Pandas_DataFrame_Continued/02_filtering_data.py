"""
Module 5 · Script 02 – Filtering Data & Filtering Based on a Condition
=====================================================================

Covers: boolean masks, comparison operators, isin(), between(),
string conditions (.str.contains/startswith), null checks, ~ (NOT),
filter() on labels, and counting/using the filtered results.
"""

import numpy as np
import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """A small movie table."""
    return pd.DataFrame({
        "title": ["Inception", "Dangal", "Parasite", "Interstellar", "3 Idiots",
                  "Coco", "Joker", "RRR"],
        "genre": ["Sci-Fi", "Drama", "Thriller", "Sci-Fi", "Comedy",
                  "Animation", "Drama", "Action"],
        "year": [2010, 2016, 2019, 2014, 2009, 2017, 2019, 2022],
        "rating": [8.8, 8.3, 8.5, 8.7, 8.4, 8.4, 8.4, 7.8],
        "box_office_m": [836, 311, 262, 701, 90, 814, 1079, np.nan],
    })


def main() -> None:
    """Walk through the different ways of filtering rows."""
    df = make_df()
    section("Original")
    print(df)

    section("1️⃣  What is a boolean mask?")
    mask = df["rating"] > 8.4
    print(mask.tolist())
    print("df[mask]:\n", df[mask])

    section("2️⃣  Filtering based on a condition (==, !=, >, <=)")
    print("Drama movies:\n", df[df["genre"] == "Drama"])
    print("\nNot Sci-Fi:\n", df[df["genre"] != "Sci-Fi"][["title", "genre"]])
    print("\nReleased before 2015:\n", df[df["year"] < 2015][["title", "year"]])

    section("3️⃣  isin() – value in a list")
    print(df[df["genre"].isin(["Sci-Fi", "Animation"])][["title", "genre"]])

    section("4️⃣  between() – inclusive range")
    print(df[df["year"].between(2014, 2019)][["title", "year"]])

    section("5️⃣  String conditions")
    print("title contains 'in' (case-insensitive):\n",
          df[df["title"].str.contains("in", case=False)][["title"]])
    print("\ntitle starts with a digit:\n", df[df["title"].str.match(r"^\d")][["title"]])

    section("6️⃣  Null checks and NOT (~)")
    print("box office missing:\n", df[df["box_office_m"].isna()][["title"]])
    print("\nNOT Drama (~):\n", df[~(df["genre"] == "Drama")][["title", "genre"]])

    section("7️⃣  Filtering then selecting columns with loc")
    print(df.loc[df["rating"] >= 8.5, ["title", "rating"]])

    section("8️⃣  Using the result")
    hits = df[df["box_office_m"] > 500]
    print(f"{len(hits)} movies earned > $500M; average rating {hits['rating'].mean():.2f}")
    print("Top-rated title:", df.loc[df["rating"].idxmax(), "title"])

    section("9️⃣  filter() works on LABELS, not values")
    print(df.filter(items=["title", "year"]).head(3))


if __name__ == "__main__":
    main()
