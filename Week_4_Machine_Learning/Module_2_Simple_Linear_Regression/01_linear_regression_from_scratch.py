"""
01_linear_regression_from_scratch.py
====================================
Week 4 · Module 2 – Mathematical modelling of a Regression Model

We fit   ŷ = β0 + β1·x   to the learner's own house-price data
(Single_Linear_Regression/house_prices.csv) in THREE ways:

  1. Closed-form ordinary least squares (OLS) with the classic formulas
         β1 = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)²        β0 = ȳ − β1·x̄
  2. Gradient descent – iteratively minimising the MSE cost
         J(β0, β1) = (1/n) Σ (ŷ − y)²
  3. scikit-learn's LinearRegression (to check our answers)

Then we compute R² and MSE by hand.

Run:
    python 01_linear_regression_from_scratch.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Single_Linear_Regression" / "house_prices.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


# ---------------------------------------------------------------
# 1. Ordinary Least Squares (closed form)
# ---------------------------------------------------------------
def fit_least_squares(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Return (intercept, slope) using the textbook OLS formulas."""
    x_mean, y_mean = x.mean(), y.mean()
    slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    intercept = y_mean - slope * x_mean
    return intercept, slope


# ---------------------------------------------------------------
# 2. Gradient descent
# ---------------------------------------------------------------
def fit_gradient_descent(x: np.ndarray, y: np.ndarray, lr: float = 0.1,
                         epochs: int = 5000) -> tuple[float, float, list[float]]:
    """Fit the line with batch gradient descent.

    Features and target are STANDARDISED first (mean 0, std 1) so a single
    learning rate works well; the parameters are converted back at the end.
    """
    x_mu, x_sd = x.mean(), x.std()
    y_mu, y_sd = y.mean(), y.std()
    xs, ys = (x - x_mu) / x_sd, (y - y_mu) / y_sd

    b0, b1, n = 0.0, 0.0, len(xs)
    history = []
    for _ in range(epochs):
        y_hat = b0 + b1 * xs
        error = y_hat - ys
        # Partial derivatives of J = (1/n) Σ error²
        grad_b0 = (2 / n) * np.sum(error)
        grad_b1 = (2 / n) * np.sum(error * xs)
        b0 -= lr * grad_b0
        b1 -= lr * grad_b1
        history.append(np.mean(error ** 2))

    # Undo the scaling:  y = y_mu + y_sd * (b0 + b1 * (x - x_mu) / x_sd)
    slope = b1 * y_sd / x_sd
    intercept = y_mu + y_sd * b0 - slope * x_mu
    return intercept, slope, history


# ---------------------------------------------------------------
# 3. Metrics by hand
# ---------------------------------------------------------------
def mse(y: np.ndarray, y_hat: np.ndarray) -> float:
    """Mean Squared Error = average of squared residuals."""
    return float(np.mean((y - y_hat) ** 2))


def r_squared(y: np.ndarray, y_hat: np.ndarray) -> float:
    """R² = 1 − SS_res / SS_tot  (share of variance explained by the model)."""
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return float(1 - ss_res / ss_tot)


def main() -> None:
    """Fit the line three ways, compare, and plot."""
    data = pd.read_csv(DATA_PATH)
    x, y = data["Area"].to_numpy(float), data["Price"].to_numpy(float)
    print(f"[*] Loaded {len(data)} houses from {DATA_PATH.name}\n")

    b0_ols, b1_ols = fit_least_squares(x, y)
    b0_gd, b1_gd, history = fit_gradient_descent(x, y)
    sk = LinearRegression().fit(x.reshape(-1, 1), y)

    print(f"{'Method':<22}{'Intercept β0':>16}{'Slope β1':>12}")
    print("-" * 50)
    print(f"{'Least squares (OLS)':<22}{b0_ols:>16,.2f}{b1_ols:>12.4f}")
    print(f"{'Gradient descent':<22}{b0_gd:>16,.2f}{b1_gd:>12.4f}")
    print(f"{'scikit-learn':<22}{sk.intercept_:>16,.2f}{sk.coef_[0]:>12.4f}")

    y_hat = b0_ols + b1_ols * x
    print(f"\n[+] MSE  = {mse(y, y_hat):,.2f}")
    print(f"[+] RMSE = {np.sqrt(mse(y, y_hat)):,.2f}  (same units as price)")
    print(f"[+] R²   = {r_squared(y, y_hat):.4f}")
    print(f"\n[*] Interpretation: every extra sq. ft. adds about ${b1_ols:,.2f} to the price.")
    print(f"[*] Prediction for 1900 sq. ft.: ${b0_ols + b1_ols * 1900:,.2f}")

    # --- Plots: fitted line + gradient-descent learning curve ---
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.scatter(x, y, label="data")
    xs = np.linspace(x.min(), x.max(), 50)
    ax1.plot(xs, b0_ols + b1_ols * xs, color="red", label="OLS line")
    ax1.set(xlabel="Area (sq. ft.)", ylabel="Price", title="Least-squares fit")
    ax1.legend()
    ax2.plot(history[:300])
    ax2.set(xlabel="Epoch", ylabel="MSE (standardised units)",
            title="Gradient descent: cost going down")
    fig.tight_layout()
    out = OUTPUT_DIR / "linear_regression_from_scratch.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"[*] Plot saved to: {out}")


if __name__ == "__main__":
    main()
