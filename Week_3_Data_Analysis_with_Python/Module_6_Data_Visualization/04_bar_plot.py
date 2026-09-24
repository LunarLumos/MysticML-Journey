"""
Module 6 · Script 04 – Bar Plot
===============================

Use a bar plot to COMPARE a number across categories.
Covers: vertical & horizontal bars, value labels, grouped bars,
stacked bars, pandas .plot.bar(), seaborn barplot / countplot.
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


LANGUAGES = ["Python", "JavaScript", "Java", "C++", "Go"]
USERS_2024 = [68, 62, 35, 23, 14]
USERS_2025 = [74, 63, 33, 24, 17]


def simple_bars() -> None:
    """Vertical and horizontal bar charts with value labels."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    bars = axes[0].bar(LANGUAGES, USERS_2025, color="tab:blue")
    axes[0].bar_label(bars, fmt="%d%%")
    axes[0].set_title("Vertical bar – % developers using (2025, illustrative)")
    axes[0].set_ylabel("% of developers")

    order = np.argsort(USERS_2025)
    hbars = axes[1].barh(np.array(LANGUAGES)[order], np.array(USERS_2025)[order], color="tab:green")
    axes[1].bar_label(hbars, padding=3)
    axes[1].set_title("Horizontal bar – sorted (long labels read better)")
    fig.tight_layout()
    save(fig, "04_bar_simple.png")


def grouped_and_stacked() -> None:
    """Compare two years side by side and stacked."""
    x = np.arange(len(LANGUAGES))
    width = 0.38
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar(x - width / 2, USERS_2024, width, label="2024")
    axes[0].bar(x + width / 2, USERS_2025, width, label="2025")
    axes[0].set_xticks(x, LANGUAGES)
    axes[0].set_title("Grouped bars")
    axes[0].legend()

    axes[1].bar(LANGUAGES, USERS_2024, label="2024")
    axes[1].bar(LANGUAGES, USERS_2025, bottom=USERS_2024, label="2025")
    axes[1].set_title("Stacked bars")
    axes[1].legend()
    fig.tight_layout()
    save(fig, "04_bar_grouped_stacked.png")


def pandas_and_seaborn() -> None:
    """pandas .plot.bar and seaborn barplot/countplot."""
    df = pd.DataFrame({"2024": USERS_2024, "2025": USERS_2025}, index=LANGUAGES)
    ax = df.plot.bar(rot=0, figsize=(7, 4), title="pandas: df.plot.bar()")
    save(ax.get_figure(), "04_bar_pandas.png")

    rng = np.random.default_rng(5)
    orders = pd.DataFrame({
        "day": rng.choice(["Mon", "Tue", "Wed", "Thu", "Fri"], 200),
        "amount": rng.gamma(2, 150, 200).round(),
    })
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.barplot(data=orders, x="day", y="amount", order=day_order, ax=axes[0],
                estimator="mean", errorbar="sd")
    axes[0].set_title("sns.barplot – mean order amount ± std")
    sns.countplot(data=orders, x="day", order=day_order, ax=axes[1])
    axes[1].set_title("sns.countplot – number of orders per day")
    fig.tight_layout()
    save(fig, "04_bar_seaborn.png")


if __name__ == "__main__":
    simple_bars()
    grouped_and_stacked()
    pandas_and_seaborn()
