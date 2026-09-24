"""
Module 2 - The Artificial Neuron (concept)
==========================================
A single artificial neuron does three things:

    1. multiply each input by a weight       x1*w1, x2*w2, ...
    2. add them up plus a bias               z = w·x + b
    3. pass z through an activation function a = f(z)

We build one by hand with NumPy, then show that a single neuron can
learn AND / OR (linearly separable) but NOT XOR - which is why we need
hidden layers (see 03_ann_from_scratch_xor.py).

Run:
    python 01_neuron_concept.py
"""

import numpy as np


# ---------------------------------------------------------------------------
# A neuron as a tiny class
# ---------------------------------------------------------------------------
class Neuron:
    """One artificial neuron with a sigmoid activation."""

    def __init__(self, n_inputs, seed=0):
        rng = np.random.default_rng(seed)
        self.w = rng.normal(0, 0.5, size=n_inputs)
        self.b = 0.0

    @staticmethod
    def sigmoid(z):
        """Squash any number into (0, 1)."""
        return 1 / (1 + np.exp(-z))

    def forward(self, x):
        """Weighted sum + bias, then activation."""
        z = x @ self.w + self.b
        return self.sigmoid(z)

    def train(self, X, y, lr=1.0, epochs=2000):
        """Classic gradient descent on binary cross-entropy (the 'perceptron' idea)."""
        for _ in range(epochs):
            p = self.forward(X)
            error = p - y                      # dLoss/dz for sigmoid + BCE
            self.w -= lr * X.T @ error / len(X)
            self.b -= lr * error.mean()


def demo_single_forward():
    """Walk through one forward pass step by step."""
    print("=" * 60)
    print("One forward pass, step by step")
    print("=" * 60)
    x = np.array([1.0, 0.5, -1.5])        # inputs (e.g. 3 features)
    w = np.array([0.4, -0.2, 0.1])        # weights = importance of each input
    b = 0.3                               # bias = shifts the threshold
    z = np.dot(w, x) + b
    a = 1 / (1 + np.exp(-z))
    print(f"inputs  x = {x}")
    print(f"weights w = {w}, bias b = {b}")
    print(f"z = w·x + b = {z:.3f}")
    print(f"a = sigmoid(z) = {a:.3f}   <- neuron output\n")


def demo_logic_gates():
    """Train one neuron on AND, OR and XOR truth tables."""
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    gates = {
        "AND": np.array([0, 0, 0, 1]),
        "OR": np.array([0, 1, 1, 1]),
        "XOR": np.array([0, 1, 1, 0]),
    }
    print("=" * 60)
    print("Can ONE neuron learn these logic gates?")
    print("=" * 60)
    for name, y in gates.items():
        neuron = Neuron(2)
        neuron.train(X, y)
        pred = (neuron.forward(X) > 0.5).astype(int)
        ok = "YES" if np.array_equal(pred, y) else "NO  <- not linearly separable!"
        print(f"{name:>3}: target={y}  predicted={pred}  learned? {ok}")
    print("\nXOR needs a hidden layer -> see 03_ann_from_scratch_xor.py")


if __name__ == "__main__":
    demo_single_forward()
    demo_logic_gates()
