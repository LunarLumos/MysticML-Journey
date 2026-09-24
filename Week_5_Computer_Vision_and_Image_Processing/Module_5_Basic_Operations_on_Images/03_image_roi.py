"""
Module 5 - Image ROI (Region Of Interest)
=========================================

An ROI is a rectangular slice of the image:  roi = img[y1:y2, x1:x2]
  * slicing returns a VIEW -> changing roi changes the original image!
    use roi.copy() if you want an independent piece
  * you can paste an ROI somewhere else if the shapes match
  * cv2.selectROI lets you draw the box with the mouse (only with --show)
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402


if __name__ == "__main__":
    args = base_parser("Image ROI").parse_args()
    out = output_dir(__file__)
    img = cv2.imread(str(get_image_path("shapes.png")))

    # 1) Cut out the green circle (centre (400, 120), radius 80)
    x1, y1, x2, y2 = 320, 40, 480, 200
    if args.show:  # let the user choose the region with the mouse instead
        x, y, w, h = cv2.selectROI("Select a region, then ENTER", img)
        cv2.destroyAllWindows()
        if w and h:
            x1, y1, x2, y2 = x, y, x + w, y + h
    roi = img[y1:y2, x1:x2].copy()
    print(f"ROI from (x={x1}, y={y1}) to (x={x2}, y={y2}) -> shape {roi.shape}")

    # 2) Paste (copy) the ROI to another location of the same size
    pasted = img.copy()
    h, w = roi.shape[:2]
    pasted[220:220 + h, 20:20 + w] = roi
    cv2.rectangle(pasted, (x1, y1), (x2, y2), (255, 255, 255), 2)

    # 3) Views vs copies: editing a view edits the original
    demo = img.copy()
    view = demo[0:100, 0:100]      # NO copy
    view[:] = 0                    # blacken the view ...
    print("Top-left pixel of the ORIGINAL after editing the view:", demo[0, 0],
          "-> the original changed too!")

    # 4) Process only the ROI (blur a region - like hiding a face / licence plate)
    anon = img.copy()
    anon[40:200, 320:480] = cv2.GaussianBlur(anon[40:200, 320:480], (51, 51), 0)

    grid = make_grid([img, roi, pasted, demo, anon],
                     ["original", "ROI", "ROI pasted", "view edited", "blur only ROI"], cols=3)
    save_image(out, "roi.png", grid)
    show_images({"ROI demo": grid}, args.show)
