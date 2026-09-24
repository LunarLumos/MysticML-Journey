"""
Module 5 · Script 04 – .set_index() & .reset_index() in Pandas
==============================================================

Covers: making a column the index, keeping the column (drop=False),
multi-column (MultiIndex) indexes, reset_index (back to a column or
dropped), and why a good index makes lookups easy.
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def make_df() -> pd.DataFrame:
    """Country statistics."""
    return pd.DataFrame({
        "code": ["IN", "JP", "FR", "BR", "US"],
        "country": ["India", "Japan", "France", "Brazil", "USA"],
        "continent": ["Asia", "Asia", "Europe", "S. America", "N. America"],
        "population_m": [1428, 124, 68, 216, 335],
        "capital": ["New Delhi", "Tokyo", "Paris", "Brasília", "Washington"],
    })


def main() -> None:
    """set_index / reset_index in all their flavours."""
    df = make_df()
    section("Original – default RangeIndex 0..4")
    print(df)

    section("1️⃣  set_index('code')")
    by_code = df.set_index("code")
    print(by_code)
    print("\nNow lookups by label are easy -> by_code.loc['JP', 'capital'] =",
          by_code.loc["JP", "capital"])

    section("2️⃣  drop=False keeps the column as well")
    print(df.set_index("code", drop=False).head(2))

    section("3️⃣  MultiIndex – set_index(['continent', 'country'])")
    multi = df.set_index(["continent", "country"]).sort_index()
    print(multi)
    print("\nmulti.loc['Asia']:\n", multi.loc["Asia"])

    section("4️⃣  reset_index() – move the index back into a column")
    print(by_code.reset_index())

    section("5️⃣  reset_index(drop=True) – throw the old index away")
    filtered = df[df["population_m"] > 200]
    print("After filtering, index has gaps:", filtered.index.tolist())
    print(filtered.reset_index(drop=True))

    section("6️⃣  Resetting a MultiIndex / after groupby")
    print(multi.reset_index(level="country").head(3))
    totals = df.groupby("continent")["population_m"].sum()
    print("\ngroupby result (continent is the index):\n", totals)
    print("\n.reset_index() -> tidy table:\n", totals.reset_index(name="total_pop_m"))

    section("7️⃣  Naming the index & set_index with inplace")
    renamed = by_code.rename_axis("iso_code")
    print(renamed.head(2))
    df2 = df.copy()
    df2.set_index("country", inplace=True)
    print("index after inplace set_index:", df2.index.tolist())


if __name__ == "__main__":
    main()
