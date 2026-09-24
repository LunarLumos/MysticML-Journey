"""
Module 5 - Overfitting vs Underfitting
======================================
Part A (sklearn): fit polynomials of degree 1, 4 and 15 to noisy data.
         degree 1  -> UNDERFIT (too simple, high bias)
         degree 4  -> GOOD FIT
         degree 15 -> OVERFIT  (memorises noise, high variance)
Part B (sklearn): learning curves - train vs validation score as the
         training set grows - the standard diagnostic tool.
Part C (Keras):  a big network trained on very little data overfits
         (val loss goes UP while train loss goes down). Dropout + L2
         regularisation + EarlyStopping fight it.

Data: synthetic (seeded) for A, sklearn digits for B, breast cancer for C.

Run:
    python 02_overfitting_underfitting.py
    python 02_overfitting_underfitting.py --epochs 150
"""

import argparse
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer, load_digits
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import learning_curve, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


# ---------------------------------------------------------------------------
# Part A - polynomial degrees
# ---------------------------------------------------------------------------
def polynomial_demo():
    print("=" * 60)
    print("Part A: under / good / over fitting with polynomials")
    print("=" * 60)
    rng = np.random.default_rng(SEED)
    x = np.sort(rng.uniform(0, 1, 30))
    y = np.cos(1.5 * np.pi * x) + rng.normal(0, 0.1, 30)
    x_test = np.sort(rng.uniform(0, 1, 100))
    y_test = np.cos(1.5 * np.pi * x_test) + rng.normal(0, 0.1, 100)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    grid = np.linspace(0, 1, 300)
    for ax, degree, label in zip(axes, [1, 4, 15], ["UNDERFIT", "GOOD FIT", "OVERFIT"]):
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(x[:, None], y)
        train_mse = mean_squared_error(y, model.predict(x[:, None]))
        test_mse = mean_squared_error(y_test, model.predict(x_test[:, None]))
        print(f"degree {degree:>2}: train MSE {train_mse:.4f} | test MSE {test_mse:.4f}  -> {label}")
        ax.scatter(x, y, s=15, label="train data")
        ax.plot(grid, np.cos(1.5 * np.pi * grid), "g:", label="true function")
        ax.plot(grid, model.predict(grid[:, None]), "r", label=f"degree {degree}")
        ax.set(ylim=(-2, 2), title=f"{label}  (test MSE {test_mse:.3f})")
        ax.legend(fontsize=8)
    plt.tight_layout()
    out = OUTPUT_DIR / "under_over_fitting_poly.png"
    plt.savefig(out, dpi=110)
    plt.close()
    print(f"Saved -> {out}\n")


# ---------------------------------------------------------------------------
# Part B - learning curves
# ---------------------------------------------------------------------------
def learning_curve_demo():
    print("=" * 60)
    print("Part B: learning curves")
    print("=" * 60)
    X, y = load_digits(return_X_y=True)
    models = {
        "Decision tree depth=2 (underfits)": DecisionTreeClassifier(max_depth=2, random_state=SEED),
        "Decision tree unlimited (overfits)": DecisionTreeClassifier(random_state=SEED),
        "SVC rbf (good)": make_pipeline(StandardScaler(), SVC()),
    }
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, (name, model) in zip(axes, models.items()):
        sizes, train_sc, val_sc = learning_curve(
            model, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 6), n_jobs=1)
        tr, va = train_sc.mean(axis=1), val_sc.mean(axis=1)
        print(f"{name:<36} train acc {tr[-1]:.3f} | val acc {va[-1]:.3f} | gap {tr[-1] - va[-1]:.3f}")
        ax.plot(sizes, tr, "o-", label="train")
        ax.plot(sizes, va, "o-", label="validation")
        ax.set(title=name, xlabel="training samples", ylabel="accuracy", ylim=(0, 1.05))
        ax.legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "learning_curves.png"
    plt.savefig(out, dpi=110)
    plt.close()
    print("Both curves low & close = underfit | big gap = overfit | both high & close = good")
    print(f"Saved -> {out}\n")


# ---------------------------------------------------------------------------
# Part C - overfitting a Keras network and fixing it
# ---------------------------------------------------------------------------
def big_net(regularised):
    reg = keras.regularizers.l2(1e-3) if regularised else None
    layers = [keras.Input(shape=(30,))]
    for _ in range(3):
        layers.append(keras.layers.Dense(256, activation="relu", kernel_regularizer=reg))
        if regularised:
            layers.append(keras.layers.Dropout(0.5))
    layers.append(keras.layers.Dense(1, activation="sigmoid"))
    model = keras.Sequential(layers)
    # NOTE: Keras' reported `loss` also contains the L2 penalty, so we track the
    # pure cross-entropy as a separate metric ("bce") for a fair comparison.
    model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="binary_crossentropy",
                  metrics=["accuracy", keras.metrics.BinaryCrossentropy(name="bce")])
    return model


def keras_overfit_demo(epochs):
    print("=" * 60)
    print("Part C: Keras - overfitting and regularisation")
    print("=" * 60)
    X, y = load_breast_cancer(return_X_y=True)
    # Deliberately tiny training set (40 samples) to make overfitting obvious
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, train_size=40, random_state=SEED, stratify=y)
    scaler = StandardScaler().fit(X_train)
    X_train, X_val = scaler.transform(X_train), scaler.transform(X_val)
    y_train, y_val = y_train.reshape(-1, 1), y_val.reshape(-1, 1)   # match (n, 1) output

    runs = {}
    for name, regularised, callbacks in [
        ("No regularisation", False, []),
        ("Dropout + L2 + EarlyStopping", True,
         [keras.callbacks.EarlyStopping(monitor="val_bce", patience=10,
                                        restore_best_weights=True)]),
    ]:
        keras.utils.set_random_seed(SEED)
        model = big_net(regularised)
        h = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs,
                      batch_size=8, verbose=0, callbacks=callbacks)
        _, val_acc, val_bce = model.evaluate(X_val, y_val, verbose=0)
        runs[name] = h.history
        best = int(np.argmin(h.history["val_bce"]))
        print(f"{name:<30} epochs run {len(h.history['loss']):>3} | train BCE "
              f"{h.history['bce'][-1]:.4f} | best val BCE {h.history['val_bce'][best]:.4f} "
              f"(epoch {best + 1}) | val BCE of kept model {val_bce:.4f} | val acc {val_acc:.3f}")
    print("Without regularisation train BCE -> 0 while val BCE climbs after its best epoch:"
          " that gap is overfitting.")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, (name, h) in zip(axes, runs.items()):
        ax.plot(h["bce"], label="train BCE")
        ax.plot(h["val_bce"], label="validation BCE")
        ax.set(title=name, xlabel="epoch", ylabel="BCE loss")
        ax.legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "keras_overfitting.png"
    plt.savefig(out, dpi=110)
    plt.close()
    print(f"Saved -> {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=80)
    args = parser.parse_args()
    OUTPUT_DIR.mkdir(exist_ok=True)
    polynomial_demo()
    learning_curve_demo()
    keras_overfit_demo(args.epochs)
