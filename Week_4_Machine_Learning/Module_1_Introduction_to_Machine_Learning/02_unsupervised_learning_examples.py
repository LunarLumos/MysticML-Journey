"""
02_unsupervised_learning_examples.py
====================================
Week 4 · Module 1 – Machine Learning Types → UNSUPERVISED LEARNING

Unsupervised learning = the data has NO labels. The algorithm must discover
structure on its own. Two classic tasks:

  • Clustering                -> group similar samples  (K-Means)
  • Dimensionality reduction  -> compress many features into a few (PCA)

Run:
    python 02_unsupervised_learning_examples.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits, make_blobs
from sklearn.decomposition import PCA

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


# ---------------------------------------------------------------
# Example 1: Clustering shoppers (no labels given!)
# ---------------------------------------------------------------
def clustering_example() -> None:
    """Find 3 groups of shoppers using only (annual spend, visits per month)."""
    print("=" * 60)
    print("Example 1 · Clustering shoppers with K-Means")
    print("=" * 60)
    X, _ = make_blobs(n_samples=150, centers=[[20, 2], [60, 8], [90, 3]],
                      cluster_std=[5, 6, 5], random_state=7)
    # NOTE: we throw away the true labels (_) – the model never sees them.
    kmeans = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)
    for i, center in enumerate(kmeans.cluster_centers_):
        size = np.sum(kmeans.labels_ == i)
        print(f"[+] Group {i}: {size:3d} shoppers | avg spend ≈ {center[0]:.0f}k, "
              f"visits ≈ {center[1]:.1f}/month")

    OUTPUT_DIR.mkdir(exist_ok=True)
    plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap="viridis", s=20)
    plt.scatter(*kmeans.cluster_centers_.T, c="red", marker="X", s=200, label="centroids")
    plt.xlabel("Annual spend (k)")
    plt.ylabel("Visits per month")
    plt.title("Unsupervised: K-Means found 3 shopper groups")
    plt.legend()
    out = OUTPUT_DIR / "unsupervised_clusters.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"[*] Plot saved to: {out}\n")


# ---------------------------------------------------------------
# Example 2: Dimensionality reduction on handwritten digits
# ---------------------------------------------------------------
def pca_example() -> None:
    """Compress 64-pixel digit images into 2 numbers with PCA."""
    print("=" * 60)
    print("Example 2 · Dimensionality reduction with PCA (64 → 2 features)")
    print("=" * 60)
    digits = load_digits()
    pca = PCA(n_components=2).fit(digits.data)
    X_2d = pca.transform(digits.data)
    kept = pca.explained_variance_ratio_.sum()
    print(f"[*] Original shape: {digits.data.shape}  ->  reduced shape: {X_2d.shape}")
    print(f"[*] Variance kept by 2 components: {kept:.1%}")
    # PCA never used the labels; we only use them to COLOUR the plot afterwards.
    plt.scatter(X_2d[:, 0], X_2d[:, 1], c=digits.target, cmap="tab10", s=8)
    plt.colorbar(label="digit (only used for colouring)")
    plt.title("PCA projection of the digits dataset")
    out = OUTPUT_DIR / "unsupervised_pca_digits.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"[*] Plot saved to: {out}\n")


def main() -> None:
    """Run both unsupervised-learning examples."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    clustering_example()
    pca_example()


if __name__ == "__main__":
    main()
