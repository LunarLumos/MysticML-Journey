"""
Module 6 · Script 08 – Detecting Outliers
=========================================

Two classic rules:

1. IQR rule (robust, used by box plots)
       IQR = Q3 - Q1
       outlier if  x < Q1 - 1.5·IQR   or   x > Q3 + 1.5·IQR

2. Z-score rule (assumes roughly normal data)
       z = (x - mean) / std
       outlier if  |z| > 3        (sometimes 2.5 or 2)

Then: visualise them, and decide what to do (remove, cap, or keep).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def save(fig: plt.Figure, filename: str) -> None:
    """Save a figure into outputs/ and close it."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"💾 Saved -> {path}")


def make_delivery_times() -> pd.Series:
    """Synthetic delivery times (minutes) with planted outliers."""
    rng = np.random.default_rng(21)
    normal = rng.normal(35, 6, 300)
    outliers = np.array([2, 5, 90, 110, 125])
    return pd.Series(np.concatenate([normal, outliers]).round(1), name="minutes")


def iqr_outliers(s: pd.Series, k: float = 1.5) -> tuple[pd.Series, float, float]:
    """Return a boolean mask of outliers plus the lower/upper fences."""
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return (s < lower) | (s > upper), lower, upper


def zscore_outliers(s: pd.Series, threshold: float = 3.0) -> tuple[pd.Series, pd.Series]:
    """Return a boolean mask of outliers and the z-scores themselves."""
    z = (s - s.mean()) / s.std(ddof=0)
    return z.abs() > threshold, z


def report(s: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Print both methods' results."""
    iqr_mask, lower, upper = iqr_outliers(s)
    z_mask, z = zscore_outliers(s)
    scipy_z = stats.zscore(s)  # same thing via SciPy

    print(f"n = {len(s)}, mean = {s.mean():.1f}, median = {s.median():.1f}, std = {s.std():.1f}")
    print(f"\nIQR method: fences = [{lower:.1f}, {upper:.1f}]")
    print(f"  -> {iqr_mask.sum()} outliers: {sorted(s[iqr_mask].tolist())}")
    print("\nZ-score method (|z| > 3):")
    print(f"  -> {z_mask.sum()} outliers: {sorted(s[z_mask].tolist())}")
    print("  largest |z| values:", z.abs().nlargest(3).round(2).tolist())
    print("  scipy.stats.zscore agrees:", np.allclose(z, scipy_z))
    print("\nNote: IQR flags more points here – it isn't fooled by the outliers "
          "inflating the mean & std.")
    return iqr_mask, z_mask


def visualise(s: pd.Series, iqr_mask: pd.Series, z_mask: pd.Series) -> None:
    """Box plot, histogram with fences, and a scatter coloured by status."""
    _, lower, upper = iqr_outliers(s)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))

    sns.boxplot(x=s, ax=axes[0], color="lightblue")
    axes[0].set_title("Box plot – dots are IQR outliers")

    axes[1].hist(s, bins=40, color="grey", edgecolor="black")
    axes[1].axvline(lower, color="red", linestyle="--", label="IQR fences")
    axes[1].axvline(upper, color="red", linestyle="--")
    mean, std = s.mean(), s.std(ddof=0)
    axes[1].axvline(mean + 3 * std, color="purple", linestyle=":", label="mean ± 3σ")
    axes[1].axvline(mean - 3 * std, color="purple", linestyle=":")
    axes[1].set_title("Histogram with thresholds")
    axes[1].legend()

    status = np.select([iqr_mask & z_mask, iqr_mask], ["IQR + Z", "IQR only"], "normal")
    colours = {"normal": "tab:blue", "IQR only": "tab:orange", "IQR + Z": "tab:red"}
    for label, colour in colours.items():
        pts = s[status == label]
        axes[2].scatter(pts.index, pts, s=18, color=colour, label=label)
    axes[2].set_title("Each delivery, coloured by outlier status")
    axes[2].set_xlabel("Order #")
    axes[2].set_ylabel("Minutes")
    axes[2].legend()
    fig.tight_layout()
    save(fig, "08_outliers.png")


def handle(s: pd.Series, iqr_mask: pd.Series) -> None:
    """Three ways of dealing with outliers."""
    _, lower, upper = iqr_outliers(s)
    removed = s[~iqr_mask]
    capped = s.clip(lower, upper)            # "winsorising"
    median_filled = s.mask(iqr_mask, s.median())
    summary = pd.DataFrame({
        "original": s.describe(),
        "removed": removed.describe(),
        "capped": capped.describe(),
        "median_filled": median_filled.describe(),
    }).round(1)
    print("\nEffect of each strategy:\n", summary)
    print("\nOnly remove outliers that are ERRORS; real extreme values may be important!")


if __name__ == "__main__":
    times = make_delivery_times()
    iqr_flags, z_flags = report(times)
    visualise(times, iqr_flags, z_flags)
    handle(times, iqr_flags)
