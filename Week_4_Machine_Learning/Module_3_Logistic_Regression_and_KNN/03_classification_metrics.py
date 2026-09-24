"""
03_classification_metrics.py
============================
Week 4 · Module 3 – Confusion Matrix & Classification Evaluation Metrics

                     Predicted 0    Predicted 1
    Actual 0  (neg)      TN             FP        ← "false alarm"
    Actual 1  (pos)      FN             TP
                         ↑ "missed case"

    Accuracy  = (TP + TN) / total
    Precision = TP / (TP + FP)      "when I say positive, how often am I right?"
    Recall    = TP / (TP + FN)      "of all real positives, how many did I catch?"
    F1        = 2 · P · R / (P + R) harmonic mean of precision & recall

We compute everything BY HAND from the confusion matrix, check it against
scikit-learn, and show how moving the decision threshold trades precision
for recall.

Run:
    python 03_classification_metrics.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def metrics_by_hand(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Compute TN/FP/FN/TP and the four headline metrics manually."""
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {
        "TN": tn, "FP": fp, "FN": fn, "TP": tp,
        "accuracy": (tp + tn) / len(y_true),
        "precision": precision,
        "recall": recall,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
    }


def main() -> None:
    """Train a classifier and dissect its evaluation metrics."""
    data = load_breast_cancer()
    # Make "malignant" the POSITIVE class (1) – it is the case we must not miss.
    y = (data.target == 0).astype(int)
    X_tr, X_te, y_tr, y_te = train_test_split(data.data, y, test_size=0.25,
                                              stratify=y, random_state=0)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)
    proba = model.predict_proba(X_te)[:, 1]

    manual = metrics_by_hand(y_te, y_pred)
    print("=" * 60)
    print("Confusion matrix (positive class = malignant)")
    print("=" * 60)
    print(confusion_matrix(y_te, y_pred))
    print(f"TN={manual['TN']}  FP={manual['FP']}  FN={manual['FN']}  TP={manual['TP']}\n")

    print(f"{'Metric':<11}{'by hand':>10}{'sklearn':>10}")
    for name, fn in (("accuracy", accuracy_score), ("precision", precision_score),
                     ("recall", recall_score), ("f1", f1_score)):
        print(f"{name:<11}{manual[name]:>10.4f}{fn(y_te, y_pred):>10.4f}")
    print(f"{'ROC AUC':<11}{'':>10}{roc_auc_score(y_te, proba):>10.4f}")

    print("\n[*] Full classification report:")
    print(classification_report(y_te, y_pred, target_names=["benign", "malignant"]))

    # --- Threshold trade-off ---
    print("[*] Moving the decision threshold (precision ↔ recall trade-off):")
    print(f"    {'threshold':>9}{'precision':>11}{'recall':>9}{'f1':>8}")
    for t in (0.2, 0.35, 0.5, 0.65, 0.8):
        m = metrics_by_hand(y_te, (proba >= t).astype(int))
        print(f"    {t:>9.2f}{m['precision']:>11.3f}{m['recall']:>9.3f}{m['f1']:>8.3f}")
    print("    → In cancer screening we prefer a LOW threshold (high recall).")

    OUTPUT_DIR.mkdir(exist_ok=True)
    disp = ConfusionMatrixDisplay.from_predictions(
        y_te, y_pred, display_labels=["benign", "malignant"], cmap="Blues")
    disp.ax_.set_title("Confusion matrix – logistic regression")
    out = OUTPUT_DIR / "confusion_matrix.png"
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"\n[*] Confusion matrix plot saved to: {out}")


if __name__ == "__main__":
    main()
