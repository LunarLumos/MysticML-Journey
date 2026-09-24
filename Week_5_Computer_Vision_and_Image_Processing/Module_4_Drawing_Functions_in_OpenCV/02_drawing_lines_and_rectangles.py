"""
Module 4 - Drawing Lines and Rectangles
=======================================

    cv2.line(img, pt1, pt2, color, thickness, lineType)
    cv2.arrowedLine(img, pt1, pt2, color, thickness, tipLength=0.1)
    cv2.rectangle(img, top_left, bottom_right, color, thickness)

  * points are (x, y) tuples of ints, origin (0, 0) = TOP-LEFT corner
  * colour is BGR: (255, 0, 0) = blue, (0, 255, 0) = green, (0, 0, 255) = red
  * thickness = -1 (or cv2.FILLED) fills the shape
  * lineType = cv2.LINE_AA gives smooth anti-aliased edges
  * drawing functions modify the image IN PLACE
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402


def draw_lines(img):
    """Draw several line styles on img."""
    cv2.line(img, (20, 30), (380, 30), (255, 255, 255), 1)                    # thin white
    cv2.line(img, (20, 60), (380, 60), (0, 255, 0), 5)                        # thick green
    cv2.line(img, (20, 100), (380, 140), (0, 0, 255), 3, cv2.LINE_AA)         # smooth red diagonal
    cv2.arrowedLine(img, (20, 180), (380, 180), (0, 255, 255), 3, tipLength=0.08)
    # Grid of thin lines - like graph paper
    for x in range(20, 400, 40):
        cv2.line(img, (x, 220), (x, 380), (90, 90, 90), 1)
    for y in range(220, 400, 40):
        cv2.line(img, (20, y), (380, y), (90, 90, 90), 1)
    return img


def draw_rectangles(img):
    """Draw outline, filled and 'bounding box' style rectangles on img."""
    cv2.rectangle(img, (420, 20), (580, 120), (255, 0, 0), 3)                 # blue outline
    cv2.rectangle(img, (420, 150), (580, 250), (0, 165, 255), -1)             # filled orange
    # A "detection box" with a label, the way detectors draw results
    x, y, w, h = 430, 290, 140, 90
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.rectangle(img, (x, y - 22), (x + 80, y), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, "face 97%", (x + 3, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
    return img


if __name__ == "__main__":
    args = base_parser("Draw lines and rectangles").parse_args()
    canvas = np.zeros((400, 600, 3), dtype=np.uint8)
    draw_rectangles(draw_lines(canvas))
    save_image(output_dir(__file__), "lines_and_rectangles.png", canvas)
    show_images({"Lines & rectangles": canvas}, args.show)
