"""
Module 2 - Feed-Forward Network + Backpropagation FROM SCRATCH (NumPy only)
===========================================================================
We solve XOR - the problem a single neuron could not solve - with a
2 -> 4 -> 1 network:

    input (2) --W1,b1--> hidden (4, tanh) --W2,b2--> output (1, sigmoid)

Steps implemented by hand:
  1. Feed forward        : compute predictions layer by layer
  2. Cost function       : binary cross-entropy (BCE)
  3. Back propagation    : chain rule, from output back to input
  4. Gradient descent    : W <- W - lr * dW
  5. Gradient check      : compare our backprop gradients with numerical
                           (finite-difference) gradients to PROVE they are right

Run:
    python 03_ann_from_scratch_xor.py
    python 03_ann_from_scratch_xor.py --epochs 5000 --lr 0.5
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42

# XOR truth table
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
Y = np.array([[0], [1], [1], [0]], dtype=float)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def init_params(n_in=2, n_hidden=4, n_out=1, seed=SEED):
    """Random small weights, zero biases."""
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0, 1, size=(n_in, n_hidden)),
        "b1": np.zeros((1, n_hidden)),
        "W2": rng.normal(0, 1, size=(n_hidden, n_out)),
        "b2": np.zeros((1, n_out)),
    }


# ---------------------------------------------------------------------------
# 1. Feed forward
# ---------------------------------------------------------------------------
def forward(params, X):
    """Return the prediction and a cache of intermediate values for backprop."""
    Z1 = X @ params["W1"] + params["b1"]      # (n, 4)
    A1 = np.tanh(Z1)                          # hidden activations
    Z2 = A1 @ params["W2"] + params["b2"]     # (n, 1)
    A2 = sigmoid(Z2)                          # output probability
    return A2, {"X": X, "Z1": Z1, "A1": A1, "Z2": Z2, "A2": A2}


# ---------------------------------------------------------------------------
# 2. Cost function - Binary Cross-Entropy
# ---------------------------------------------------------------------------
def bce_loss(y_pred, y_true, eps=1e-12):
    """L = -mean( y*log(p) + (1-y)*log(1-p) )"""
    p = np.clip(y_pred, eps, 1 - eps)
    return float(-np.mean(y_true * np.log(p) + (1 - y_true) * np.log(1 - p)))


# ---------------------------------------------------------------------------
# 3. Back propagation (chain rule)
# ---------------------------------------------------------------------------
def backward(params, cache, y_true):
    """Compute dLoss/dParam for every parameter."""
    n = y_true.shape[0]
    A1, A2, X_in = cache["A1"], cache["A2"], cache["X"]

    # Output layer: for sigmoid + BCE the derivative simplifies beautifully
    dZ2 = (A2 - y_true) / n                   # dL/dZ2
    dW2 = A1.T @ dZ2                          # dL/dW2
    db2 = dZ2.sum(axis=0, keepdims=True)

    # Hidden layer: push the error back through W2, then through tanh'
    dA1 = dZ2 @ params["W2"].T
    dZ1 = dA1 * (1 - A1 ** 2)                 # tanh'(z) = 1 - tanh(z)^2
    dW1 = X_in.T @ dZ1
    db1 = dZ1.sum(axis=0, keepdims=True)
    return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}


# ---------------------------------------------------------------------------
# 5. Gradient check
# ---------------------------------------------------------------------------
def gradient_check(params, X, Y, eps=1e-5):
    """Compare analytic (backprop) gradients to numerical finite differences.

    numerical grad ≈ [L(θ + ε) - L(θ - ε)] / (2ε)
    A relative error below ~1e-7 means backprop is implemented correctly.
    """
    _, cache = forward(params, X)
    analytic = backward(params, cache, Y)
    num_list, ana_list = [], []
    for name, P in params.items():
        for idx in np.ndindex(P.shape):
            old = P[idx]
            P[idx] = old + eps
            loss_plus = bce_loss(forward(params, X)[0], Y)
            P[idx] = old - eps
            loss_minus = bce_loss(forward(params, X)[0], Y)
            P[idx] = old                                  # restore!
            num_list.append((loss_plus - loss_minus) / (2 * eps))
            ana_list.append(analytic[name][idx])
    num, ana = np.array(num_list), np.array(ana_list)
    rel_error = np.linalg.norm(num - ana) / (np.linalg.norm(num) + np.linalg.norm(ana))
    return rel_error


# ---------------------------------------------------------------------------
# 4. Training loop (gradient descent)
# ---------------------------------------------------------------------------
def train(epochs, lr):
    params = init_params()

    rel_err = gradient_check(params, X, Y)
    status = "PASSED" if rel_err < 1e-7 else "CHECK YOUR MATH"
    print(f"Gradient check relative error: {rel_err:.2e}  -> {status}\n")

    losses = []
    for epoch in range(epochs + 1):
        y_pred, cache = forward(params, X)
        loss = bce_loss(y_pred, Y)
        losses.append(loss)
        grads = backward(params, cache, Y)
        for k in params:
            params[k] -= lr * grads[k]
        if epoch % max(1, epochs // 10) == 0:
            print(f"epoch {epoch:>5}  loss {loss:.4f}")
    return params, losses


def plot_results(params, losses):
    """Loss curve + learned (non-linear!) decision boundary."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].plot(losses)
    axes[0].set(title="Training loss (BCE)", xlabel="epoch", ylabel="loss")

    xx, yy = np.meshgrid(np.linspace(-0.5, 1.5, 200), np.linspace(-0.5, 1.5, 200))
    grid = np.c_[xx.ravel(), yy.ravel()]
    zz = forward(params, grid)[0].reshape(xx.shape)
    cs = axes[1].contourf(xx, yy, zz, levels=20, cmap="RdBu_r", alpha=0.8)
    fig.colorbar(cs, ax=axes[1], label="P(output = 1)")
    axes[1].scatter(X[:, 0], X[:, 1], c=Y.ravel(), cmap="RdBu_r", edgecolor="k", s=150)
    axes[1].set(title="XOR decision surface learned from scratch", xlabel="x1", ylabel="x2")
    plt.tight_layout()
    out = OUTPUT_DIR / "xor_from_scratch.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"\nSaved plot -> {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="2-4-1 network on XOR from scratch")
    parser.add_argument("--epochs", type=int, default=3000)
    parser.add_argument("--lr", type=float, default=1.0)
    args = parser.parse_args()

    trained, loss_history = train(args.epochs, args.lr)
    preds, _ = forward(trained, X)
    print("\nFinal predictions:")
    for x, p, t in zip(X, preds.ravel(), Y.ravel()):
        print(f"  {x.astype(int)} -> {p:.3f}  (rounded {int(p > 0.5)}, target {int(t)})")
    plot_results(trained, loss_history)
