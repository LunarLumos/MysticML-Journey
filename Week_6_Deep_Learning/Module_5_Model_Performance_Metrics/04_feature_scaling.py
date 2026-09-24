"""
Module 5 - Feature Scaling
==========================
The Wine dataset has features on wildly different scales (proline ~ 1000,
hue ~ 1). Distance-based models (KNN) and gradient-based models (neural
networks) suffer when features aren't scaled.

We compare:
    no scaling | StandardScaler (mean 0, std 1) | MinMaxScaler (0..1)
on: KNN, Logistic Regression and a small Keras ANN.

Golden rule: fit the scaler on the TRAINING data only, then transform both
train and test (otherwise test information leaks into training).

Run:
    python 04_feature_scaling.py
    python 04_feature_scaling.py --epochs 50
"""

import argparse
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


def keras_accuracy(X_train, y_train, X_test, y_test, epochs):
    keras.utils.set_random_seed(SEED)
    model = keras.Sequential([
        keras.Input(shape=(X_train.shape[1],)),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(3, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    model.fit(X_train, y_train, epochs=epochs, batch_size=16, verbose=0)
    return model.evaluate(X_test, y_test, verbose=0)[1]


def main(epochs):
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = load_wine()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.3, random_state=SEED, stratify=data.target)

    print("Feature ranges BEFORE scaling (train set):")
    for name, lo, hi in zip(data.feature_names[:5], X_train.min(0), X_train.max(0)):
        print(f"  {name:<22} {lo:>8.2f} .. {hi:>8.2f}")
    print(f"  ... proline: {X_train[:, -1].min():.0f} .. {X_train[:, -1].max():.0f}\n")

    scalers = {"None": None, "StandardScaler": StandardScaler(), "MinMaxScaler": MinMaxScaler()}
    print(f"{'Scaling':<16}{'KNN':>8}{'LogReg':>8}{'Keras ANN':>11}")
    scaled_versions = {}
    for name, scaler in scalers.items():
        if scaler is None:
            Xtr, Xte = X_train, X_test
        else:
            scaler.fit(X_train)                       # fit on TRAIN only
            Xtr, Xte = scaler.transform(X_train), scaler.transform(X_test)
        scaled_versions[name] = Xtr
        knn = KNeighborsClassifier().fit(Xtr, y_train).score(Xte, y_test)
        logreg = LogisticRegression(max_iter=200).fit(Xtr, y_train).score(Xte, y_test)
        ann = keras_accuracy(Xtr, y_train, Xte, y_test, epochs)
        print(f"{name:<16}{knn:>8.3f}{logreg:>8.3f}{ann:>11.3f}")
    print("\n(LogReg may warn about convergence without scaling - that's the point!)")

    # ---- Plot: feature distributions before / after ---------------------------
    idx = [0, 4, 12]                                  # alcohol, magnesium, proline
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, (name, Xs) in zip(axes, scaled_versions.items()):
        ax.boxplot([Xs[:, i] for i in idx])
        ax.set_xticks(range(1, len(idx) + 1), [data.feature_names[i] for i in idx])
        ax.set_title(f"Scaling: {name}")
    plt.tight_layout()
    out = OUTPUT_DIR / "feature_scaling.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"Saved plot -> {out}")


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=30)
    main(parser.parse_args().epochs)
