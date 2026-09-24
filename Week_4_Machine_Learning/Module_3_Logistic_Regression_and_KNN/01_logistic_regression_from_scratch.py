"""
01_logistic_regression_from_scratch.py
======================================
Week 4 · Module 3 – Logistic Regression: Working and Mathematical Equation

Logistic regression predicts the PROBABILITY that y = 1:

    z      = β0 + β1·x1 + ... + βn·xn        (a linear score, called the logit)
    σ(z)   = 1 / (1 + e^(−z))                 (sigmoid squashes z into 0..1)
    ŷ      = 1 if σ(z) ≥ 0.5 else 0

It is trained by minimising the LOG-LOSS (binary cross-entropy):

    J(β) = −(1/n) Σ [ y·log(p) + (1 − y)·log(1 − p) ]

whose gradient is beautifully simple:   ∂J/∂β = (1/n) Xᵀ (p − y)

We implement this with NumPy gradient descent on the breast-cancer dataset and
compare with scikit-learn.

Run:
    python 01_logistic_regression_from_scratch.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def sigmoid(z: np.ndarray) -> np.ndarray:
    """The logistic (sigmoid) function."""
    return 1 / (1 + np.exp(-z))


def binary_log_loss(y: np.ndarray, p: np.ndarray, eps: float = 1e-12) -> float:
    """Binary cross-entropy; eps avoids log(0)."""
    p = np.clip(p, eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


class LogisticRegressionScratch:
    """Minimal logistic regression trained with batch gradient descent."""

    def __init__(self, lr: float = 0.1, epochs: int = 2000):
        self.lr = lr
        self.epochs = epochs
        self.weights: np.ndarray | None = None
        self.bias = 0.0
        self.loss_history: list[float] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegressionScratch":
        """Learn weights and bias from training data."""
        n, d = X.shape
        self.weights = np.zeros(d)
        for _ in range(self.epochs):
            p = sigmoid(X @ self.weights + self.bias)
            error = p - y                     # (p − y)
            self.weights -= self.lr * (X.T @ error) / n
            self.bias -= self.lr * error.mean()
            self.loss_history.append(binary_log_loss(y, p))
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Probability of the positive class."""
        return sigmoid(X @ self.weights + self.bias)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """Hard 0/1 predictions."""
        return (self.predict_proba(X) >= threshold).astype(int)


def main() -> None:
    """Train scratch vs sklearn logistic regression and compare."""
    # --- Sigmoid intuition ---
    print("[*] Sigmoid values:  z → σ(z)")
    for z in (-6, -2, 0, 2, 6):
        print(f"    {z:>3} → {sigmoid(np.array(z)):.4f}")

    # --- Data (1 = benign, 0 = malignant) ---
    X, y = load_breast_cancer(return_X_y=True)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y,
                                              random_state=42)
    scaler = StandardScaler().fit(X_tr)          # gradient descent needs scaled features
    X_tr, X_te = scaler.transform(X_tr), scaler.transform(X_te)

    scratch = LogisticRegressionScratch(lr=0.1, epochs=2000).fit(X_tr, y_tr)
    sk = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)

    print("\n" + "=" * 60)
    print(f"{'Model':<22}{'Test accuracy':>15}{'Test log-loss':>15}")
    print("-" * 60)
    for name, model in (("From scratch (NumPy)", scratch), ("scikit-learn", sk)):
        proba = model.predict_proba(X_te)
        proba = proba[:, 1] if proba.ndim == 2 else proba
        print(f"{name:<22}{accuracy_score(y_te, model.predict(X_te)):>15.3f}"
              f"{log_loss(y_te, proba):>15.4f}")

    # --- Interpret coefficients as odds ratios ---
    names = load_breast_cancer().feature_names
    top = np.argsort(np.abs(scratch.weights))[::-1][:3]
    print("\n[*] Top-3 most influential (scaled) features in the scratch model:")
    for i in top:
        print(f"    {names[i]:<24} β={scratch.weights[i]:+.3f}  "
              f"odds ×{np.exp(scratch.weights[i]):.2f} per +1 std")

    # --- Plots ---
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    zs = np.linspace(-8, 8, 200)
    ax1.plot(zs, sigmoid(zs))
    ax1.axhline(0.5, ls="--", color="grey")
    ax1.set(title="Sigmoid function", xlabel="z", ylabel="σ(z)")
    ax2.plot(scratch.loss_history)
    ax2.set(title="Training log-loss (gradient descent)", xlabel="epoch", ylabel="loss")
    fig.tight_layout()
    out = OUTPUT_DIR / "logistic_from_scratch.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"\n[*] Plot saved to: {out}")


if __name__ == "__main__":
    main()
