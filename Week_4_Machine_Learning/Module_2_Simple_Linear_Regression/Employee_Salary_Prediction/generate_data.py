"""
generate_data.py
================
Creates the SYNTHETIC dataset data/employee_salary.csv (seeded → reproducible).

Columns
-------
EmployeeID       – running id
YearsExperience  – 0–20 years (float, 1 decimal)
EducationLevel   – Bachelor / Master / PhD
Department       – Engineering / Marketing / Sales / HR
Age              – derived from experience + noise
Salary           – yearly salary in USD (the target)

The "true" salary rule used to simulate the data:
    Salary = 32,000 + 4,200·Experience + edu_bonus + dept_bonus + noise(σ = 6,000)

Run:
    python generate_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUT_PATH = BASE_DIR / "data" / "employee_salary.csv"

EDU_BONUS = {"Bachelor": 0, "Master": 7_000, "PhD": 15_000}
DEPT_BONUS = {"HR": 0, "Marketing": 3_000, "Sales": 5_000, "Engineering": 12_000}


def generate(n: int = 250, seed: int = 42) -> pd.DataFrame:
    """Return a synthetic employee salary DataFrame."""
    rng = np.random.default_rng(seed)
    experience = np.round(rng.uniform(0, 20, n), 1)
    education = rng.choice(list(EDU_BONUS), size=n, p=[0.55, 0.35, 0.10])
    department = rng.choice(list(DEPT_BONUS), size=n, p=[0.15, 0.25, 0.25, 0.35])
    age = np.clip(np.round(22 + experience + rng.normal(2, 2.5, n)), 21, 65).astype(int)
    salary = (32_000 + 4_200 * experience
              + np.vectorize(EDU_BONUS.get)(education)
              + np.vectorize(DEPT_BONUS.get)(department)
              + rng.normal(0, 6_000, n))
    return pd.DataFrame({
        "EmployeeID": np.arange(1, n + 1),
        "YearsExperience": experience,
        "EducationLevel": education,
        "Department": department,
        "Age": age,
        "Salary": np.round(salary, -1).astype(int),
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
