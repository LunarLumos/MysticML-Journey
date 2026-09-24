"""
Module 5 - Accessing and Modifying Pixel Values
===============================================

    px = img[y, x]          -> [B, G, R]  (ROW first, then COLUMN!)
    b  = img[y, x, 0]       -> just the blue value
    img[y, x] = [0, 0, 255] -> paint one pixel red
    img[y1:y2, x1:x2] = ... -> paint a whole block (slicing, very fast)

Tip: avoid Python for-loops over pixels - NumPy slicing/boolean masks are
hundreds of times faster. (img.item()/itemset() were removed in NumPy 2.)
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402


def per_pixel_loop(img):
    """SLOW way: invert a small image pixel by pixel (for teaching only)."""
    out = img.copy()
    for y in range(out.shape[0]):
        for x in range(out.shape[1]):
            out[y, x] = 255 - out[y, x]
    return out


if __name__ == "__main__":
    args = base_parser("Access and modify pixels").parse_args()
    out = output_dir(__file__)
    img = cv2.imread(str(get_image_path("shapes.png")))

    # --- Reading pixels --------------------------------------------------------
    y, x = 100, 400                                   # centre of the green circle
    print(f"img[{y}, {x}]      = {img[y, x]}   (B, G, R)")
    print(f"img[{y}, {x}, 1]   = {img[y, x, 1]}   (green channel only)")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"gray[{y}, {x}]     = {gray[y, x]}   (single brightness value)")

    # --- Modifying single pixels and blocks ------------------------------------
    edited = img.copy()                               # copy() so the original stays intact
    edited[y, x] = [0, 0, 255]                        # one red pixel (hard to see!)
    edited[10:40, 10:590] = [255, 255, 255]           # a white stripe (slicing)
    edited[:, :, 2] = 0                               # remove ALL red from the image
    print("After edits: img[20, 20] =", edited[20, 20], " (white stripe, red removed)")

    # --- Boolean mask: change every pixel that matches a condition --------------
    recolored = img.copy()
    green_mask = (img[:, :, 1] > 200) & (img[:, :, 0] < 50) & (img[:, :, 2] < 50)
    recolored[green_mask] = [255, 0, 255]             # all pure-green pixels -> magenta
    print(f"Pixels recoloured with a mask: {green_mask.sum():,}")

    # --- Loop vs vectorised timing on a small patch -----------------------------
    import time
    patch = img[:100, :100]
    t0 = time.perf_counter(); slow = per_pixel_loop(patch); t1 = time.perf_counter()
    fast = 255 - patch;                              t2 = time.perf_counter()
    print(f"Invert 100x100 patch: loop {1000 * (t1 - t0):.1f} ms vs NumPy "
          f"{1000 * (t2 - t1):.3f} ms  (same result: {np.array_equal(slow, fast)})")

    grid = make_grid([img, edited, recolored], ["original", "edited (red removed)",
                                                "mask recolour"], cols=3)
    save_image(out, "pixel_editing.png", grid)
    show_images({"Pixel editing": grid}, args.show)
