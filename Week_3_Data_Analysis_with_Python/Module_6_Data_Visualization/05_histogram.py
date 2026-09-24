"""
Module 6 · Script 05 – Histogram
================================

Use a histogram to see the DISTRIBUTION (shape) of one numeric variable.
Covers: bins, density, overlapping histograms, skewed data,
mean/median lines, and seaborn histplot with KDE.
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


def bins_matter(heights: np.ndarray) -> None:
    """Same data, different bin counts."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.5), sharey=False)
    for ax, bins in zip(axes, [5, 20, 80]):
        ax.hist(heights, bins=bins, color="tab:purple", edgecolor="black")
        ax.set_title(f"bins = {bins}")
        ax.set_xlabel("Height (cm)")
    axes[0].set_ylabel("Frequency")
    fig.suptitle("Choosing the number of bins changes the story")
    fig.tight_layout()
    save(fig, "05_hist_bins.png")


def overlapping(heights_m: np.ndarray, heights_f: np.ndarray) -> None:
    """Two groups on the same axes, with mean lines."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(heights_m, bins=30, alpha=0.55, label="Male", density=True)
    ax.hist(heights_f, bins=30, alpha=0.55, label="Female", density=True)
    ax.axvline(heights_m.mean(), color="tab:blue", linestyle="--")
    ax.axvline(heights_f.mean(), color="tab:orange", linestyle="--")
    ax.set_title("Overlapping histograms (density=True, dashed = mean)")
    ax.set_xlabel("Height (cm)")
    ax.set_ylabel("Density")
    ax.legend()
    save(fig, "05_hist_overlap.png")


def skewed() -> None:
    """Right-skewed data: mean is pulled to the right of the median."""
    rng = np.random.default_rng(2)
    incomes = rng.lognormal(mean=10.5, sigma=0.6, size=2000) / 1000  # thousands
    mean, median = incomes.mean(), np.median(incomes)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(incomes, bins=50, kde=True, ax=ax, color="tab:green")
    ax.axvline(mean, color="red", linestyle="--", label=f"mean {mean:.1f}k")
    ax.axvline(median, color="black", linestyle=":", label=f"median {median:.1f}k")
    ax.set_title("Right-skewed income distribution (seaborn histplot + KDE)")
    ax.set_xlabel("Income (thousands)")
    ax.legend()
    save(fig, "05_hist_skewed_kde.png")
    print(f"Skewed data: mean={mean:.1f}k > median={median:.1f}k "
          f"(skewness={pd.Series(incomes).skew():.2f})")


if __name__ == "__main__":
    generator = np.random.default_rng(42)
    male = generator.normal(175, 7, 1000)
    female = generator.normal(162, 6, 1000)
    everyone = np.concatenate([male, female])
    print(f"{everyone.size} synthetic heights, mean {everyone.mean():.1f} cm")
    bins_matter(everyone)
    overlapping(male, female)
    skewed()
