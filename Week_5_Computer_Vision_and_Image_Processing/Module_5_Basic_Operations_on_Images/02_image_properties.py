"""
Module 5 - Accessing Image Properties
=====================================

    img.shape  (rows, cols, channels)   img.size  total values
    img.dtype  data type (uint8)        img.ndim  2 = gray, 3 = colour
Plus some quick statistics: mean colour, min/max and their locations,
and a histogram of pixel intensities.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402


def properties(img):
    """Return a dict of the most common image properties."""
    return {
        "shape": img.shape,
        "height": img.shape[0],
        "width": img.shape[1],
        "channels": 1 if img.ndim == 2 else img.shape[2],
        "size (values)": img.size,
        "dtype": img.dtype,
        "aspect ratio": round(img.shape[1] / img.shape[0], 3),
        "memory (KB)": round(img.nbytes / 1024, 1),
    }


if __name__ == "__main__":
    base_parser("Image properties").parse_args()
    out = output_dir(__file__)
    img = cv2.imread(str(get_image_path("china.jpg")))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for name, value in properties(img).items():
        print(f"  {name:<15}: {value}")

    b, g, r = cv2.mean(img)[:3]
    print(f"\n  mean colour (B, G, R) = ({b:.1f}, {g:.1f}, {r:.1f})")
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
    print(f"  darkest pixel  {min_val:.0f} at (x, y) = {min_loc}")
    print(f"  brightest pixel {max_val:.0f} at (x, y) = {max_loc}")

    # Histogram = how many pixels have each intensity 0..255
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, col in enumerate("bgr"):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        ax.plot(hist, color=col, label=f"{col.upper()} channel")
    ax.set_xlabel("pixel value"); ax.set_ylabel("number of pixels")
    ax.set_title("Colour histogram of china.jpg"); ax.legend()
    fig.savefig(out / "histogram.png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved -> {out / 'histogram.png'}")
