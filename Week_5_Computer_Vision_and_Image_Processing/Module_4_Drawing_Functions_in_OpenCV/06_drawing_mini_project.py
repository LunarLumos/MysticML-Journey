"""
Module 4 - Mini project: draw a scene using ALL the drawing functions
=====================================================================

A night-time landscape: gradient sky (creating an image), moon (circle),
mountains (polygons), house (rectangles + polygon roof), path (lines),
lake (ellipse) and a title (text).
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402


def draw_scene(h=400, w=640):
    """Return the finished scene as a BGR image."""
    # Sky: vertical gradient from dark blue (top) to purple (horizon)
    t = np.linspace(0, 1, h)[:, None]
    sky = np.zeros((h, w, 3), dtype=np.uint8)
    sky[..., 0] = (80 + 100 * t).astype(np.uint8)       # blue
    sky[..., 2] = (20 + 80 * t).astype(np.uint8)        # red
    img = sky

    rng = np.random.default_rng(7)                       # stars = tiny circles
    for x, y in zip(rng.integers(0, w, 60), rng.integers(0, h // 2, 60)):
        cv2.circle(img, (int(x), int(y)), 1, (255, 255, 255), -1)
    cv2.circle(img, (540, 70), 40, (200, 240, 255), -1)                  # moon

    mountains = np.array([[0, 300], [120, 170], [230, 280], [360, 140],
                          [500, 290], [640, 200], [640, 400], [0, 400]], np.int32)
    cv2.fillPoly(img, [mountains], (60, 80, 40))
    cv2.rectangle(img, (0, 320), (w, h), (40, 100, 40), -1)              # grass
    cv2.ellipse(img, (480, 360), (120, 25), 0, 0, 360, (140, 90, 20), -1)  # lake

    cv2.rectangle(img, (120, 250), (240, 340), (60, 120, 200), -1)       # house wall
    roof = np.array([[110, 250], [180, 195], [250, 250]], np.int32)
    cv2.fillPoly(img, [roof], (30, 30, 150))
    cv2.rectangle(img, (165, 290), (195, 340), (30, 60, 100), -1)        # door
    cv2.rectangle(img, (135, 265), (158, 285), (0, 230, 255), -1)        # lit window
    cv2.line(img, (180, 340), (260, 400), (120, 170, 200), 6)            # path
    cv2.putText(img, "Night in MysticML Valley", (150, 40),
                cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 1, cv2.LINE_AA)
    return img


if __name__ == "__main__":
    args = base_parser("Drawing mini project").parse_args()
    scene = draw_scene()
    save_image(output_dir(__file__), "scene.png", scene)
    show_images({"Scene": scene}, args.show)
