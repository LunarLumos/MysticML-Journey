"""
Module 5 - Image Sharpening
===========================

Sharpening boosts the difference between a pixel and its neighbours.

1) Sharpening kernel with cv2.filter2D:
        [[ 0, -1,  0],
         [-1,  5, -1],        centre weight 5, neighbours -1  (sum = 1,
         [ 0, -1,  0]]        so overall brightness stays the same)

2) Unsharp masking (what photo editors do):
        sharp = original + amount * (original - blurred)
      = cv2.addWeighted(original, 1 + amount, blurred, -amount, 0)
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402


KERNELS = {
    "basic (4-neighbour)": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32),
    "strong (8-neighbour)": np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], np.float32),
}


def unsharp_mask(img, sigma=2.0, amount=1.5):
    """Classic unsharp masking."""
    blurred = cv2.GaussianBlur(img, (0, 0), sigma)
    return cv2.addWeighted(img, 1 + amount, blurred, -amount, 0)


def sharpness(img):
    """Variance of the Laplacian - a popular 'how sharp is this image' score."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


if __name__ == "__main__":
    args = base_parser("Image sharpening").parse_args()
    out = output_dir(__file__)
    original = cv2.imread(str(get_image_path("flower.jpg")))
    soft = cv2.GaussianBlur(original, (5, 5), 0)           # start from a slightly blurry photo

    results = {"blurry input": soft}
    for name, kernel in KERNELS.items():
        results[f"kernel {name}"] = cv2.filter2D(soft, -1, kernel)
    results["unsharp mask"] = unsharp_mask(soft)

    print("Sharpness score (variance of Laplacian, higher = sharper):")
    print(f"  {'original photo':<30} {sharpness(original):8.1f}")
    for name, img in results.items():
        print(f"  {name:<30} {sharpness(img):8.1f}")

    grid = make_grid(list(results.values()), list(results.keys()), cols=2, cell=(360, 240))
    save_image(out, "sharpening.png", grid)
    show_images({"Sharpening": grid}, args.show)
