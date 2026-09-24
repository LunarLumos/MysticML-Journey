"""
Module 1 - Introduction to Image Processing & Computer Vision
=============================================================

Image PROCESSING : image in  -> (better / changed) image out
                   e.g. resize, blur, sharpen, edge detection
Computer VISION  : image in  -> understanding / information out
                   e.g. "there are 3 faces", "this is a flower"

This script runs a tiny pipeline on a real photo to show both ideas:
    load -> grayscale -> blur -> threshold -> edges -> find contours (count objects)

Run:
    python 02_intro_image_processing.py          # saves outputs/pipeline.png
    python 02_intro_image_processing.py --show   # also opens a window
"""

import sys
from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402


def processing_pipeline(image):
    """Run classic image-processing steps and return (steps_dict, n_objects)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)            # 3 channels -> 1 channel
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)                # remove noise
    _, thresh = cv2.threshold(blurred, 0, 255,                  # Otsu picks the threshold
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edges = cv2.Canny(blurred, 50, 150)                        # outlines

    # --- the "computer vision" step: turn pixels into information -------------
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big = [c for c in contours if cv2.contourArea(c) > 500]    # ignore tiny specks
    annotated = image.copy()
    cv2.drawContours(annotated, big, -1, (0, 0, 255), 2)

    steps = {"1. original": image, "2. grayscale": gray, "3. blurred": blurred,
             "4. threshold (Otsu)": thresh, "5. Canny edges": edges,
             f"6. {len(big)} objects found": annotated}
    return steps, len(big)


if __name__ == "__main__":
    args = base_parser(__doc__.splitlines()[1]).parse_args()
    out = output_dir(__file__)

    img = cv2.imread(str(get_image_path("shapes.png")))
    print(f"Loaded image with shape {img.shape} (height, width, channels)")

    steps, n = processing_pipeline(img)
    print(f"Image processing produced {len(steps) - 1} new images;")
    print(f"computer vision step counted {n} large objects in the picture.")

    grid = make_grid(list(steps.values()), list(steps.keys()), cols=3)
    save_image(out, "pipeline.png", grid)
    show_images({"Image processing pipeline": grid}, args.show)
