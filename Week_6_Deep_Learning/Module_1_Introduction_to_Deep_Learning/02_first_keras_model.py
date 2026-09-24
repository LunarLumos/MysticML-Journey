"""
Module 1 - Your First Keras Model
=================================
Two tiny "hello world" models:

  Part A: a single neuron learns the rule  y = 2x + 1  from examples.
          (It should discover weight ≈ 2 and bias ≈ 1 by itself!)
  Part B: a small network classifies Iris flowers (sklearn built-in data).

The 5 Keras steps you will repeat all week:
  1. Prepare data   2. Build model   3. Compile   4. Fit   5. Evaluate/Predict

Run:
    python 02_first_keras_model.py              # default epochs
    python 02_first_keras_model.py --epochs 300
"""

import argparse
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


# ---------------------------------------------------------------------------
# Part A - one neuron learns a straight line
# ---------------------------------------------------------------------------
def line_model(epochs):
    """Train a 1-neuron model on y = 2x + 1 and print learned weight & bias."""
    print("=" * 60)
    print("Part A: single neuron learns y = 2x + 1")
    print("=" * 60)

    # 1. Data
    x = np.linspace(-5, 5, 50).reshape(-1, 1).astype("float32")
    y = 2 * x + 1

    # 2. Model: Dense(1) == one neuron == w*x + b
    model = keras.Sequential([keras.Input(shape=(1,)), keras.layers.Dense(1)])

    # 3. Compile: choose optimizer + loss
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.1), loss="mse")

    # 4. Fit
    history = model.fit(x, y, epochs=epochs, verbose=0)

    # 5. Inspect / predict
    w, b = model.layers[0].get_weights()
    print(f"Learned weight = {w[0][0]:.3f}  (true 2)")
    print(f"Learned bias   = {b[0]:.3f}  (true 1)")
    print(f"Prediction for x=10: {model.predict(np.array([[10.0]]), verbose=0)[0][0]:.2f} (true 21)")
    print(f"Final MSE loss: {history.history['loss'][-1]:.5f}\n")
    return history


# ---------------------------------------------------------------------------
# Part B - a small classifier on Iris
# ---------------------------------------------------------------------------
def iris_model(epochs):
    """Train a tiny dense network on the Iris dataset."""
    print("=" * 60)
    print("Part B: small neural network on Iris (3 classes)")
    print("=" * 60)
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )
    scaler = StandardScaler().fit(X_train)          # neural nets like scaled inputs
    X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

    model = keras.Sequential([
        keras.Input(shape=(4,)),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(3, activation="softmax"),   # 3 class probabilities
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    model.summary()

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=16,
                        validation_split=0.2, verbose=0)
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test accuracy: {acc:.3f}   Test loss: {loss:.3f}")

    probs = model.predict(X_test[:3], verbose=0)
    print("First 3 test samples -> predicted class probabilities:")
    for p, true in zip(probs, y_test[:3]):
        print(f"  {np.round(p, 3)}  predicted={p.argmax()}  true={true}")
    return history


def plot_histories(hist_a, hist_b):
    """Save loss curves of both models side by side."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(hist_a.history["loss"])
    axes[0].set(title="Part A: y = 2x + 1 (MSE)", xlabel="epoch", ylabel="loss")
    axes[1].plot(hist_b.history["accuracy"], label="train acc")
    axes[1].plot(hist_b.history["val_accuracy"], label="val acc")
    axes[1].set(title="Part B: Iris accuracy", xlabel="epoch", ylabel="accuracy")
    axes[1].legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "first_keras_model.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"\nSaved training curves -> {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="First Keras models")
    parser.add_argument("--epochs", type=int, default=100, help="training epochs")
    args = parser.parse_args()

    keras.utils.set_random_seed(SEED)       # seeds Python, NumPy and TensorFlow
    h_a = line_model(args.epochs)
    h_b = iris_model(args.epochs)
    plot_histories(h_a, h_b)
