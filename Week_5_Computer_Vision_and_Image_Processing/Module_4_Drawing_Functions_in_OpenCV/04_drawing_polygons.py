"""
Module 4 - Drawing Polygons
===========================

    pts = np.array([[x1, y1], [x2, y2], ...], np.int32).reshape((-1, 1, 2))
    cv2.polylines(img, [pts], isClosed=True, color, thickness)  # outline
    cv2.fillPoly(img, [pts], color)                             # filled
    cv2.fillConvexPoly(img, pts, color)                         # faster, convex only

Points MUST be int32 and are passed inside a LIST (you can draw many at once).
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402


def regular_polygon(center, radius, sides, rotation_deg=-90):
    """Return the vertices of a regular polygon (triangle, hexagon, ...)."""
    angles = np.deg2rad(rotation_deg + np.arange(sides) * 360 / sides)
    xs = center[0] + radius * np.cos(angles)
    ys = center[1] + radius * np.sin(angles)
    return np.stack([xs, ys], axis=1).astype(np.int32).reshape((-1, 1, 2))


def star(center, outer, inner, points=5):
    """Return the vertices of a star (alternating outer/inner radius)."""
    angles = np.deg2rad(-90 + np.arange(points * 2) * 180 / points)
    radii = np.where(np.arange(points * 2) % 2 == 0, outer, inner)
    xs = center[0] + radii * np.cos(angles)
    ys = center[1] + radii * np.sin(angles)
    return np.stack([xs, ys], axis=1).astype(np.int32).reshape((-1, 1, 2))


if __name__ == "__main__":
    args = base_parser("Draw polygons").parse_args()
    img = np.zeros((360, 640, 3), dtype=np.uint8)

    triangle = regular_polygon((90, 110), 70, 3)
    hexagon = regular_polygon((250, 110), 70, 6)
    cv2.polylines(img, [triangle], True, (0, 255, 0), 3)             # closed outline
    cv2.fillPoly(img, [hexagon], (255, 128, 0))                      # filled
    cv2.fillPoly(img, [star((430, 110), 75, 30)], (0, 215, 255))
    zigzag = np.array([[20, 300], [80, 230], [140, 300], [200, 230], [260, 300]], np.int32)
    cv2.polylines(img, [zigzag.reshape((-1, 1, 2))], False, (0, 0, 255), 4)  # isClosed=False
    # Several polygons in ONE call
    squares = [regular_polygon((360 + i * 90, 280), 35, 4, 45) for i in range(3)]
    cv2.polylines(img, squares, True, (255, 0, 255), 2, cv2.LINE_AA)

    print("Triangle vertices:\n", triangle.reshape(-1, 2))
    save_image(output_dir(__file__), "polygons.png", img)
    show_images({"Polygons": img}, args.show)
