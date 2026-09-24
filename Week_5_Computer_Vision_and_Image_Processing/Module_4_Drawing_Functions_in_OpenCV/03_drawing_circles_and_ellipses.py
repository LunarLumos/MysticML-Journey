"""
Module 4 - Drawing Circles and Ellipses
=======================================

    cv2.circle(img, center, radius, color, thickness)
    cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness)

  * axes = (half_width, half_height) of the ellipse
  * angle rotates the whole ellipse (degrees, clockwise)
  * startAngle/endAngle draw only an ARC (0, 360 = full ellipse)
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402


def draw_circles(img):
    """Outline, filled and concentric circles."""
    cv2.circle(img, (100, 100), 60, (0, 0, 255), 3)                     # red outline
    cv2.circle(img, (250, 100), 60, (0, 255, 0), -1)                    # filled green
    for r in range(10, 70, 12):                                          # target / bullseye
        cv2.circle(img, (400, 100), r, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.circle(img, (520, 100), 5, (0, 255, 255), -1)                   # a "dot" = tiny filled circle
    return img


def draw_ellipses(img):
    """Full, rotated, half and partial ellipses (arcs)."""
    cv2.ellipse(img, (100, 280), (80, 40), 0, 0, 360, (255, 0, 0), 3)          # full
    cv2.ellipse(img, (260, 280), (80, 40), 45, 0, 360, (255, 0, 255), -1)      # rotated, filled
    cv2.ellipse(img, (420, 280), (70, 50), 0, 0, 180, (0, 255, 255), 3)        # bottom half (smile!)
    cv2.ellipse(img, (540, 280), (50, 50), 0, 0, 270, (0, 165, 255), -1)       # "pac-man"
    return img


if __name__ == "__main__":
    args = base_parser("Draw circles and ellipses").parse_args()
    canvas = np.full((380, 620, 3), 30, dtype=np.uint8)
    draw_ellipses(draw_circles(canvas))
    save_image(output_dir(__file__), "circles_and_ellipses.png", canvas)
    show_images({"Circles & ellipses": canvas}, args.show)
