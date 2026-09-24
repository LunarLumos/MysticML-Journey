"""
customer_segmentation.py
========================
Week 4 · Module 4 – Project: Customers Clustering

Business question: "Which groups of customers do we have, so marketing can
target each group differently?"

Pipeline
--------
1. Load data/customers.csv (synthetic – see generate_data.py)
2. Select features: AnnualIncome_k, SpendingScore  (+ standardise)
3. Choose k with the elbow method and silhouette score
4. Fit K-Means with the chosen k and PROFILE each segment
5. Cross-check with hierarchical clustering (ward) + dendrogram
6. Save plots and a CSV with each customer's segment to outputs/

Run:
    python customer_segmentation.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "customers.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
FEATURES = ["AnnualIncome_k", "SpendingScore"]


def load_data() -> pd.DataFrame:
    """Load the customers CSV, generating it if missing."""
    if not DATA_PATH.exists():
        from generate_data import generate
        DATA_PATH.parent.mkdir(exist_ok=True)
        generate().to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)


def name_segment(income: float, score: float, inc_mid: float, sc_mid: float) -> str:
    """Give a human-friendly marketing name to a cluster centre."""
    hi_inc, hi_sc = income > inc_mid + 15, score > sc_mid + 15
    lo_inc, lo_sc = income < inc_mid - 15, score < sc_mid - 15
    if hi_inc and hi_sc:
        return "VIP big spenders"
    if hi_inc and lo_sc:
        return "Careful high earners"
    if lo_inc and hi_sc:
        return "Young impulsive buyers"
    if lo_inc and lo_sc:
        return "Budget-conscious"
    return "Average customers"


def choose_k(X: np.ndarray) -> int:
    """Print elbow/silhouette table, save plot, return the best-silhouette k."""
    ks = range(2, 11)
    wcss, sil = [], []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        wcss.append(km.inertia_)
        sil.append(silhouette_score(X, km.labels_))
    print(f"    {'k':>3}{'WCSS':>10}{'silhouette':>12}")
    for k, w, s in zip(ks, wcss, sil):
        print(f"    {k:>3}{w:>10.1f}{s:>12.3f}")
    best = list(ks)[int(np.argmax(sil))]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
    ax1.plot(list(ks), wcss, "o-")
    ax1.set(title="Elbow method", xlabel="k", ylabel="WCSS")
    ax2.plot(list(ks), sil, "o-", color="green")
    ax2.set(title="Silhouette score", xlabel="k")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "customers_choose_k.png", dpi=110)
    plt.close(fig)
    return best


def main() -> None:
    """Run the customer segmentation project."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = load_data()
    print("=" * 64)
    print("Customer Segmentation")
    print("=" * 64)
    print(f"[*] {len(df)} customers | columns: {list(df.columns)}")
    print(df[["Age", *FEATURES]].describe().round(1).loc[["mean", "std", "min", "max"]])

    X = StandardScaler().fit_transform(df[FEATURES])

    print("\n[*] Choosing the number of segments:")
    k = choose_k(X)
    print(f"[*] Chosen k = {k}")

    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    df["Segment"] = km.labels_

    profile = df.groupby("Segment").agg(
        Customers=("CustomerID", "count"), Age=("Age", "mean"),
        Income_k=("AnnualIncome_k", "mean"), Score=("SpendingScore", "mean"),
        PctFemale=("Gender", lambda g: (g == "Female").mean() * 100),
    ).round(1)
    inc_mid, sc_mid = df["AnnualIncome_k"].mean(), df["SpendingScore"].mean()
    profile["Name"] = [name_segment(r.Income_k, r.Score, inc_mid, sc_mid)
                       for r in profile.itertuples()]
    print("\n[*] Segment profiles:")
    print(profile.to_string())

    # --- Cross-check with hierarchical clustering ---
    agg = AgglomerativeClustering(n_clusters=k, linkage="ward").fit_predict(X)
    print(f"\n[*] Agreement K-Means vs hierarchical (ARI): "
          f"{adjusted_rand_score(km.labels_, agg):.3f}  (1.0 = identical)")

    # --- Plots ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    for seg, row in profile.iterrows():
        part = df[df["Segment"] == seg]
        ax1.scatter(part["AnnualIncome_k"], part["SpendingScore"], s=20,
                    label=f"{seg}: {row['Name']}")
    centres = df.groupby("Segment")[FEATURES].mean()
    ax1.scatter(centres["AnnualIncome_k"], centres["SpendingScore"], c="black",
                marker="X", s=150)
    ax1.set(xlabel="Annual income (k$)", ylabel="Spending score", title="K-Means segments")
    ax1.legend(fontsize=8)
    dendrogram(linkage(X, method="ward"), ax=ax2, no_labels=True, truncate_mode="level", p=6)
    ax2.set(title="Dendrogram (ward, truncated)", ylabel="merge distance")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "customer_segments.png", dpi=110)
    plt.close(fig)

    out_csv = OUTPUT_DIR / "customers_with_segments.csv"
    df.merge(profile[["Name"]], left_on="Segment", right_index=True).to_csv(out_csv, index=False)
    print(f"[*] Plots and {out_csv.name} saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
