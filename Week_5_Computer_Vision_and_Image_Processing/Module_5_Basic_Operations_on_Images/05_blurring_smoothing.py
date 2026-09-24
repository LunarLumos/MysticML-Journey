"""
Module 5 - Blurring | Image Smoothing
=====================================

Blurring = replacing each pixel by a (weighted) average of its neighbours,
computed by sliding a small KERNEL over the image (convolution).

| Function                      | Kernel / idea                        | Good for              |
|-------------------------------|--------------------------------------|-----------------------|
| cv2.blur(img, (k, k))         | plain average (box filter)           | simple smoothing      |
| cv2.GaussianBlur(img,(k,k),s) | Gaussian weights, centre counts most | general noise         |
| cv2.medianBlur(img, k)        | median of neighbours                 | salt & pepper noise   |
| cv2.bilateralFilter(img,d,..) | averages only SIMILAR colours        | smooth + keep edges   |
| cv2.filter2D(img, -1, K)      | ANY custom kernel                    | experiments           |
Kernel sizes must be odd (3, 5, 7 ...).
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402



def add_salt_and_pepper(img, amount=0.04, seed=0):
    """Return a copy of img with random black/white pixels (noise)."""
    rng = np.random.default_rng(seed)
    noisy = img.copy()
    r = rng.random(img.shape[:2])
    noisy[r < amount / 2] = 0
    noisy[r > 1 - amount / 2] = 255
    return noisy


if __name__ == "__main__":
    parser = base_parser("Blurring and smoothing")
    parser.add_argument("--ksize", type=int, default=7, help="odd kernel size (default 7)")
    args = parser.parse_args()
    k = args.ksize if args.ksize % 2 else args.ksize + 1
    out = output_dir(__file__)

    img = cv2.imread(str(get_image_path("flower.jpg")))
    noisy = add_salt_and_pepper(img)
    box_kernel = np.ones((k, k), np.float32) / (k * k)          # what cv2.blur uses

    results = {
        "noisy input": noisy,
        f"average blur {k}x{k}": cv2.blur(noisy, (k, k)),
        "filter2D same kernel": cv2.filter2D(noisy, -1, box_kernel),
        f"Gaussian {k}x{k}": cv2.GaussianBlur(noisy, (k, k), 0),
        f"median k={k}": cv2.medianBlur(noisy, k),
        "bilateral (on clean img)": cv2.bilateralFilter(img, 9, 75, 75),
    }
    # How well did each filter remove the noise?  (lower = closer to the clean image)
    print(f"Mean absolute error vs the clean image (kernel {k}):")
    for name, res in results.items():
        print(f"  {name:<26} {np.abs(res.astype(int) - img.astype(int)).mean():6.2f}")

    grid = make_grid(list(results.values()), list(results.keys()), cols=3)
    save_image(out, "blurring.png", grid)
    show_images({"Blurring": grid}, args.show)
