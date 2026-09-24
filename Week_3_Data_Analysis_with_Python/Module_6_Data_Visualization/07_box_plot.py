"""
Module 6 · Script 07 – Box Plot
===============================

A box plot summarises a distribution with 5 numbers:
    min-whisker, Q1 (25%), median (50%), Q3 (75%), max-whisker
Whiskers reach up to 1.5 × IQR; points beyond them are drawn as outliers.

Covers: matplotlib boxplot, printing the 5-number summary, comparing
groups with seaborn boxplot, and violin plots.
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


def make_scores() -> pd.DataFrame:
    """Synthetic exam scores for three classes (with a few outliers)."""
    rng = np.random.default_rng(8)
    frames = []
    for name, mean, std in [("Class A", 72, 8), ("Class B", 65, 12), ("Class C", 80, 5)]:
        scores = rng.normal(mean, std, 40)
        frames.append(pd.DataFrame({"class": name, "score": scores}))
    df = pd.concat(frames, ignore_index=True)
    df.loc[[3, 45, 90], "score"] = [25, 99, 45]  # plant outliers
    df["score"] = df["score"].clip(0, 100).round(1)
    return df


def five_number_summary(scores: pd.Series) -> None:
    """Print the numbers a box plot draws."""
    q1, median, q3 = scores.quantile([0.25, 0.5, 0.75])
    iqr = q3 - q1
    print("5-number summary (all classes):")
    print(f"  min={scores.min()}  Q1={q1:.1f}  median={median:.1f}  Q3={q3:.1f}  max={scores.max()}")
    print(f"  IQR={iqr:.1f} -> whisker limits [{q1 - 1.5 * iqr:.1f}, {q3 + 1.5 * iqr:.1f}]")


def matplotlib_box(df: pd.DataFrame) -> None:
    """One box per class, drawn with plain matplotlib."""
    groups = [g["score"].to_numpy() for _, g in df.groupby("class")]
    labels = sorted(df["class"].unique())
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.boxplot(groups, tick_labels=labels, patch_artist=True, notch=True,
               boxprops={"facecolor": "lightsteelblue"})
    ax.set_title("matplotlib boxplot (notch = CI of median)")
    ax.set_ylabel("Score")
    save(fig, "07_box_matplotlib.png")


def seaborn_box_violin(df: pd.DataFrame) -> None:
    """Seaborn box + strip overlay and violin plot."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.boxplot(data=df, x="class", y="score", hue="class", ax=axes[0], legend=False)
    sns.stripplot(data=df, x="class", y="score", color="black", size=3, alpha=0.5, ax=axes[0])
    axes[0].set_title("sns.boxplot + raw points")
    sns.violinplot(data=df, x="class", y="score", hue="class", inner="quartile",
                   ax=axes[1], legend=False)
    axes[1].set_title("sns.violinplot – box plot + distribution shape")
    fig.tight_layout()
    save(fig, "07_box_seaborn_violin.png")


if __name__ == "__main__":
    data = make_scores()
    print(data.groupby("class")["score"].describe().round(1))
    five_number_summary(data["score"])
    matplotlib_box(data)
    seaborn_box_violin(data)
