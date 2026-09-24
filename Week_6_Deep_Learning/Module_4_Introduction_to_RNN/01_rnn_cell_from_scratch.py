"""
Module 4 - An RNN cell FROM SCRATCH (forward pass) + the vanishing gradient
===========================================================================
A Recurrent Neural Network reads a sequence one step at a time and keeps a
"memory" vector h (the hidden state):

    h_t = tanh( W_x · x_t  +  W_h · h_(t-1)  +  b )
    y_t = W_y · h_t + b_y

The SAME weights (W_x, W_h, W_y) are reused at every time step.

Part A: run the forward pass on a small sequence and print h_t.
Part B: show WHY plain RNNs forget long-range information - the gradient
        flowing back through time is multiplied by W_h and tanh' at every
        step, so it shrinks exponentially (vanishing gradient).

Run:
    python 01_rnn_cell_from_scratch.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


class SimpleRNNCell:
    """Minimal NumPy RNN: input_dim -> hidden_dim -> output_dim."""

    def __init__(self, input_dim, hidden_dim, output_dim, weight_scale=0.5, seed=SEED):
        rng = np.random.default_rng(seed)
        self.Wx = rng.normal(0, weight_scale, (hidden_dim, input_dim))
        self.Wh = rng.normal(0, weight_scale / np.sqrt(hidden_dim), (hidden_dim, hidden_dim))
        self.b = np.zeros(hidden_dim)
        self.Wy = rng.normal(0, weight_scale, (output_dim, hidden_dim))
        self.by = np.zeros(output_dim)

    def step(self, x_t, h_prev):
        """One time step: combine the new input with the previous memory."""
        return np.tanh(self.Wx @ x_t + self.Wh @ h_prev + self.b)

    def forward(self, sequence):
        """Process a whole sequence; return all hidden states and outputs."""
        h = np.zeros(self.Wh.shape[0])
        hs, ys = [], []
        for x_t in sequence:
            h = self.step(x_t, h)
            hs.append(h)
            ys.append(self.Wy @ h + self.by)
        return np.array(hs), np.array(ys)


# ---------------------------------------------------------------------------
# Part A - forward pass
# ---------------------------------------------------------------------------
def forward_demo():
    print("=" * 60)
    print("Part A: forward pass through time")
    print("=" * 60)
    rnn = SimpleRNNCell(input_dim=1, hidden_dim=4, output_dim=1)
    sequence = np.array([[1.0], [0.0], [0.0], [0.0], [0.0], [0.0]])   # one "spike" then zeros
    hs, ys = rnn.forward(sequence)
    print("input is 1 at t=0 and 0 afterwards - watch the memory fade:\n")
    for t, (x, h, y) in enumerate(zip(sequence, hs, ys)):
        print(f"t={t}  x={x[0]:.0f}  h={np.round(h, 3)}  |h|={np.linalg.norm(h):.3f}  y={y[0]:+.3f}")
    print()


# ---------------------------------------------------------------------------
# Part B - vanishing gradient
# ---------------------------------------------------------------------------
def gradient_norms_through_time(rnn, seq_len=50):
    """Norm of d h_T / d h_t for t = T..0 (how much the start still matters)."""
    rng = np.random.default_rng(SEED)
    sequence = rng.normal(0, 1, (seq_len, rnn.Wx.shape[1]))
    hs, _ = rnn.forward(sequence)
    grad = np.eye(rnn.Wh.shape[0])              # d h_T / d h_T = identity
    norms = [np.linalg.norm(grad)]
    for t in range(seq_len - 1, 0, -1):
        # d h_t / d h_(t-1) = diag(1 - h_t^2) · W_h      (chain rule)
        jac = np.diag(1 - hs[t] ** 2) @ rnn.Wh
        grad = grad @ jac
        norms.append(np.linalg.norm(grad))
    return np.array(norms[::-1])                # index = time step t


def vanishing_gradient_demo():
    print("=" * 60)
    print("Part B: vanishing gradient in a plain RNN")
    print("=" * 60)
    OUTPUT_DIR.mkdir(exist_ok=True)
    plt.figure(figsize=(8, 4.5))
    for scale in [0.5, 1.0, 2.0]:
        rnn = SimpleRNNCell(input_dim=1, hidden_dim=16, output_dim=1, weight_scale=scale)
        norms = gradient_norms_through_time(rnn)
        print(f"weight scale {scale}: |dh_T/dh_T| = {norms[-1]:.2e}  ->  "
              f"|dh_T/dh_0| = {norms[0]:.2e}")
        plt.semilogy(norms, label=f"W_h scale {scale}")
    plt.xlabel("time step t (T = 49 is the last step)")
    plt.ylabel("‖ ∂h_T / ∂h_t ‖  (log scale)")
    plt.title("Gradient reaching early time steps shrinks exponentially")
    plt.legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "rnn_vanishing_gradient.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print("\nEarly inputs get almost no gradient -> the RNN cannot learn")
    print("long-range dependencies. LSTM fixes this with a gated cell state.")
    print(f"Saved plot -> {out}")


if __name__ == "__main__":
    forward_demo()
    vanishing_gradient_demo()
