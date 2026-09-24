"""
Module 2 - Activation Functions
===============================
Implements and plots the most common activation functions AND their
derivatives (the derivative is what backpropagation uses):

    sigmoid, tanh, ReLU, Leaky ReLU, softmax

Why do we need them?  Without a non-linear activation, stacking layers
is pointless: many linear layers collapse into ONE linear layer.

Run:
    python 02_activation_functions.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


# ---------------------------------------------------------------------------
# Activation functions + derivatives
# ---------------------------------------------------------------------------
def sigmoid(z):
    """1 / (1 + e^-z): output in (0, 1). Used for binary outputs."""
    return 1 / (1 + np.exp(-z))


def sigmoid_grad(z):
    s = sigmoid(z)
    return s * (1 - s)                    # max 0.25 -> causes vanishing gradients


def tanh(z):
    """Output in (-1, 1), zero-centred."""
    return np.tanh(z)


def tanh_grad(z):
    return 1 - np.tanh(z) ** 2


def relu(z):
    """max(0, z): the default choice for hidden layers."""
    return np.maximum(0, z)


def relu_grad(z):
    return (z > 0).astype(float)


def leaky_relu(z, alpha=0.1):
    """Like ReLU but lets a small gradient through for z < 0 (no 'dead' neurons)."""
    return np.where(z > 0, z, alpha * z)


def leaky_relu_grad(z, alpha=0.1):
    return np.where(z > 0, 1.0, alpha)


def softmax(z):
    """Turn a vector of scores into probabilities that sum to 1 (multi-class output)."""
    e = np.exp(z - np.max(z))             # subtract max for numerical stability
    return e / e.sum()


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
def plot_activations():
    """Plot each activation (solid) and its derivative (dashed)."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    z = np.linspace(-5, 5, 400)
    funcs = [
        ("Sigmoid", sigmoid, sigmoid_grad),
        ("Tanh", tanh, tanh_grad),
        ("ReLU", relu, relu_grad),
        ("Leaky ReLU (α=0.1)", leaky_relu, leaky_relu_grad),
    ]
    fig, axes = plt.subplots(1, 5, figsize=(22, 4))
    for ax, (name, f, df) in zip(axes, funcs):
        ax.plot(z, f(z), label="f(z)", lw=2)
        ax.plot(z, df(z), "--", label="f'(z)")
        ax.axhline(0, color="gray", lw=0.5)
        ax.axvline(0, color="gray", lw=0.5)
        ax.set_title(name)
        ax.legend()

    # Softmax works on a VECTOR, so show it as a bar chart
    scores = np.array([2.0, 1.0, 0.1, -1.0])
    probs = softmax(scores)
    axes[4].bar(["cat", "dog", "bird", "fish"], probs, color="tab:purple")
    axes[4].set_title(f"Softmax of scores {scores.tolist()}")
    axes[4].set_ylabel("probability")
    plt.tight_layout()
    out = OUTPUT_DIR / "activation_functions.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"Saved plot -> {out}")


def print_summary():
    """Print a small table of values and a usage guide."""
    zs = np.array([-2.0, 0.0, 2.0])
    print(f"{'z':>6} | {'sigmoid':>8} | {'tanh':>7} | {'relu':>5} | {'leaky':>6}")
    for z in zs:
        print(f"{z:>6.1f} | {sigmoid(z):>8.3f} | {tanh(z):>7.3f} | "
              f"{relu(z):>5.1f} | {leaky_relu(z):>6.2f}")
    s = softmax(np.array([2.0, 1.0, 0.1, -1.0]))
    print(f"\nsoftmax([2, 1, 0.1, -1]) = {np.round(s, 3)}  (sum = {s.sum():.1f})")
    print("\nRule of thumb:")
    print("  hidden layers        -> ReLU (or Leaky ReLU)")
    print("  binary output        -> sigmoid")
    print("  multi-class output   -> softmax")
    print("  regression output    -> none (linear)")
    print("  RNN/LSTM internals   -> tanh + sigmoid gates\n")


if __name__ == "__main__":
    print_summary()
    plot_activations()
