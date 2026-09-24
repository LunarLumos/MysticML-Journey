"""
Module 6 · Script 01 – Introduction to Data Visualization
=========================================================

Install the libraries (run once):

    pip install matplotlib seaborn

Covers: checking versions, the anatomy of a matplotlib figure
(Figure -> Axes -> title/labels/legend/ticks), the two APIs (pyplot vs
object-oriented), subplots, seaborn on top of matplotlib, and saving
figures to the outputs/ folder.
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def save(fig: plt.Figure, filename: str) -> None:
    """Save a figure into outputs/ and close it (keeps memory low)."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"💾 Saved -> {path}")


def versions() -> None:
    """Print library versions."""
    print("matplotlib:", matplotlib.__version__)
    print("seaborn   :", sns.__version__)
    print("backend   :", matplotlib.get_backend())


def anatomy() -> None:
    """Label every part of a figure."""
    x = np.arange(1, 8)
    y = np.array([3, 5, 4, 6, 8, 7, 9])
    fig, ax = plt.subplots(figsize=(7, 4))          # Figure = canvas, Axes = one plot
    ax.plot(x, y, marker="o", label="visitors (k)")  # the data
    ax.set_title("Anatomy of a plot")                # title
    ax.set_xlabel("Day of week")                     # x-axis label
    ax.set_ylabel("Visitors (thousands)")            # y-axis label
    ax.set_xticks(x, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])  # ticks
    ax.grid(alpha=0.3)                               # grid
    ax.legend()                                      # legend
    ax.annotate("peak", xy=(7, 9), xytext=(5.5, 8.6),
                arrowprops={"arrowstyle": "->"})     # annotation
    save(fig, "01_anatomy.png")


def two_apis() -> None:
    """pyplot (state-based) vs object-oriented API, side by side."""
    x = np.linspace(0, 2 * np.pi, 100)

    # pyplot style – quick & simple
    plt.figure(figsize=(5, 3))
    plt.plot(x, np.sin(x))
    plt.title("pyplot API: plt.plot(...)")
    save(plt.gcf(), "01_pyplot_api.png")

    # object-oriented style – recommended for anything with >1 plot
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    axes[0].plot(x, np.sin(x), color="tab:blue")
    axes[0].set_title("axes[0]: sin")
    axes[1].plot(x, np.cos(x), color="tab:orange")
    axes[1].set_title("axes[1]: cos")
    fig.suptitle("Object-oriented API: fig, axes = plt.subplots(1, 2)")
    fig.tight_layout()
    save(fig, "01_oo_api_subplots.png")


def seaborn_intro() -> None:
    """Seaborn works directly with DataFrames and adds nicer defaults."""
    rng = np.random.default_rng(1)
    df = pd.DataFrame({
        "hours_studied": rng.uniform(0, 10, 60).round(1),
        "group": rng.choice(["A", "B"], 60),
    })
    df["score"] = (40 + 5 * df["hours_studied"] + rng.normal(0, 6, 60)).round(1)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df, x="hours_studied", y="score", hue="group", ax=ax)
    ax.set_title("Seaborn: one line, DataFrame in, colour by group")
    save(fig, "01_seaborn_intro.png")
    sns.reset_defaults()


if __name__ == "__main__":
    versions()
    anatomy()
    two_apis()
    seaborn_intro()
    print("\nWhy visualise? Patterns, trends and outliers are far easier to SEE than to read.")
