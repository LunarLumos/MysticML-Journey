"""
Module 4 - Creating an Image (a blank canvas)
=============================================

Because an image is just a NumPy array, "creating an image" = creating an array:

    np.zeros((h, w, 3), np.uint8)            -> black colour canvas
    np.ones((h, w, 3), np.uint8) * 255       -> white canvas
    np.full((h, w, 3), (255, 0, 0), np.uint8)-> filled with a BGR colour (blue!)
    np.zeros((h, w), np.uint8)               -> black GRAYSCALE canvas

Remember: shape is (HEIGHT, WIDTH, channels) but OpenCV points are (x, y)!
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402


def create_canvases(h=200, w=300):
    """Return a dict of differently created blank images."""
    horizontal = np.tile(np.linspace(0, 255, w, dtype=np.uint8), (h, 1))  # 0..255 left->right
    return {
        "black (zeros)": np.zeros((h, w, 3), dtype=np.uint8),
        "white (ones*255)": np.ones((h, w, 3), dtype=np.uint8) * 255,
        "blue (full, BGR)": np.full((h, w, 3), (255, 0, 0), dtype=np.uint8),
        "gray gradient": cv2.cvtColor(horizontal, cv2.COLOR_GRAY2BGR),
        "random noise": np.random.default_rng(0).integers(0, 256, (h, w, 3), dtype=np.uint8),
        "half & half": np.hstack([np.full((h, w // 2, 3), (0, 0, 255), np.uint8),
                                  np.full((h, w - w // 2, 3), (0, 255, 255), np.uint8)]),
    }


if __name__ == "__main__":
    args = base_parser("Create blank images").parse_args()
    out = output_dir(__file__)
    canvases = create_canvases()
    for name, img in canvases.items():
        print(f"{name:<18} shape={img.shape} dtype={img.dtype} first pixel={img[0, 0]}")
        save_image(out, "canvas_" + name.split()[0] + ".png", img)
    show_images(canvases, args.show)
