"""
Module 5 - Outliers: detection and handling
===========================================
An outlier is a data point far away from the rest (typo, sensor glitch, or a
genuinely rare event). A few outliers can drag a model badly off course,
especially models trained with squared error (linear regression, MSE nets).

Detection methods:
    1. Z-score          |x - mean| / std > 3
    2. IQR rule         x < Q1 - 1.5*IQR  or  x > Q3 + 1.5*IQR   (box-plot rule)
    3. IsolationForest  ML model that isolates unusual points (works in many dims)

Handling methods (compared by their effect on a linear regression):
    remove | cap / winsorize (clip to IQR fences) | robust model (HuberRegressor)

Data is SYNTHETIC (seeded): y = 3x + 5 + noise, with 8 injected outliers.

Run:
    python 05_outliers.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import HuberRegressor, LinearRegression

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42
TRUE_SLOPE, TRUE_INTERCEPT = 3.0, 5.0


def make_data(n=100, n_outliers=8, seed=SEED):
    """Clean linear data plus a handful of large positive outliers."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, 10, n)
    y = TRUE_SLOPE * x + TRUE_INTERCEPT + rng.normal(0, 2, n)
    idx = rng.choice(np.where(x > 6)[0], n_outliers, replace=False)
    y[idx] += rng.uniform(40, 70, n_outliers)          # corrupt a few targets
    is_outlier = np.zeros(n, dtype=bool)
    is_outlier[idx] = True
    return x, y, is_outlier


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------
def zscore_outliers(values, threshold=3.0):
    z = (values - values.mean()) / values.std()
    return np.abs(z) > threshold


def iqr_bounds(values):
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def iqr_outliers(values):
    lo, hi = iqr_bounds(values)
    return (values < lo) | (values > hi)


def residual_outliers(x, y):
    """Outliers in y should be judged RELATIVE to the trend: use residuals of a robust fit."""
    robust = HuberRegressor().fit(x[:, None], y)
    return iqr_outliers(y - robust.predict(x[:, None]))


def isolation_forest_outliers(x, y, contamination=0.08):
    model = IsolationForest(contamination=contamination, random_state=SEED)
    return model.fit_predict(np.c_[x, y]) == -1        # -1 = outlier


def report(name, found, truth):
    tp = int(np.sum(found & truth))
    print(f"{name:<28} flagged {found.sum():>3} | true outliers caught {tp}/{truth.sum()} "
          f"| false alarms {int(np.sum(found & ~truth))}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    x, y, truth = make_data()

    print("=" * 70)
    print("1. DETECTING OUTLIERS")
    print("=" * 70)
    detections = {
        "Z-score on y (|z|>3)": zscore_outliers(y),
        "IQR on y": iqr_outliers(y),
        "IQR on residuals (robust)": residual_outliers(x, y),
        "IsolationForest on (x, y)": isolation_forest_outliers(x, y),
    }
    for name, found in detections.items():
        report(name, found, truth)
    print("-> Looking at y alone misses outliers hidden inside the normal y-range;")
    print("   judging residuals from the trend (or using a multi-dim model) works better.\n")

    print("=" * 70)
    print("2. HANDLING OUTLIERS - effect on linear regression")
    print("=" * 70)
    flagged = detections["IQR on residuals (robust)"]
    residual_fit = HuberRegressor().fit(x[:, None], y)
    resid = y - residual_fit.predict(x[:, None])
    lo, hi = iqr_bounds(resid)
    y_capped = residual_fit.predict(x[:, None]) + np.clip(resid, lo, hi)

    fits = {
        "Ignore (plain OLS)": LinearRegression().fit(x[:, None], y),
        "Remove flagged points": LinearRegression().fit(x[~flagged, None], y[~flagged]),
        "Cap / winsorize residuals": LinearRegression().fit(x[:, None], y_capped),
        "Robust model (Huber)": residual_fit,
    }
    print(f"{'Strategy':<28}{'slope':>8}{'intercept':>11}   (true 3.00 / 5.00)")
    for name, model in fits.items():
        print(f"{name:<28}{model.coef_[0]:>8.2f}{model.intercept_:>11.2f}")

    # ---- Plots --------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    axes[0].boxplot(y)
    axes[0].set(title="Box plot of y (dots beyond whiskers = IQR outliers)", ylabel="y")
    axes[1].scatter(x[~truth], y[~truth], s=15, label="normal")
    axes[1].scatter(x[truth], y[truth], s=40, c="red", marker="x", label="injected outlier")
    grid = np.linspace(0, 10, 50)
    for name, model in fits.items():
        axes[1].plot(grid, model.predict(grid[:, None]), label=name)
    axes[1].plot(grid, TRUE_SLOPE * grid + TRUE_INTERCEPT, "k:", label="true line")
    axes[1].set(title="Regression lines under each strategy", xlabel="x", ylabel="y")
    axes[1].legend(fontsize=8)
    plt.tight_layout()
    out = OUTPUT_DIR / "outliers.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"\nSaved plot -> {out}")
    print("Remember: don't delete outliers blindly - first ask WHY they exist.")


if __name__ == "__main__":
    main()
