"""
02_regression_table_statsmodels_or_manual.py
============================================
Week 4 · Module 2 – Regression Table, R-Square, Mean Squared Error

A "regression table" tells you, for every coefficient:
    coef     – the estimated effect
    std err  – how uncertain that estimate is
    t        – coef / std err   (how many std errors away from 0)
    P>|t|    – probability of seeing such a t if the true coef were 0
    [0.025, 0.975] – 95% confidence interval

We build it MANUALLY with NumPy + SciPy (so you see every formula) and, if
statsmodels is installed, print statsmodels' OLS summary for comparison.

Data: the learner's Multiple_Linear_Regression/house_prices_multiple.csv
      (Price ~ Area + Bedrooms + Age)

Run:
    python 02_regression_table_statsmodels_or_manual.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Multiple_Linear_Regression" / "house_prices_multiple.csv"
FEATURES = ["Area", "Bedrooms", "Age"]
TARGET = "Price"


def manual_regression_table(X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    """Compute an OLS regression table with matrix algebra.

    β̂ = (XᵀX)⁻¹ Xᵀy
    σ̂² = SS_res / (n − p)            (p = number of parameters incl. intercept)
    Var(β̂) = σ̂² (XᵀX)⁻¹              → std err = sqrt(diagonal)
    """
    X_mat = np.column_stack([np.ones(len(X)), X.to_numpy(float)])  # add intercept column
    y_vec = y.to_numpy(float)
    n, p = X_mat.shape

    xtx_inv = np.linalg.inv(X_mat.T @ X_mat)
    beta = xtx_inv @ X_mat.T @ y_vec
    residuals = y_vec - X_mat @ beta
    dof = n - p
    sigma2 = residuals @ residuals / dof
    std_err = np.sqrt(np.diag(sigma2 * xtx_inv))
    t_stat = beta / std_err
    p_values = 2 * stats.t.sf(np.abs(t_stat), dof)
    t_crit = stats.t.ppf(0.975, dof)

    table = pd.DataFrame({
        "coef": beta,
        "std err": std_err,
        "t": t_stat,
        "P>|t|": p_values,
        "[0.025": beta - t_crit * std_err,
        "0.975]": beta + t_crit * std_err,
    }, index=["const"] + list(X.columns))

    # --- Model-level statistics ---
    ss_res = residuals @ residuals
    ss_tot = np.sum((y_vec - y_vec.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    adj_r2 = 1 - (1 - r2) * (n - 1) / dof
    k = p - 1
    f_stat = ((ss_tot - ss_res) / k) / (ss_res / dof)
    f_pvalue = stats.f.sf(f_stat, k, dof)
    print(f"[*] Observations: {n}   Parameters: {p}   Residual dof: {dof}")
    print(f"[*] R-squared:      {r2:.4f}")
    print(f"[*] Adj. R-squared: {adj_r2:.4f}   (penalises useless extra features)")
    print(f"[*] MSE (in-sample): {ss_res / n:,.2f}")
    print(f"[*] F-statistic:    {f_stat:.2f}  (p = {f_pvalue:.3g})  "
          "→ is the model better than just predicting the mean?")
    return table


def statsmodels_summary(X: pd.DataFrame, y: pd.Series) -> None:
    """Print statsmodels' OLS summary if the library is available."""
    try:
        import statsmodels.api as sm
    except ImportError:
        print("\n[!] statsmodels not installed – skipping comparison "
              "(pip install statsmodels).")
        return
    model = sm.OLS(y, sm.add_constant(X)).fit()
    print("\n" + "=" * 78)
    print("statsmodels OLS summary (should match the manual table)")
    print("=" * 78)
    print(model.summary())


def main() -> None:
    """Build and interpret the regression table."""
    data = pd.read_csv(DATA_PATH).dropna()
    X, y = data[FEATURES], data[TARGET]

    print("=" * 78)
    print("Manual OLS regression table:  Price ~ Area + Bedrooms + Age")
    print("=" * 78)
    table = manual_regression_table(X, y)
    with pd.option_context("display.float_format", "{:,.4f}".format):
        print(table)

    print("\n[*] How to read it (significance level α = 0.05):")
    for name, row in table.drop(index="const").iterrows():
        verdict = "SIGNIFICANT" if row["P>|t|"] < 0.05 else "not significant"
        print(f"    {name:<9} coef={row['coef']:>12,.2f}  p={row['P>|t|']:.4f}  → {verdict}")

    statsmodels_summary(X, y)


if __name__ == "__main__":
    main()
