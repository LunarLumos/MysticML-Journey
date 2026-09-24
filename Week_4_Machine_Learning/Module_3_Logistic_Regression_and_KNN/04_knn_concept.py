"""
04_knn_concept.py
=================
Week 4 · Module 3 – Concept of the KNN (K-Nearest Neighbours) Model

KNN is a "lazy" learner: training = just storing the data. To classify a new
point it:
    1. computes the distance to EVERY training point
           Euclidean  d(a, b) = sqrt( Σ (a_i − b_i)² )
    2. takes the k closest points
    3. returns the majority vote of their labels

Choosing k:
    small k  → very flexible, noisy, over-fits  (k = 1 memorises the data)
    large k  → smooth, may under-fit
    use an ODD k for binary problems (avoids ties) and pick it with cross-validation.
    ALWAYS scale features – distances are dominated by large-valued features otherwise.

Run:
    python 04_knn_concept.py
"""

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_wine, make_moons
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


class KNNScratch:
    """K-Nearest Neighbours classifier in pure NumPy."""

    def __init__(self, k: int = 5):
        self.k = k

    def fit(self, X: np.ndarray, y: np.ndarray) -> "KNNScratch":
        """'Training' = memorising the data."""
        self.X_train, self.y_train = X, y
        return self

    def predict_one(self, x: np.ndarray) -> int:
        """Majority vote of the k nearest neighbours of a single point."""
        distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        nearest = np.argsort(distances)[: self.k]
        return Counter(self.y_train[nearest]).most_common(1)[0][0]

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict every row of X."""
        return np.array([self.predict_one(x) for x in X])


def main() -> None:
    """Compare scratch vs sklearn KNN, show scaling effect and choose k."""
    X, y = make_moons(n_samples=400, noise=0.3, random_state=0)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)

    scratch_acc = np.mean(KNNScratch(k=5).fit(X_tr, y_tr).predict(X_te) == y_te)
    sk_acc = KNeighborsClassifier(n_neighbors=5).fit(X_tr, y_tr).score(X_te, y_te)
    print(f"[*] Moons dataset, k=5 → scratch accuracy {scratch_acc:.3f} | "
          f"sklearn accuracy {sk_acc:.3f}")

    # --- Why scaling matters (wine features range from ~0.1 to ~1600) ---
    Xw, yw = load_wine(return_X_y=True)
    raw = cross_val_score(KNeighborsClassifier(), Xw, yw, cv=5).mean()
    scaled = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier()),
                             Xw, yw, cv=5).mean()
    print(f"[*] Wine dataset: KNN without scaling = {raw:.3f}, with scaling = {scaled:.3f}")

    # --- Choosing k with cross-validation ---
    print("\n[*] Choosing k on the moons data (5-fold CV accuracy):")
    ks = list(range(1, 42, 2))
    cv_scores, train_scores = [], []
    for k in ks:
        knn = KNeighborsClassifier(n_neighbors=k)
        cv_scores.append(cross_val_score(knn, X_tr, y_tr, cv=5).mean())
        train_scores.append(knn.fit(X_tr, y_tr).score(X_tr, y_tr))
    for k, s, t in zip(ks, cv_scores, train_scores):
        if k in (1, 3, 5, 9, 15, 25, 41):
            print(f"    k={k:<3} train={t:.3f}  cv={s:.3f}")
    best_k = ks[int(np.argmax(cv_scores))]
    final = KNeighborsClassifier(n_neighbors=best_k).fit(X_tr, y_tr)
    print(f"[*] Best k = {best_k} → test accuracy {final.score(X_te, y_te):.3f}")
    print("    (k=1 has perfect TRAIN accuracy but worse CV accuracy → over-fitting)")

    # --- Plots: k curve + decision boundaries ---
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(ks, train_scores, "o-", label="train")
    axes[0].plot(ks, cv_scores, "o-", label="cross-val")
    axes[0].axvline(best_k, ls="--", color="grey")
    axes[0].set(xlabel="k", ylabel="accuracy", title="Choosing k")
    axes[0].legend()
    xx, yy = np.meshgrid(np.linspace(-2, 3, 200), np.linspace(-1.5, 2, 200))
    grid = np.c_[xx.ravel(), yy.ravel()]
    for ax, k in zip(axes[1:], (1, best_k)):
        zz = KNeighborsClassifier(n_neighbors=k).fit(X_tr, y_tr).predict(grid)
        ax.contourf(xx, yy, zz.reshape(xx.shape), alpha=0.3, cmap="coolwarm")
        ax.scatter(X_tr[:, 0], X_tr[:, 1], c=y_tr, cmap="coolwarm", s=10)
        ax.set_title(f"Decision boundary, k={k}")
    fig.tight_layout()
    out = OUTPUT_DIR / "knn_choosing_k.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"[*] Plot saved to: {out}")


if __name__ == "__main__":
    main()
