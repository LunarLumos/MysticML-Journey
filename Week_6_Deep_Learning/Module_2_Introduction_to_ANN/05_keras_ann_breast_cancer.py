"""
Module 2 - The same ideas in Keras: an ANN on the Breast Cancer dataset
=======================================================================
Everything we coded by hand (forward pass, backprop, BCE, gradient descent)
is done for us by Keras:

    Dense layers  = W·x + b + activation     (feed forward)
    loss='binary_crossentropy'               (cost function)
    optimizer='adam'                         (backprop + smarter gradient descent)

Dataset: sklearn's built-in Breast Cancer Wisconsin (569 samples, 30 features,
binary target: malignant=0 / benign=1). No download needed.

Run:
    python 05_keras_ann_breast_cancer.py
    python 05_keras_ann_breast_cancer.py --epochs 50
"""

import argparse
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


def load_data():
    """Split and standard-scale the data (fit scaler on TRAIN only)."""
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=SEED, stratify=data.target
    )
    scaler = StandardScaler().fit(X_train)
    return scaler.transform(X_train), scaler.transform(X_test), y_train, y_test, data.target_names


def build_model(n_features):
    """30 inputs -> 16 ReLU -> 8 ReLU -> 1 sigmoid."""
    model = keras.Sequential([
        keras.Input(shape=(n_features,)),
        keras.layers.Dense(16, activation="relu", name="hidden_1"),
        keras.layers.Dense(8, activation="relu", name="hidden_2"),
        keras.layers.Dense(1, activation="sigmoid", name="output"),
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                  loss="binary_crossentropy",
                  metrics=["accuracy"])
    return model


def plot_history(history):
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, key in zip(axes, ["loss", "accuracy"]):
        ax.plot(history.history[key], label=f"train {key}")
        ax.plot(history.history[f"val_{key}"], label=f"val {key}")
        ax.set(xlabel="epoch", ylabel=key, title=key.capitalize())
        ax.legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "keras_ann_breast_cancer.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"Saved training curves -> {out}")


def main(epochs):
    keras.utils.set_random_seed(SEED)
    X_train, X_test, y_train, y_test, names = load_data()
    model = build_model(X_train.shape[1])
    model.summary()

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=32,
                        validation_split=0.2, verbose=0)
    print(f"Final train loss {history.history['loss'][-1]:.4f} | "
          f"val loss {history.history['val_loss'][-1]:.4f}")

    probs = model.predict(X_test, verbose=0).ravel()
    preds = (probs > 0.5).astype(int)
    print(f"\nTest accuracy: {accuracy_score(y_test, preds):.3f}\n")
    print(classification_report(y_test, preds, target_names=names))

    # Peek inside: the learned weight matrix of the first layer
    W1, b1 = model.get_layer("hidden_1").get_weights()
    print(f"hidden_1 weights shape {W1.shape}, bias shape {b1.shape} "
          f"-> {W1.size + b1.size} trainable numbers")
    plot_history(history)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keras ANN on breast cancer data")
    parser.add_argument("--epochs", type=int, default=30)
    main(parser.parse_args().epochs)
