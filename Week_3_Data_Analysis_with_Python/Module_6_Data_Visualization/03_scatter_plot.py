"""
Module 6 · Script 03 – Scatter Plot
===================================

Use a scatter plot to see the RELATIONSHIP between two numeric variables.
Covers: basic scatter, colour/size encoding, trend line with np.polyfit,
seaborn scatterplot with hue, and regplot.
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


def make_houses(n: int = 120) -> pd.DataFrame:
    """Synthetic, seeded house data: area vs price."""
    rng = np.random.default_rng(11)
    area = rng.uniform(500, 3000, n)
    bedrooms = np.clip((area / 700).round() + rng.integers(-1, 2, n), 1, 5).astype(int)
    city = rng.choice(["Delhi", "Pune", "Goa"], n)
    premium = pd.Series(city).map({"Delhi": 1.3, "Pune": 1.0, "Goa": 1.15}).to_numpy()
    price = (area * 4.5 * premium + rng.normal(0, 1200, n)) / 1000  # lakhs
    return pd.DataFrame({"area_sqft": area.round(), "bedrooms": bedrooms,
                         "city": city, "price_lakh": price.round(1)})


def basic_scatter(df: pd.DataFrame) -> None:
    """Scatter with a least-squares trend line."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(df["area_sqft"], df["price_lakh"], alpha=0.6, edgecolor="k")
    slope, intercept = np.polyfit(df["area_sqft"], df["price_lakh"], deg=1)
    xs = np.linspace(df["area_sqft"].min(), df["area_sqft"].max(), 100)
    ax.plot(xs, slope * xs + intercept, color="red", label=f"trend: y = {slope:.4f}x + {intercept:.1f}")
    ax.set_title("House price vs area (synthetic)")
    ax.set_xlabel("Area (sq ft)")
    ax.set_ylabel("Price (₹ lakh)")
    ax.legend()
    save(fig, "03_scatter_basic.png")
    r = df["area_sqft"].corr(df["price_lakh"])
    print(f"Pearson correlation area↔price: r = {r:.3f}")


def encoded_scatter(df: pd.DataFrame) -> None:
    """Encode extra variables with colour and marker size."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    points = ax.scatter(df["area_sqft"], df["price_lakh"], c=df["bedrooms"],
                        s=df["bedrooms"] * 25, cmap="viridis", alpha=0.7)
    fig.colorbar(points, ax=ax, label="Bedrooms")
    ax.set_title("Colour & size = number of bedrooms")
    ax.set_xlabel("Area (sq ft)")
    ax.set_ylabel("Price (₹ lakh)")
    save(fig, "03_scatter_colour_size.png")


def seaborn_scatter(df: pd.DataFrame) -> None:
    """Seaborn hue + regplot."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.scatterplot(data=df, x="area_sqft", y="price_lakh", hue="city", style="city", ax=axes[0])
    axes[0].set_title("sns.scatterplot(hue='city')")
    sns.regplot(data=df, x="area_sqft", y="price_lakh", ax=axes[1],
                scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
    axes[1].set_title("sns.regplot – scatter + regression line")
    fig.tight_layout()
    save(fig, "03_scatter_seaborn.png")


if __name__ == "__main__":
    houses = make_houses()
    print(houses.head())
    basic_scatter(houses)
    encoded_scatter(houses)
    seaborn_scatter(houses)
