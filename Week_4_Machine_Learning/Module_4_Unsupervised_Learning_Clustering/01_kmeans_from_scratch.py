"""
01_kmeans_from_scratch.py
=========================
Week 4 · Module 4 – Maths behind K-Means Clustering: Centroids

K-Means minimises the WITHIN-CLUSTER SUM OF SQUARES (WCSS, a.k.a. inertia):

    J = Σ_k Σ_{x ∈ C_k} || x − μ_k ||²

Lloyd's algorithm alternates two steps until nothing changes:
    1. ASSIGN : put every point in the cluster of its nearest centroid
                   c(i) = argmin_k || x_i − μ_k ||²
    2. UPDATE : move every centroid to the MEAN of its points
                   μ_k = (1 / |C_k|) Σ_{x ∈ C_k} x

Each step can only lower J, so the algorithm always converges (but possibly to
a local minimum → run it several times from different starts, "n_init").

Run:
    python 01_kmeans_from_scratch.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def kmeans_scratch(X: np.ndarray, k: int, max_iter: int = 100, seed: int = 0,
                   verbose: bool = True) -> tuple[np.ndarray, np.ndarray, float, list]:
    """Run Lloyd's K-Means. Returns (labels, centroids, inertia, centroid_history)."""
    rng = np.random.default_rng(seed)
    centroids = X[rng.choice(len(X), size=k, replace=False)]  # random initial centroids
    history = [centroids.copy()]
    for it in range(1, max_iter + 1):
        # --- 1. ASSIGN: distance of every point to every centroid (n × k matrix) ---
        distances = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
        labels = distances.argmin(axis=1)
        # --- 2. UPDATE: centroid = mean of its assigned points ---
        new_centroids = np.array([
            X[labels == j].mean(axis=0) if np.any(labels == j) else centroids[j]
            for j in range(k)
        ])
        inertia = float(np.sum((X - new_centroids[labels]) ** 2))
        if verbose:
            print(f"    iteration {it:2d}: WCSS = {inertia:10.2f}")
        history.append(new_centroids.copy())
        if np.allclose(new_centroids, centroids):
            if verbose:
                print(f"    converged after {it} iterations ✔")
            break
        centroids = new_centroids
    return labels, new_centroids, inertia, history


def main() -> None:
    """Run scratch K-Means, compare with sklearn, and plot centroid movement."""
    X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.9, random_state=3)

    # A tiny worked example of the centroid formula
    pts = np.array([[1, 2], [2, 3], [3, 1]])
    print(f"[*] Centroid of {pts.tolist()} = mean = {pts.mean(axis=0).round(3).tolist()}\n")

    print("[*] Scratch K-Means (k=4):")
    labels, centroids, inertia, history = kmeans_scratch(X, k=4)

    sk = KMeans(n_clusters=4, n_init=10, random_state=0).fit(X)
    print(f"\n[*] WCSS scratch = {inertia:.2f} | WCSS sklearn = {sk.inertia_:.2f}")
    print("[*] Centroids (scratch, sorted):")
    print(np.round(centroids[np.argsort(centroids[:, 0])], 3))
    print("[*] Centroids (sklearn, sorted):")
    print(np.round(sk.cluster_centers_[np.argsort(sk.cluster_centers_[:, 0])], 3))

    # Bad initialisation → local minimum: why n_init matters
    print("\n[*] Effect of random initialisation (different seeds):")
    for seed in range(5):
        _, _, wcss, _ = kmeans_scratch(X, k=4, seed=seed, verbose=False)
        print(f"    seed {seed}: final WCSS = {wcss:.2f}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    plt.figure(figsize=(6, 5))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="tab10", s=12, alpha=0.6)
    path = np.array(history)  # shape (iterations, k, 2)
    for j in range(path.shape[1]):
        plt.plot(path[:, j, 0], path[:, j, 1], "k.-", lw=1)
    plt.scatter(centroids[:, 0], centroids[:, 1], c="red", marker="X", s=200,
                label="final centroids")
    plt.title("K-Means from scratch – centroid paths")
    plt.legend()
    out = OUTPUT_DIR / "kmeans_scratch_centroids.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"\n[*] Plot saved to: {out}")


if __name__ == "__main__":
    main()
