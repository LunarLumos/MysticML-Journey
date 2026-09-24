"""
Module 3 - A CNN in Keras on handwritten digits (sklearn digits, 8x8, offline)
==============================================================================
Architecture (the classic CNN recipe):

    Input 8x8x1
      -> Conv2D(16, 3x3, ReLU, padding='same')   # learn 16 local feature detectors
      -> MaxPooling2D(2x2)                       # 8x8 -> 4x4
      -> Conv2D(32, 3x3, ReLU, padding='same')   # combine features
      -> MaxPooling2D(2x2)                       # 4x4 -> 2x2
      -> Flatten                                 # 2*2*32 = 128 numbers
      -> Dense(64, ReLU) -> Dropout
      -> Dense(10, softmax)                      # one probability per digit

The same design scales to 28x28 MNIST (70,000 images) - a great next step
once you are comfortable here (keras.datasets.mnist needs a one-time download).

Run:
    python 02_keras_cnn_digits.py
    python 02_keras_cnn_digits.py --epochs 40
"""

import argparse
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


def load_data():
    """Load 1797 8x8 digit images, scale to [0,1], add a channel dimension."""
    digits = load_digits()
    X = (digits.images / 16.0).astype("float32")[..., np.newaxis]   # (n, 8, 8, 1)
    y = digits.target
    return train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)


def build_cnn():
    model = keras.Sequential([
        keras.Input(shape=(8, 8, 1)),
        keras.layers.Conv2D(16, (3, 3), activation="relu", padding="same", name="conv1"),
        keras.layers.MaxPooling2D((2, 2), name="pool1"),
        keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same", name="conv2"),
        keras.layers.MaxPooling2D((2, 2), name="pool2"),
        keras.layers.Flatten(name="flatten"),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    return model


def plot_feature_maps(model, image):
    """Show what the first conv layer 'sees' for one digit."""
    extractor = keras.Model(inputs=model.inputs, outputs=model.get_layer("conv1").output)
    fmaps = extractor.predict(image[np.newaxis], verbose=0)[0]       # (8, 8, 16)
    fig, axes = plt.subplots(2, 9, figsize=(14, 3.5))
    axes[0, 0].imshow(image[..., 0], cmap="gray_r")
    axes[0, 0].set_title("input")
    axes[1, 0].axis("off")
    for i in range(16):
        ax = axes[i // 8, i % 8 + 1]
        ax.imshow(fmaps[..., i], cmap="viridis")
        ax.set_title(f"filter {i}", fontsize=8)
    for ax in axes.ravel():
        ax.set_xticks([])
        ax.set_yticks([])
    plt.suptitle("conv1 feature maps")
    plt.tight_layout()
    out = OUTPUT_DIR / "cnn_feature_maps.png"
    plt.savefig(out, dpi=110)
    plt.close()
    print(f"Saved feature maps -> {out}")


def plot_results(history, y_test, preds):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(history.history["accuracy"], label="train")
    axes[0].plot(history.history["val_accuracy"], label="validation")
    axes[0].set(title="Accuracy", xlabel="epoch")
    axes[0].legend()
    ConfusionMatrixDisplay.from_predictions(y_test, preds, ax=axes[1], colorbar=False)
    axes[1].set_title("Confusion matrix (test)")
    plt.tight_layout()
    out = OUTPUT_DIR / "cnn_digits_results.png"
    plt.savefig(out, dpi=110)
    plt.close()
    print(f"Saved results -> {out}")


def main(epochs):
    keras.utils.set_random_seed(SEED)
    OUTPUT_DIR.mkdir(exist_ok=True)
    X_train, X_test, y_train, y_test = load_data()
    print(f"Train images {X_train.shape}, test images {X_test.shape}")

    model = build_cnn()
    model.summary()
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=32,
                        validation_split=0.1, verbose=2)

    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nTest accuracy: {acc:.3f}  (loss {loss:.3f})")
    preds = model.predict(X_test, verbose=0).argmax(axis=1)
    print(classification_report(y_test, preds, digits=3))

    plot_results(history, y_test, preds)
    plot_feature_maps(model, X_test[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keras CNN on sklearn digits")
    parser.add_argument("--epochs", type=int, default=20)
    main(parser.parse_args().epochs)
