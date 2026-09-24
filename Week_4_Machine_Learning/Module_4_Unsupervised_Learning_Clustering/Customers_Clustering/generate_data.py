"""
generate_data.py
================
Creates the SYNTHETIC mall-customers dataset data/customers.csv (seeded).

It mimics the well-known "Mall Customer Segmentation" layout:
    CustomerID, Gender, Age, AnnualIncome_k, SpendingScore (1–100)

Five hidden customer groups are simulated (the clustering script must
re-discover them WITHOUT being told):
    careful high-earners, big spenders, average, young impulsive, thrifty

Run:
    python generate_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUT_PATH = BASE_DIR / "data" / "customers.csv"

# (count, age mean, income mean (k$), spending-score mean)
SEGMENTS = [
    (40, 42, 88, 18),   # careful high earners
    (40, 32, 86, 82),   # rich big spenders
    (80, 45, 55, 50),   # average customers
    (22, 25, 25, 79),   # young impulsive, low income
    (18, 46, 26, 20),   # thrifty, low income
]


def generate(seed: int = 7) -> pd.DataFrame:
    """Return the synthetic customer DataFrame (200 rows)."""
    rng = np.random.default_rng(seed)
    rows = []
    for count, age, income, score in SEGMENTS:
        rows.append(np.column_stack([
            rng.normal(age, 7, count),
            rng.normal(income, 8, count),
            rng.normal(score, 8, count),
        ]))
    data = np.vstack(rows)
    rng.shuffle(data)
    n = len(data)
    return pd.DataFrame({
        "CustomerID": np.arange(1, n + 1),
        "Gender": rng.choice(["Female", "Male"], size=n, p=[0.56, 0.44]),
        "Age": np.clip(data[:, 0].round(), 18, 70).astype(int),
        "AnnualIncome_k": np.clip(data[:, 1].round(), 15, 140).astype(int),
        "SpendingScore": np.clip(data[:, 2].round(), 1, 100).astype(int),
    })


def main() -> None:
    """Generate and save the CSV."""
    df = generate()
    OUT_PATH.parent.mkdir(exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"[*] Wrote {len(df)} rows to {OUT_PATH}")
    print(df.head())


if __name__ == "__main__":
    main()
