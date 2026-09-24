"""
Module 6 · Script 02 – Line Plot
================================

Use a line plot for data that changes over an ordered axis (usually time).
Covers: basic line, several lines + styles, markers, pandas .plot(),
seaborn.lineplot with confidence band.
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


def monthly_sales() -> pd.DataFrame:
    """Synthetic, seeded monthly sales for three products."""
    rng = np.random.default_rng(7)
    months = pd.date_range("2025-01-01", periods=12, freq="MS")
    trend = np.linspace(100, 180, 12)
    return pd.DataFrame({
        "month": months,
        "laptops": (trend + rng.normal(0, 8, 12)).round(),
        "phones": (trend * 1.4 + 20 * np.sin(np.arange(12) / 2) + rng.normal(0, 8, 12)).round(),
        "tablets": (np.linspace(80, 60, 12) + rng.normal(0, 5, 12)).round(),
    })


def matplotlib_lines(df: pd.DataFrame) -> None:
    """Several styled lines on one Axes."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df["month"], df["laptops"], marker="o", label="Laptops")
    ax.plot(df["month"], df["phones"], marker="s", linestyle="--", label="Phones")
    ax.plot(df["month"], df["tablets"], marker="^", linestyle=":", label="Tablets")
    ax.set_title("Monthly units sold – 2025 (synthetic)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Units")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    save(fig, "02_line_matplotlib.png")


def pandas_line(df: pd.DataFrame) -> None:
    """pandas has plotting built in (uses matplotlib underneath)."""
    ax = df.set_index("month")[["laptops", "phones"]].cumsum().plot(
        figsize=(8, 4), title="Cumulative units (pandas .plot())")
    ax.set_ylabel("Cumulative units")
    save(ax.get_figure(), "02_line_pandas_cumulative.png")


def seaborn_line() -> None:
    """seaborn.lineplot averages repeated x values and draws a 95% CI band."""
    rng = np.random.default_rng(3)
    days = np.repeat(np.arange(1, 31), 5)  # 5 readings per day
    temps = 25 + 5 * np.sin(days / 5) + rng.normal(0, 1.5, days.size)
    df = pd.DataFrame({"day": days, "temp_c": temps})
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=df, x="day", y="temp_c", ax=ax, errorbar=("ci", 95))
    ax.set_title("Seaborn lineplot – mean temperature with 95% CI")
    save(fig, "02_line_seaborn_ci.png")


if __name__ == "__main__":
    sales = monthly_sales()
    print(sales.head())
    matplotlib_lines(sales)
    pandas_line(sales)
    seaborn_line()
