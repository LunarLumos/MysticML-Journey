"""
03_model_specification_and_diagnostics.py
=========================================
Week 4 · Module 2 – Regression Problem Analysis & Model Specification

"Model specification" = deciding WHICH variables (and which transformations)
go into the regression equation. We compare three specifications on the
learner's Polynomial_Regression/house_prices_multiple.csv (100 houses):

    Spec A:  Price ~ Area
    Spec B:  Price ~ Area + Bedrooms + Age
    Spec C:  Price ~ Area + Area² + Bedrooms + Age

For each we report train/test R², test MSE, adjusted R² and AIC, and we
check the key linear-regression ASSUMPTIONS with residual diagnostics:
    1. Linearity             – residuals vs fitted show no pattern
    2. Independence          – (by design of the data collection)
    3. Homoscedasticity      – residual spread is constant
    4. Normality of residuals – Shapiro-Wilk test / histogram
    5. No multicollinearity  – Variance Inflation Factor (VIF) < ~5–10

Run:
    python 03_model_specification_and_diagnostics.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Polynomial_Regression" / "house_prices_multiple.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add engineered columns used by some specifications."""
    df = df.copy()
    # Centre Area before squaring: raw Area² (~10^7) is almost perfectly correlated
    # with Area and makes the least-squares problem numerically ill-conditioned.
    df["Area2"] = (df["Area"] - df["Area"].mean()) ** 2
    return df


SPECS = {
    "A: Area": ["Area"],
    "B: Area+Bedrooms+Age": ["Area", "Bedrooms", "Age"],
    "C: B + (Area−mean)²": ["Area", "Area2", "Bedrooms", "Age"],
}


def aic(n: int, ss_res: float, k: int) -> float:
    """Akaike Information Criterion for OLS (lower is better)."""
    return n * np.log(ss_res / n) + 2 * k


def vif(df: pd.DataFrame) -> pd.Series:
    """Variance Inflation Factor: regress each feature on the others."""
    out = {}
    for col in df.columns:
        others = df.drop(columns=col)
        r2 = LinearRegression().fit(others, df[col]).score(others, df[col])
        out[col] = 1 / (1 - r2) if r2 < 1 else np.inf
    return pd.Series(out)


def main() -> None:
    """Compare specifications and run residual diagnostics on the best one."""
    data = add_features(pd.read_csv(DATA_PATH).dropna())
    print(f"[*] Loaded {len(data)} rows from {DATA_PATH.parent.name}/{DATA_PATH.name}")
    print("\n[*] Correlation with Price (first look at the problem):")
    print(data[["Area", "Bedrooms", "Age", "Price"]].corr()["Price"].round(3))

    train, test = train_test_split(data, test_size=0.25, random_state=42)
    print(f"\n{'Specification':<24}{'R² train':>9}{'R² test':>9}{'Adj R²':>9}"
          f"{'Test MSE':>18}{'AIC':>10}")
    print("-" * 79)
    best = None
    for name, cols in SPECS.items():
        model = LinearRegression().fit(train[cols], train["Price"])
        pred_tr = model.predict(train[cols])
        pred_te = model.predict(test[cols])
        n, k = len(train), len(cols) + 1
        r2_tr = r2_score(train["Price"], pred_tr)
        adj = 1 - (1 - r2_tr) * (n - 1) / (n - k)
        ss_res = np.sum((train["Price"] - pred_tr) ** 2)
        score = aic(n, ss_res, k)
        print(f"{name:<24}{r2_tr:>9.3f}{r2_score(test['Price'], pred_te):>9.3f}"
              f"{adj:>9.3f}{mean_squared_error(test['Price'], pred_te):>18,.0f}{score:>10.1f}")
        if best is None or score < best[2]:
            best = (name, cols, score, model)

    name, cols, _, model = best
    print(f"\n[*] Best specification by AIC: {name}")

    # --- Diagnostics on the chosen model (full data) ---
    fitted = model.predict(data[cols])
    resid = data["Price"] - fitted
    shapiro_p = stats.shapiro(resid).pvalue
    print(f"[+] Shapiro-Wilk normality test on residuals: p = {shapiro_p:.3f} "
          f"({'looks normal' if shapiro_p > 0.05 else 'not normal'})")
    print("[+] VIF (multicollinearity) for spec B features:")
    print(vif(data[["Area", "Bedrooms", "Age"]]).round(2).to_string())
    print("    (An UN-centred Area² would have a huge VIF – centring fixes that.)")

    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.scatter(fitted, resid, s=15)
    ax1.axhline(0, color="red")
    ax1.set(xlabel="Fitted price", ylabel="Residual",
            title="Residuals vs fitted (want: no pattern)")
    ax2.hist(resid, bins=20, edgecolor="black")
    ax2.set(xlabel="Residual", title="Residual distribution (want: bell shape)")
    fig.tight_layout()
    out = OUTPUT_DIR / "regression_diagnostics.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"[*] Diagnostic plots saved to: {out}")


if __name__ == "__main__":
    main()
