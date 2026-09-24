"""
02_kmeans_elbow_silhouette.py
=============================
Week 4 · Module 4 – K-Means with scikit-learn & "Handling" K-Means

Practical issues when using K-Means and how to handle them:
  1. Choosing k           → Elbow method (WCSS) + Silhouette score
  2. Feature scales        → ALWAYS standardise (K-Means uses distances)
  3. Random initialisation → k-means++ init and n_init > 1
  4. Shape assumptions     → K-Means expects round, similar-size blobs

Silhouette of a point:  s = (b − a) / max(a, b)
    a = mean distance to points in its own cluster
    b = mean distance to points in the nearest OTHER cluster
    s ≈ 1 well clustered · s ≈ 0 on a border · s < 0 probably wrong cluster

Run:
    python 02_kmeans_elbow_silhouette.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine, make_blobs, make_moons
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def elbow_and_silhouette(X: np.ndarray, k_range=range(2, 11)) -> tuple[list, list]:
    """Return WCSS and silhouette score for every k."""
    wcss, sil = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        wcss.append(km.inertia_)
        sil.append(silhouette_score(X, km.labels_))
    return wcss, sil


def main() -> None:
    """Demonstrate choosing k and the main pitfalls of K-Means."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # ---------- 1. Choosing k ----------
    X, _ = make_blobs(n_samples=500, centers=5, cluster_std=1.0, random_state=11)
    ks = list(range(2, 11))
    wcss, sil = elbow_and_silhouette(X, ks)
    print("[*] Choosing k (data really has 5 blobs):")
    print(f"    {'k':>3}{'WCSS':>12}{'silhouette':>12}")
    for k, w, s in zip(ks, wcss, sil):
        print(f"    {k:>3}{w:>12.1f}{s:>12.3f}")
    best_k = ks[int(np.argmax(sil))]
    print(f"[*] Highest silhouette at k = {best_k}  (look for the 'elbow' in WCSS too)")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(ks, wcss, "o-")
    ax1.set(xlabel="k", ylabel="WCSS (inertia)", title="Elbow method")
    ax2.plot(ks, sil, "o-", color="green")
    ax2.axvline(best_k, ls="--", color="grey")
    ax2.set(xlabel="k", ylabel="silhouette score", title="Silhouette method")
    fig.tight_layout()
    out = OUTPUT_DIR / "elbow_silhouette.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"[*] Plot saved to: {out}")

    # ---------- 2. Scaling matters ----------
    Xw, yw = load_wine(return_X_y=True)
    raw = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(Xw)
    scaled = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(
        StandardScaler().fit_transform(Xw))
    print("\n[*] Wine data, agreement with the true cultivars (Adjusted Rand Index):")
    print(f"    without scaling: ARI = {adjusted_rand_score(yw, raw):.3f}")
    print(f"    with scaling   : ARI = {adjusted_rand_score(yw, scaled):.3f}")

    # ---------- 3. Initialisation ----------
    print("\n[*] Initialisation (same data, same k=5):")
    for seed in range(4):
        single = KMeans(n_clusters=5, init="random", n_init=1, random_state=seed).fit(X)
        print(f"    random init, n_init=1, seed={seed} → WCSS {single.inertia_:.1f}")
    multi = KMeans(n_clusters=5, init="k-means++", n_init=10, random_state=0).fit(X)
    print(f"    k-means++,  n_init=10          → WCSS {multi.inertia_:.1f}  (best, stable)")

    # ---------- 4. Shape limitation ----------
    Xm, ym = make_moons(n_samples=300, noise=0.05, random_state=0)
    moons = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(Xm)
    print("\n[*] Non-round clusters (two moons):")
    print(f"    K-Means ARI = {adjusted_rand_score(ym, moons):.3f} "
          "→ poor; try hierarchical (single linkage) or DBSCAN instead.")


if __name__ == "__main__":
    main()
