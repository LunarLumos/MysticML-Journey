"""
salary_prediction.py
====================
Week 4 · Module 2 – Project: Employee Salary Prediction

Pipeline
--------
1. Load data/employee_salary.csv (synthetic – see generate_data.py)
2. EDA: shape, missing values, correlation of experience with salary
3. Model 1 – SIMPLE linear regression:   Salary ~ YearsExperience
4. Model 2 – MULTIPLE linear regression: Salary ~ Experience + Education + Department + Age
             (categorical columns one-hot encoded inside a Pipeline)
5. Evaluate both on a held-out test set: MAE, MSE, RMSE, R²
6. Regression-table style coefficients for model 2 (with p-values via statsmodels
   if installed)
7. Predict salaries for new employees + save plots to outputs/

Run:
    python salary_prediction.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "employee_salary.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

NUMERIC = ["YearsExperience", "Age"]
CATEGORICAL = ["EducationLevel", "Department"]
TARGET = "Salary"


def load_data() -> pd.DataFrame:
    """Load the CSV, (re)generating it if it is missing."""
    if not DATA_PATH.exists():
        from generate_data import generate
        DATA_PATH.parent.mkdir(exist_ok=True)
        generate().to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)


def report(name: str, y_true, y_pred) -> dict:
    """Print and return regression metrics."""
    mse = mean_squared_error(y_true, y_pred)
    metrics = {"MAE": mean_absolute_error(y_true, y_pred), "MSE": mse,
               "RMSE": np.sqrt(mse), "R2": r2_score(y_true, y_pred)}
    print(f"[+] {name:<34} MAE=${metrics['MAE']:>8,.0f}  RMSE=${metrics['RMSE']:>8,.0f}"
          f"  R²={metrics['R2']:.3f}")
    return metrics


def build_multiple_model() -> Pipeline:
    """One-hot encode categoricals, pass numerics through, then OLS."""
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(drop="first"), CATEGORICAL),  # drop 1 level → no dummy trap
        ("num", "passthrough", NUMERIC),
    ])
    return Pipeline([("prep", pre), ("ols", LinearRegression())])


def print_significance(X_train: pd.DataFrame, y_train: pd.Series) -> None:
    """Show p-values for model 2's coefficients (requires statsmodels)."""
    try:
        import statsmodels.api as sm
    except ImportError:
        print("[!] statsmodels not installed – skipping p-values.")
        return
    X_enc = pd.get_dummies(X_train, columns=CATEGORICAL, drop_first=True, dtype=float)
    ols = sm.OLS(y_train, sm.add_constant(X_enc)).fit()
    table = pd.DataFrame({"coef": ols.params, "std err": ols.bse,
                          "t": ols.tvalues, "P>|t|": ols.pvalues})
    print("\n[*] Regression table for model 2 (statsmodels OLS):")
    with pd.option_context("display.float_format", "{:,.3f}".format):
        print(table)
    weak = table.index[table["P>|t|"] > 0.05].tolist()
    if weak:
        print(f"    → Not significant at 5%: {weak} – once experience is known, "
              "they add little.")


def main() -> None:
    """Run the full salary-prediction project."""
    df = load_data()
    print("=" * 70)
    print("Employee Salary Prediction")
    print("=" * 70)
    print(f"[*] Rows: {len(df)} | Missing values: {int(df.isnull().sum().sum())}")
    print(f"[*] Salary range: ${df[TARGET].min():,} – ${df[TARGET].max():,}")
    print(f"[*] Corr(YearsExperience, Salary) = "
          f"{df['YearsExperience'].corr(df[TARGET]):.3f}")
    print("[*] Mean salary by education:")
    print(df.groupby("EducationLevel")[TARGET].mean().round(0).to_string())

    X = df[NUMERIC + CATEGORICAL]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    print("\n[*] Test-set performance")
    simple = LinearRegression().fit(X_train[["YearsExperience"]], y_train)
    report("Model 1: simple (experience only)", y_test,
           simple.predict(X_test[["YearsExperience"]]))
    multiple = build_multiple_model().fit(X_train, y_train)
    report("Model 2: multiple (all features)", y_test, multiple.predict(X_test))

    print(f"\n[*] Model 1 equation: Salary = {simple.intercept_:,.0f} + "
          f"{simple.coef_[0]:,.0f} × YearsExperience")
    print_significance(X_train, y_train)

    new_staff = pd.DataFrame({
        "YearsExperience": [1.0, 5.0, 12.0],
        "Age": [23, 29, 38],
        "EducationLevel": ["Bachelor", "Master", "PhD"],
        "Department": ["HR", "Engineering", "Sales"],
    })
    new_staff["PredictedSalary"] = multiple.predict(new_staff).round(-2)
    print("\n[*] Predictions for new employees:")
    print(new_staff.to_string(index=False))

    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.scatter(df["YearsExperience"], y, s=10, alpha=0.6)
    xs = np.linspace(0, 20, 50).reshape(-1, 1)
    ax1.plot(xs, simple.predict(pd.DataFrame(xs, columns=["YearsExperience"])),
             color="red", label="Model 1 fit")
    ax1.set(xlabel="Years of experience", ylabel="Salary ($)", title="Salary vs experience")
    ax1.legend()
    pred = multiple.predict(X_test)
    ax2.scatter(y_test, pred, s=12)
    lims = [y.min(), y.max()]
    ax2.plot(lims, lims, "r--", label="perfect prediction")
    ax2.set(xlabel="Actual salary", ylabel="Predicted salary", title="Model 2: actual vs predicted")
    ax2.legend()
    fig.tight_layout()
    out = OUTPUT_DIR / "salary_prediction.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"\n[*] Plots saved to: {out}")


if __name__ == "__main__":
    main()
