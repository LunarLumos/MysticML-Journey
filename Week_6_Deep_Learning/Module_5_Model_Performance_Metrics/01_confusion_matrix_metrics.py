"""
Module 5 - Confusion Matrix, Precision, Recall, F1-Score
========================================================
We train a small Keras ANN on the Breast Cancer dataset and evaluate it:

  1. Build the confusion matrix (TP, FP, FN, TN)
  2. Compute accuracy / precision / recall / F1 BY HAND
  3. Verify with sklearn.metrics
  4. Show how moving the decision threshold trades precision vs recall

Here "positive" = malignant (the class we care about catching), so we flip
sklearn's labels (0 = malignant) to make malignant = 1.

Run:
    python 01_confusion_matrix_metrics.py
    python 01_confusion_matrix_metrics.py --epochs 40
"""

import argparse
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, confusion_matrix,
                             f1_score, precision_recall_curve, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
SEED = 42


def get_predictions(epochs):
    """Train a small ANN and return test labels + predicted probabilities."""
    data = load_breast_cancer()
    y = 1 - data.target                              # 1 = malignant (positive class)
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, y, test_size=0.3, random_state=SEED, stratify=y)
    scaler = StandardScaler().fit(X_train)
    X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

    model = keras.Sequential([
        keras.Input(shape=(X_train.shape[1],)),
        keras.layers.Dense(8, activation="relu"),
        keras.layers.Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy")
    model.fit(X_train, y_train, epochs=epochs, batch_size=32, verbose=0)
    return y_test, model.predict(X_test, verbose=0).ravel()


def manual_metrics(y_true, y_pred):
    """Compute the metrics from the four confusion-matrix counts."""
    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    tn = int(np.sum((y_pred == 0) & (y_true == 0)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))   # false alarm   (Type I error)
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))   # missed cancer (Type II error)
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if tp + fp else 0.0    # of predicted positives, how many right?
    recall = tp / (tp + fn) if tp + fn else 0.0       # of real positives, how many found?
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return dict(TP=tp, TN=tn, FP=fp, FN=fn, accuracy=accuracy,
                precision=precision, recall=recall, f1=f1)


def main(epochs):
    keras.utils.set_random_seed(SEED)
    OUTPUT_DIR.mkdir(exist_ok=True)
    y_test, probs = get_predictions(epochs)
    y_pred = (probs >= 0.5).astype(int)

    m = manual_metrics(y_test, y_pred)
    print("Confusion matrix layout (sklearn):  [[TN FP]\n                                     [FN TP]]")
    print(confusion_matrix(y_test, y_pred), "\n")
    print(f"TP={m['TP']}  TN={m['TN']}  FP={m['FP']}  FN={m['FN']}\n")
    print(f"{'Metric':<10}{'by hand':>10}{'sklearn':>10}")
    for name, fn in [("accuracy", accuracy_score), ("precision", precision_score),
                     ("recall", recall_score), ("f1", f1_score)]:
        print(f"{name:<10}{m[name]:>10.3f}{fn(y_test, y_pred):>10.3f}")

    # ---- Threshold trade-off ------------------------------------------------
    print("\nThreshold  precision  recall  f1")
    for thr in [0.2, 0.35, 0.5, 0.65, 0.8]:
        p = (probs >= thr).astype(int)
        mm = manual_metrics(y_test, p)
        print(f"   {thr:.2f}      {mm['precision']:.3f}    {mm['recall']:.3f}  {mm['f1']:.3f}")
    print("Lower threshold -> catch more cancers (recall up) but more false alarms.")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=["benign", "malignant"], ax=axes[0], colorbar=False)
    axes[0].set_title("Confusion matrix (threshold 0.5)")
    prec, rec, _ = precision_recall_curve(y_test, probs)
    axes[1].plot(rec, prec)
    axes[1].set(xlabel="Recall", ylabel="Precision", title="Precision-Recall curve")
    plt.tight_layout()
    out = OUTPUT_DIR / "confusion_matrix_metrics.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"\nSaved plot -> {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=20)
    main(parser.parse_args().epochs)
