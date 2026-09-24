"""
Module 4 - SimpleRNN vs LSTM in Keras: forecasting a noisy sine wave
====================================================================
Task: given the last WINDOW values of a (synthetic, seeded) noisy sine wave,
predict the next value.

We train two models with the SAME size and settings:
    SimpleRNN(32) -> Dense(1)
    LSTM(32)      -> Dense(1)
and compare test MSE, parameter count and training time.

Data is SYNTHETIC: sin(t) + 0.5*sin(t/3) + small Gaussian noise.

Run:
    python 02_simplernn_vs_lstm_sine.py
    python 02_simplernn_vs_lstm_sine.py --epochs 30 --window 60
"""

import argparse
import os
import time
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def make_series(n_points=1500, noise=0.05, seed=SEED):
    """Synthetic signal with a short AND a long cycle, plus noise."""
    rng = np.random.default_rng(seed)
    t = np.arange(n_points) * 0.1
    return (np.sin(t) + 0.5 * np.sin(t / 3) + rng.normal(0, noise, n_points)).astype("float32")


def make_windows(series, window):
    """Turn a 1-D series into (samples, window, 1) inputs and next-value targets."""
    X = np.array([series[i:i + window] for i in range(len(series) - window)])
    y = series[window:]
    return X[..., np.newaxis], y


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
def build(kind, window, units=32):
    layer = keras.layers.SimpleRNN if kind == "SimpleRNN" else keras.layers.LSTM
    model = keras.Sequential([
        keras.Input(shape=(window, 1)),
        layer(units),
        keras.layers.Dense(1),
    ], name=kind)
    model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="mse")
    return model


def main(epochs, window):
    keras.utils.set_random_seed(SEED)
    OUTPUT_DIR.mkdir(exist_ok=True)

    series = make_series()
    X, y = make_windows(series, window)
    split = int(0.8 * len(X))                       # time series: NO shuffling split
    X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]
    print(f"Train windows {X_train.shape}, test windows {X_test.shape}\n")

    # Baseline: "tomorrow = today"
    naive_mse = float(np.mean((X_test[:, -1, 0] - y_test) ** 2))

    results, histories, preds = {}, {}, {}
    for kind in ["SimpleRNN", "LSTM"]:
        keras.utils.set_random_seed(SEED)
        model = build(kind, window)
        start = time.time()
        hist = model.fit(X_train, y_train, epochs=epochs, batch_size=32,
                         validation_split=0.1, verbose=0)
        seconds = time.time() - start
        mse = model.evaluate(X_test, y_test, verbose=0)
        results[kind] = (model.count_params(), seconds, mse)
        histories[kind] = hist.history
        preds[kind] = model.predict(X_test, verbose=0).ravel()
        print(f"{kind:<10} trained in {seconds:5.1f}s  test MSE = {mse:.5f}")

    # ---- Comparison table --------------------------------------------------
    print(f"\n{'Model':<12}{'Params':>8}{'Train s':>10}{'Test MSE':>12}")
    print("-" * 42)
    for kind, (params, secs, mse) in results.items():
        print(f"{kind:<12}{params:>8}{secs:>10.1f}{mse:>12.5f}")
    print(f"{'Naive last':<12}{0:>8}{0:>10.1f}{naive_mse:>12.5f}   <- baseline")
    print("\nLSTM has ~4x the parameters (input/forget/output gates + candidate).")
    print("A smooth sine wave only needs SHORT memory (the last few points), so both")
    print("models beat the naive baseline and score about the same here. LSTM's gated")
    print("cell state pays off when the answer depends on inputs FAR back in time")
    print("(long texts, long-range seasonality) - where SimpleRNN's gradients vanish.")

    # ---- Plots --------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
    for kind, h in histories.items():
        axes[0].plot(h["val_loss"], label=f"{kind} val loss")
    axes[0].set(title="Validation MSE", xlabel="epoch", yscale="log")
    axes[0].legend()
    n = 200
    axes[1].plot(y_test[:n], "k", lw=2, label="true")
    for kind, p in preds.items():
        axes[1].plot(p[:n], "--", label=kind)
    axes[1].set(title=f"Next-step forecast (first {n} test points)", xlabel="time step")
    axes[1].legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "rnn_vs_lstm_sine.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"Saved plot -> {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SimpleRNN vs LSTM on a sine wave")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--window", type=int, default=40, help="input sequence length")
    args = parser.parse_args()
    main(args.epochs, args.window)
