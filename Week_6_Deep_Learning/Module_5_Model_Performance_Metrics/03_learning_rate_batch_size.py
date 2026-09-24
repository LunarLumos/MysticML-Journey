"""
Module 5 - Learning Rate and Batch Size experiments
===================================================
Two of the most important training hyper-parameters:

  Learning rate (lr): how big each gradient-descent step is.
      too small -> painfully slow      too big -> loss jumps around / diverges
  Batch size: how many samples are used per gradient update.
      small -> noisy but many updates per epoch (often generalises well)
      large -> smooth, fast per epoch on GPU, but fewer updates

We train the same small network on the sklearn digits dataset (flattened 64
pixels) with different settings and compare the loss curves.
Plain SGD is used so the effect of the learning rate is easy to see.

Run:
    python 03_learning_rate_batch_size.py
    python 03_learning_rate_batch_size.py --epochs 30
"""

import argparse
import os
import time
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


def load_data():
    X, y = load_digits(return_X_y=True)
    X = (X / 16.0).astype("float32")
    return train_test_split(X, y, test_size=0.25, random_state=SEED, stratify=y)


def run(X_train, y_train, X_val, y_val, lr, batch_size, epochs):
    """Train one fresh model and return (history, val accuracy, seconds)."""
    keras.utils.set_random_seed(SEED)
    model = keras.Sequential([
        keras.Input(shape=(64,)),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(optimizer=keras.optimizers.SGD(learning_rate=lr),
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    start = time.time()
    h = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs,
                  batch_size=batch_size, verbose=0)
    return h.history, h.history["val_accuracy"][-1], time.time() - start


def main(epochs):
    OUTPUT_DIR.mkdir(exist_ok=True)
    X_train, X_val, y_train, y_val = load_data()
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

    # ---- Experiment 1: learning rate ------------------------------------------
    print("Experiment 1 - learning rate (batch size 32, SGD)")
    print(f"{'lr':>8} | {'final train loss':>16} | {'val acc':>7}")
    for lr in [0.001, 0.01, 0.1, 1.0, 5.0]:
        hist, val_acc, _ = run(X_train, y_train, X_val, y_val, lr, 32, epochs)
        loss = np.array(hist["loss"], dtype=float)
        loss = np.where(np.isfinite(loss), loss, np.nan)        # diverged -> NaN
        print(f"{lr:>8} | {loss[-1]:>16.4f} | {val_acc:>7.3f}")
        axes[0].plot(loss, label=f"lr={lr}")
    axes[0].set(title="Effect of learning rate", xlabel="epoch", ylabel="train loss",
                yscale="log")
    axes[0].legend()

    # ---- Experiment 2: batch size ---------------------------------------------
    print("\nExperiment 2 - batch size (lr 0.1, SGD)")
    print(f"{'batch':>6} | {'updates/epoch':>13} | {'val acc':>7} | {'seconds':>7}")
    for bs in [8, 32, 128, len(X_train)]:
        hist, val_acc, secs = run(X_train, y_train, X_val, y_val, 0.1, bs, epochs)
        updates = int(np.ceil(len(X_train) / bs))
        print(f"{bs:>6} | {updates:>13} | {val_acc:>7.3f} | {secs:>7.1f}")
        label = f"batch={bs}" + (" (full batch)" if bs == len(X_train) else "")
        axes[1].plot(hist["val_loss"], label=label)
    axes[1].set(title="Effect of batch size", xlabel="epoch", ylabel="validation loss",
                yscale="log")
    axes[1].legend()

    plt.tight_layout()
    out = OUTPUT_DIR / "learning_rate_batch_size.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"\nSaved plot -> {out}")
    print("Tip: Adam's default lr=0.001 is a solid start; batch 32 is a common default.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=15)
    main(parser.parse_args().epochs)
