"""
04_regression_vs_classification.py
==================================
Week 4 · Module 1 – Regression vs Classification

Same input data, two different QUESTIONS:
  • Regression      : "What will this house SELL for?"        -> a number
  • Classification  : "Is this house EXPENSIVE (above median)?" -> a category

Notice how the model family, the output and the METRIC all change.

Run:
    python 04_regression_vs_classification.py
"""

import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def make_house_data(n: int = 300, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Create a synthetic house dataset: area (sq ft), rooms → price."""
    rng = np.random.default_rng(seed)
    area = rng.uniform(600, 4000, n)
    rooms = rng.integers(1, 6, n)
    price = 50_000 + 120 * area + 15_000 * rooms + rng.normal(0, 25_000, n)
    return np.column_stack([area, rooms]), price


def main() -> None:
    """Solve the regression and the classification version side by side."""
    X, price = make_house_data()
    is_expensive = (price > np.median(price)).astype(int)  # turn number → category

    X_tr, X_te, p_tr, p_te, c_tr, c_te = train_test_split(
        X, price, is_expensive, test_size=0.25, random_state=42)

    # ---------------- Regression ----------------
    reg = LinearRegression().fit(X_tr, p_tr)
    p_pred = reg.predict(X_te)
    print("=" * 60)
    print("REGRESSION  → predict the price (continuous number)")
    print("=" * 60)
    print(f"[+] Example predictions: {np.round(p_pred[:3], -2)}")
    print(f"[+] Mean Absolute Error : ${mean_absolute_error(p_te, p_pred):,.0f}")
    print(f"[+] R² score            : {r2_score(p_te, p_pred):.3f}")

    # ---------------- Classification ----------------
    clf = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_tr, c_tr)
    c_pred = clf.predict(X_te)
    proba = clf.predict_proba(X_te)[:, 1]
    print("\n" + "=" * 60)
    print("CLASSIFICATION → predict expensive? (0 = no, 1 = yes)")
    print("=" * 60)
    print(f"[+] Example predictions   : {c_pred[:3]}")
    print(f"[+] Example probabilities : {np.round(proba[:3], 3)}")
    print(f"[+] Accuracy              : {accuracy_score(c_te, c_pred):.3f}")

    print("\n[*] Summary")
    print(f"    {'':<14}{'Regression':<22}{'Classification'}")
    print(f"    {'Output':<14}{'number (price)':<22}{'class (0/1)'}")
    print(f"    {'Model used':<14}{'LinearRegression':<22}{'LogisticRegression'}")
    print(f"    {'Metrics':<14}{'MAE, MSE, R²':<22}{'accuracy, precision, recall, F1'}")


if __name__ == "__main__":
    main()
