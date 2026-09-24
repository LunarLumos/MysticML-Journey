"""
Module 2 - Images as matrices & numbers | Shape, Dimension and Size
==================================================================

A digital image is just a grid of numbers:
  * grayscale : 2-D array  (height, width)          one 0-255 value per pixel
  * colour    : 3-D array  (height, width, 3)       B, G, R values per pixel
  * with alpha: 3-D array  (height, width, 4)

Useful attributes (they are plain NumPy):
  img.shape  -> (rows, cols[, channels])
  img.ndim   -> number of dimensions (2 = gray, 3 = colour)
  img.size   -> total number of values = rows * cols * channels
  img.dtype  -> uint8 = integers 0..255
  img.nbytes -> memory used in bytes
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402


def describe(name, img):
    """Print shape, dimensions, size, dtype and memory of an image."""
    h, w = img.shape[:2]
    channels = 1 if img.ndim == 2 else img.shape[2]
    print(f"{name}")
    print(f"  shape  : {img.shape}  -> height={h}, width={w}, channels={channels}")
    print(f"  ndim   : {img.ndim}")
    print(f"  size   : {img.size:,} values  (= {h} x {w} x {channels})")
    print(f"  dtype  : {img.dtype}  (min={img.min()}, max={img.max()})")
    print(f"  memory : {img.nbytes / 1024:.1f} KB in RAM")


if __name__ == "__main__":
    args = base_parser("Images as matrices").parse_args()
    out = output_dir(__file__)
    np.set_printoptions(linewidth=120)

    color = cv2.imread(str(get_image_path("china.jpg")))
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    describe("Colour image (china.jpg)", color)
    describe("Grayscale version", gray)

    file_kb = get_image_path("china.jpg").stat().st_size / 1024
    print(f"\nFile size on disk: {file_kb:.1f} KB (JPEG compressed) vs "
          f"{color.nbytes / 1024:.1f} KB decoded in memory")

    print("\nTop-left 5x5 block of the GRAYSCALE matrix (numbers = brightness):")
    print(gray[:5, :5])
    print("\nPixel (row=0, col=0) in colour is [B, G, R] =", color[0, 0])

    # --- Numbers -> image: build a tiny 8x8 image by hand ----------------------
    tiny = np.array([[0, 255] * 4, [255, 0] * 4] * 4, dtype=np.uint8)  # checkerboard
    print("\nAn 8x8 checkerboard written as a matrix:\n", tiny)
    big = cv2.resize(tiny, (240, 240), interpolation=cv2.INTER_NEAREST)  # enlarge to see it
    save_image(out, "checkerboard_from_numbers.png", big)

    # Each colour channel is itself a grayscale matrix
    b, g, r = cv2.split(color)
    channels = np.hstack([b, g, r])
    save_image(out, "bgr_channels_side_by_side.png", channels)
    show_images({"Checkerboard": big, "B | G | R channels": channels}, args.show)
