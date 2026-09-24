"""
03_hierarchical_clustering_dendrogram.py
========================================
Week 4 · Module 4 – Hierarchical Clustering & Dendrogram

Agglomerative (bottom-up) hierarchical clustering:
    1. start with every point as its own cluster
    2. repeatedly MERGE the two closest clusters
    3. stop when everything is one cluster → the merge history is a tree
       (the DENDROGRAM). Cut the tree at a height to get k clusters.

"Closest clusters" depends on the LINKAGE:
    single   – distance between the two closest points  (chains, finds odd shapes)
    complete – distance between the two farthest points (compact clusters)
    average  – average of all pairwise distances
    ward     – merge that increases total WCSS the least (most like K-Means)

Run:
    python 03_hierarchical_clustering_dendrogram.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import adjusted_rand_score

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def tiny_worked_example() -> None:
    """Show the merge table for 5 one-dimensional points."""
    points = np.array([[1.0], [2.0], [6.0], [7.0], [15.0]])
    Z = linkage(points, method="single")
    print("[*] Tiny example: points 1, 2, 6, 7, 15 (single linkage)")
    print("    Each row = one merge: [cluster A, cluster B, distance, size of new cluster]")
    for i, row in enumerate(Z):
        print(f"    merge {i + 1}: {int(row[0])} + {int(row[1])} at distance "
              f"{row[2]:.1f} → new cluster of size {int(row[3])}")
    print("    (ids ≥ 5 refer to clusters created by earlier merges)\n")


def main() -> None:
    """Build a dendrogram, cut it, and compare linkages."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    tiny_worked_example()

    X, y = make_blobs(n_samples=60, centers=3, cluster_std=0.8, random_state=1)
    Z = linkage(X, method="ward")
    labels = fcluster(Z, t=3, criterion="maxclust")   # cut the tree into 3 clusters
    print(f"[*] Ward linkage, cut into 3 clusters → sizes {np.bincount(labels)[1:].tolist()}")
    print(f"    agreement with true blobs (ARI) = {adjusted_rand_score(y, labels):.3f}")
    # Reading the dendrogram: the LAST merges are the tall ones. A big jump in
    # merge height means two well-separated groups were forced together.
    print("    heights of the last 4 merges (clusters left after each merge):")
    for i in range(len(Z) - 4, len(Z)):
        print(f"      merge {i + 1:2d}: height {Z[i, 2]:6.2f} → {len(X) - (i + 1)} cluster(s)")
    print("    → cut just below a big jump (here between the 3-cluster and 2-cluster merges)")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
    dendrogram(Z, ax=ax1, color_threshold=Z[-3, 2] + 0.01, no_labels=True)
    ax1.axhline(Z[-3, 2] + 0.01, ls="--", color="grey", label="cut → 3 clusters")
    ax1.set(title="Dendrogram (ward linkage)", ylabel="merge distance")
    ax1.legend()
    ax2.scatter(X[:, 0], X[:, 1], c=labels, cmap="tab10")
    ax2.set_title("Resulting 3 clusters")
    fig.tight_layout()
    out = OUTPUT_DIR / "dendrogram.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"[*] Dendrogram saved to: {out}\n")

    # --- Compare linkages on non-convex data ---
    Xm, ym = make_moons(n_samples=300, noise=0.05, random_state=0)
    print("[*] Linkage comparison on the 'two moons' data (ARI, 1.0 = perfect):")
    for method in ("single", "complete", "average", "ward"):
        pred = AgglomerativeClustering(n_clusters=2, linkage=method).fit_predict(Xm)
        print(f"    {method:<9} ARI = {adjusted_rand_score(ym, pred):.3f}")
    print("    → single linkage follows the curved shapes; ward prefers round blobs.")


if __name__ == "__main__":
    main()
