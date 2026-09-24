"""
Module 1 · Script 06 – Different Mathematical Functions
=======================================================

Covers: rounding, powers/roots, exponentials & logarithms, trigonometry,
statistics, cumulative functions and handling NaN values.
"""

import numpy as np


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def rounding() -> None:
    """Different ways of rounding numbers."""
    section("1️⃣  Rounding")
    x = np.array([-2.7, -1.5, 0.2, 1.5, 2.5, 3.14159])
    print("x          :", x)
    print("np.round   :", np.round(x), "(banker's rounding: .5 -> even)")
    print("round(x, 2):", np.round(x, 2))
    print("np.floor   :", np.floor(x))
    print("np.ceil    :", np.ceil(x))
    print("np.trunc   :", np.trunc(x))
    print("np.abs     :", np.abs(x))


def powers_logs() -> None:
    """Powers, roots, exponentials and logarithms."""
    section("2️⃣  Powers, roots, exp and log")
    x = np.array([1, 2, 4, 8])
    print("x           :", x)
    print("np.power(x,3):", np.power(x, 3))
    print("np.sqrt     :", np.sqrt(x).round(3))
    print("np.cbrt     :", np.cbrt(x).round(3))
    print("np.exp      :", np.exp(x).round(2))
    print("np.log      :", np.log(x).round(3), "(natural log)")
    print("np.log2     :", np.log2(x))
    print("np.log10    :", np.log10(x).round(3))


def trigonometry() -> None:
    """Trig functions work in radians."""
    section("3️⃣  Trigonometry")
    degrees = np.array([0, 30, 45, 60, 90])
    radians = np.deg2rad(degrees)
    print("degrees :", degrees)
    print("radians :", radians.round(4))
    print("sin     :", np.sin(radians).round(4))
    print("cos     :", np.cos(radians).round(4))
    print("np.pi   :", np.pi, "| np.e:", np.e)


def statistics() -> None:
    """Descriptive statistics on a small dataset."""
    section("4️⃣  Statistics")
    heights = np.array([160, 172, 168, 181, 175, 158, 190])
    print("heights    :", heights)
    print("mean       :", heights.mean().round(2))
    print("median     :", np.median(heights))
    print("std / var  :", heights.std().round(2), "/", heights.var().round(2))
    print("min / max  :", heights.min(), "/", heights.max())
    print("range (ptp):", np.ptp(heights))
    print("quartiles  :", np.percentile(heights, [25, 50, 75]))
    weights = np.array([55, 70, 65, 85, 74, 52, 95])
    print("corrcoef(heights, weights):", np.corrcoef(heights, weights)[0, 1].round(3))


def cumulative_and_nan() -> None:
    """Cumulative sums/products and NaN-safe functions."""
    section("5️⃣  Cumulative functions")
    x = np.array([1, 2, 3, 4, 5])
    print("cumsum :", np.cumsum(x))
    print("cumprod:", np.cumprod(x))
    print("diff   :", np.diff(x))

    section("6️⃣  NaN-aware functions")
    data = np.array([4.0, np.nan, 6.0, 8.0])
    print("data            :", data)
    print("np.mean(data)   :", np.mean(data), "(NaN spreads!)")
    print("np.nanmean(data):", np.nanmean(data))
    print("np.nansum(data) :", np.nansum(data))
    print("np.isnan(data)  :", np.isnan(data))
    print("replace NaN     :", np.nan_to_num(data, nan=0.0))


if __name__ == "__main__":
    rounding()
    powers_logs()
    trigonometry()
    statistics()
    cumulative_and_nan()
