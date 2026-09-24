"""
Module 7 - Step 2: Training the Face Recognition Model
======================================================

1. Load every crop in dataset/<person>/  -> faces + integer labels
2. Hold out 25 % of the samples (stratified) and train on the rest
3. Report accuracy, a classification report and a confusion matrix
4. Retrain on ALL samples and save the final model to models/

    python 02_train_model.py                    # auto: LBPH if opencv-contrib, else Eigenfaces
    python 02_train_model.py --method eigen     # force the scikit-learn PCA + SVM recognizer
    python 02_train_model.py --method lbph      # force OpenCV LBPH (needs opencv-contrib-python)

No dataset yet? Run 01_capture_samples.py first (or add --synthetic here to
generate an offline synthetic dataset automatically).
"""

import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report)
from sklearn.model_selection import train_test_split

from face_recognition_utils import (DATASET_DIR, MODELS_DIR, FaceRecognizer,
                                    generate_synthetic_dataset, load_dataset)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def evaluate(method, faces, labels, names, test_size, seed=42):
    """Train on a split, evaluate on the held-out part; returns accuracy."""
    idx = np.arange(len(labels))
    train_idx, test_idx = train_test_split(idx, test_size=test_size, stratify=labels,
                                           random_state=seed)
    rec = FaceRecognizer(method, names)
    start = time.perf_counter()
    rec.fit([faces[i] for i in train_idx], labels[train_idx])
    print(f"Trained '{rec.method}' on {len(train_idx)} faces in "
          f"{time.perf_counter() - start:.2f} s")

    preds, unknown = [], 0
    for i in test_idx:
        label, _score, confident = rec.predict(faces[i])
        preds.append(label)
        unknown += not confident
    preds = np.array(preds)
    acc = accuracy_score(labels[test_idx], preds)
    print(f"\nHeld-out accuracy: {acc:.3f} on {len(test_idx)} faces "
          f"({unknown} would be flagged 'Unknown' by the confidence threshold)")
    print(classification_report(labels[test_idx], preds, labels=range(len(names)),
                                target_names=names, zero_division=0))

    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(labels[test_idx], preds,
                                            labels=range(len(names)),
                                            display_labels=names, ax=ax,
                                            xticks_rotation=45, colorbar=False)
    ax.set_title(f"Face recognition ({rec.method}) - held-out set")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=100)
    plt.close(fig)
    print(f"Confusion matrix saved -> {OUTPUT_DIR / 'confusion_matrix.png'}")
    return acc


def save_eigenfaces_figure(rec, n=8):
    """For the Eigenfaces model, plot the mean face and the first principal components."""
    if rec.method != "eigen":
        return
    pca = rec.model.named_steps["pca"]
    shape = (100, 100)
    fig, axes = plt.subplots(1, n + 1, figsize=(2 * (n + 1), 2.4))
    axes[0].imshow(pca.mean_.reshape(shape), cmap="gray")
    axes[0].set_title("mean face")
    for i in range(n):
        axes[i + 1].imshow(pca.components_[i].reshape(shape), cmap="gray")
        axes[i + 1].set_title(f"eigenface {i + 1}")
    for ax in axes:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "eigenfaces.png", dpi=100)
    plt.close(fig)
    print(f"Eigenfaces figure saved -> {OUTPUT_DIR / 'eigenfaces.png'}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train the face recognizer")
    parser.add_argument("--method", choices=["auto", "lbph", "eigen"], default="auto")
    parser.add_argument("--test-size", type=float, default=0.25)
    parser.add_argument("--synthetic", action="store_true",
                        help="generate a synthetic dataset first if dataset/ is empty")
    args = parser.parse_args()

    faces, labels, names = load_dataset()
    if not names and args.synthetic:
        generate_synthetic_dataset()
        faces, labels, names = load_dataset()
    if len(names) < 2:
        sys.exit(f"Need samples of at least 2 people in {DATASET_DIR} "
                 "(run 01_capture_samples.py, or use --synthetic).")

    print(f"Dataset: {len(faces)} faces of {len(names)} people -> "
          + ", ".join(f"{n} ({(labels == i).sum()})" for i, n in enumerate(names)))
    evaluate(args.method, faces, labels, names, args.test_size)

    # Final model: use every sample we have
    final = FaceRecognizer(args.method, names).fit(faces, labels)
    model_file = final.save(MODELS_DIR)
    print(f"\nFinal model ({final.method}) trained on all {len(faces)} faces -> {model_file}")
    save_eigenfaces_figure(final)
