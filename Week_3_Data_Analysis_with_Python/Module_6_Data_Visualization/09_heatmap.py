"""
Module 6 · Script 09 – Heatmap
==============================

A heatmap colours each cell of a matrix by its value. Most common uses:
  * correlation matrix between numeric features (before ML!)
  * pivot tables (e.g. sales by weekday × hour)
  * missing-value maps

Covers: sns.heatmap with annot/cmap/center, masking the upper triangle,
pivot-table heatmap, missing-values heatmap and plain matplotlib imshow.
Uses scikit-learn's bundled Iris dataset if available (offline), else a
synthetic fallback.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def save(fig: plt.Figure, filename: str) -> None:
    """Save a figure into outputs/ and close it."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"💾 Saved -> {path}")


def load_numeric_data() -> pd.DataFrame:
    """Iris measurements (bundled with scikit-learn) or a synthetic fallback."""
    try:
        from sklearn.datasets import load_iris
        iris = load_iris(as_frame=True)
        print("Using scikit-learn's bundled Iris dataset.")
        return iris.frame.drop(columns="target")
    except ImportError:
        print("scikit-learn not installed – using synthetic data instead.")
        rng = np.random.default_rng(0)
        a = rng.normal(0, 1, 150)
        return pd.DataFrame({"a": a, "b": a * 0.8 + rng.normal(0, 0.5, 150),
                             "c": -a + rng.normal(0, 1, 150), "d": rng.normal(0, 1, 150)})


def correlation_heatmap(df: pd.DataFrame) -> None:
    """Full and lower-triangle correlation heatmaps."""
    corr = df.corr()
    print("\nCorrelation matrix:\n", corr.round(2))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1,
                center=0, square=True, linewidths=0.5, ax=axes[0])
    axes[0].set_title("Correlation heatmap")

    mask = np.triu(np.ones_like(corr, dtype=bool))  # hide upper triangle (duplicates)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1,
                center=0, square=True, linewidths=0.5, ax=axes[1])
    axes[1].set_title("Lower triangle only (no duplicates)")
    fig.tight_layout()
    save(fig, "09_heatmap_correlation.png")

    pairs = corr.where(~mask).stack().sort_values(key=abs, ascending=False)
    print("\nStrongest correlations:\n", pairs.head(3).round(3))


def pivot_heatmap() -> None:
    """Orders by weekday × hour – a pivot table shown as a heatmap."""
    rng = np.random.default_rng(4)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rows = []
    for d_idx, day in enumerate(days):
        for hour in range(9, 22):
            base = 20 + (15 if d_idx >= 5 else 0) + (25 if hour in (13, 14, 20, 21) else 0)
            rows.append({"day": day, "hour": hour, "orders": rng.poisson(base)})
    orders = pd.DataFrame(rows)
    table = orders.pivot_table(index="day", columns="hour", values="orders").reindex(days)
    fig, ax = plt.subplots(figsize=(11, 4))
    sns.heatmap(table, cmap="YlOrRd", annot=True, fmt=".0f", cbar_kws={"label": "orders"}, ax=ax)
    ax.set_title("Food orders by weekday × hour (synthetic)")
    save(fig, "09_heatmap_pivot.png")


def missing_values_heatmap() -> None:
    """Visualise where data is missing."""
    rng = np.random.default_rng(9)
    df = pd.DataFrame(rng.normal(size=(40, 6)), columns=[f"col_{i}" for i in range(6)])
    df = df.mask(rng.random(df.shape) < 0.12)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.heatmap(df.isna(), cbar=False, cmap="Greys", ax=ax)
    ax.set_title("Missing-values map (black = NaN)")
    save(fig, "09_heatmap_missing.png")
    print("\nMissing per column:", df.isna().sum().to_dict())


def matplotlib_imshow() -> None:
    """Heatmap with plain matplotlib (no seaborn)."""
    matrix = np.arange(1, 26).reshape(5, 5)
    fig, ax = plt.subplots(figsize=(4.5, 4))
    image = ax.imshow(matrix, cmap="viridis")
    fig.colorbar(image, ax=ax)
    for (i, j), val in np.ndenumerate(matrix):
        ax.text(j, i, val, ha="center", va="center", color="white")
    ax.set_title("matplotlib imshow")
    save(fig, "09_heatmap_imshow.png")


if __name__ == "__main__":
    features = load_numeric_data()
    correlation_heatmap(features)
    pivot_heatmap()
    missing_values_heatmap()
    matplotlib_imshow()
