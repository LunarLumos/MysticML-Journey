"""
Module 6 · Script 06 – Pie Chart
================================

Use a pie (or donut) chart to show PARTS OF A WHOLE – best with few
categories (≤ 5–6). Covers: percentages, explode, start angle, donut,
grouping small slices into "Other", and pandas .plot.pie().
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def save(fig: plt.Figure, filename: str) -> None:
    """Save a figure into outputs/ and close it."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"💾 Saved -> {path}")


# Illustrative monthly household budget (₹)
BUDGET = pd.Series({"Rent": 18000, "Food": 9000, "Transport": 3500, "Savings": 8000,
                    "Fun": 2500, "Phone": 600, "Books": 400})


def group_small(series: pd.Series, threshold: float = 0.05) -> pd.Series:
    """Merge slices smaller than `threshold` of the total into 'Other'."""
    share = series / series.sum()
    big = series[share >= threshold]
    other = series[share < threshold].sum()
    return pd.concat([big, pd.Series({"Other": other})]) if other else big


def basic_pie(budget: pd.Series) -> None:
    """Classic pie with percentages and an exploded slice."""
    explode = [0.08 if label == "Savings" else 0 for label in budget.index]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(budget, labels=budget.index, autopct="%1.1f%%", startangle=90,
           explode=explode, shadow=False, wedgeprops={"edgecolor": "white"})
    ax.set_title("Monthly budget (small slices grouped as 'Other')")
    ax.axis("equal")  # keep it a circle
    save(fig, "06_pie_basic.png")


def donut(budget: pd.Series) -> None:
    """A donut chart is a pie with a hole – the centre can hold a total."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(budget, labels=budget.index, autopct="%1.0f%%", pctdistance=0.8,
           startangle=90, wedgeprops={"width": 0.4, "edgecolor": "white"})
    ax.text(0, 0, f"₹{budget.sum():,}\ntotal", ha="center", va="center", fontsize=13)
    ax.set_title("Donut chart")
    save(fig, "06_pie_donut.png")


def pandas_pie() -> None:
    """pandas can draw a pie directly from value_counts()."""
    payments = pd.Series(["UPI"] * 55 + ["Card"] * 25 + ["Cash"] * 15 + ["Wallet"] * 5)
    ax = payments.value_counts().plot.pie(autopct="%1.0f%%", figsize=(5, 5),
                                          title="Payment methods (pandas .plot.pie)")
    ax.set_ylabel("")
    save(ax.get_figure(), "06_pie_pandas.png")


if __name__ == "__main__":
    grouped = group_small(BUDGET)
    print("Budget after grouping small slices:\n", grouped)
    basic_pie(grouped)
    donut(grouped)
    pandas_pie()
    print("\nTip: if slices are similar in size, a bar chart is easier to compare.")
