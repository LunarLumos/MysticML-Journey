"""
Module 2 - Cost (Loss) Functions
================================
A cost function measures HOW WRONG the network is. Training = making it small.

    MSE  (Mean Squared Error)          -> regression
    BCE  (Binary Cross-Entropy)        -> binary classification (sigmoid output)
    CCE  (Categorical Cross-Entropy)   -> multi-class (softmax output)

We implement each in NumPy, check them against Keras' built-in versions,
and plot how the loss grows as a prediction gets worse.

Run:
    python 04_cost_functions.py
"""

import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
EPS = 1e-7


# ---------------------------------------------------------------------------
# NumPy implementations
# ---------------------------------------------------------------------------
def mse(y_true, y_pred):
    """mean( (y - ŷ)^2 )  - big errors are punished quadratically."""
    return np.mean((y_true - y_pred) ** 2)


def binary_cross_entropy(y_true, p):
    """-mean( y log p + (1-y) log(1-p) )  - confident & wrong = huge loss."""
    p = np.clip(p, EPS, 1 - EPS)
    return -np.mean(y_true * np.log(p) + (1 - y_true) * np.log(1 - p))


def categorical_cross_entropy(y_onehot, probs):
    """-mean( sum_k y_k log p_k )  - only the prob. of the TRUE class matters."""
    probs = np.clip(probs, EPS, 1.0)
    return -np.mean(np.sum(y_onehot * np.log(probs), axis=1))


def compare_with_keras():
    """Compute each loss by hand and with Keras - they should match."""
    y_reg, pred_reg = np.array([3.0, -0.5, 2.0, 7.0]), np.array([2.5, 0.0, 2.0, 8.0])
    y_bin, p_bin = np.array([1.0, 0.0, 1.0, 0.0]), np.array([0.9, 0.2, 0.6, 0.4])
    y_cat = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
    p_cat = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.3, 0.3, 0.4]])

    ours = [mse(y_reg, pred_reg),
            binary_cross_entropy(y_bin, p_bin),
            categorical_cross_entropy(y_cat, p_cat)]
    print(f"{'Loss':<28}{'NumPy':>10}{'Keras':>10}")
    try:
        from tensorflow import keras
        theirs = [
            float(keras.losses.MeanSquaredError()(y_reg, pred_reg)),
            float(keras.losses.BinaryCrossentropy()(y_bin, p_bin)),
            float(keras.losses.CategoricalCrossentropy()(y_cat, p_cat)),
        ]
    except ImportError:
        theirs = [float("nan")] * 3
        print("(TensorFlow not installed - showing NumPy values only)")
    names = ["MSE", "Binary Cross-Entropy", "Categorical Cross-Entropy"]
    for n, a, b in zip(names, ours, theirs):
        print(f"{n:<28}{a:>10.4f}{b:>10.4f}")
    print()


def plot_losses():
    """Plot loss vs prediction for a sample whose true label is 1."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    p = np.linspace(0.01, 0.99, 200)
    plt.figure(figsize=(7, 4.5))
    plt.plot(p, (1 - p) ** 2, label="MSE  (y=1)")
    plt.plot(p, -np.log(p), label="Cross-entropy  (y=1)")
    plt.xlabel("predicted probability for the true class")
    plt.ylabel("loss")
    plt.title("Cross-entropy punishes confident mistakes much harder")
    plt.legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "cost_functions.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"Saved plot -> {out}")


if __name__ == "__main__":
    compare_with_keras()
    print("Which loss when?")
    print("  regression (predict a number)       -> 'mse' (or 'mae')")
    print("  binary classification, sigmoid out  -> 'binary_crossentropy'")
    print("  multi-class, one-hot labels         -> 'categorical_crossentropy'")
    print("  multi-class, integer labels         -> 'sparse_categorical_crossentropy'\n")
    plot_losses()
