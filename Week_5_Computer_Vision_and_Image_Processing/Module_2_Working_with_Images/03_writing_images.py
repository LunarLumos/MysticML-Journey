"""
Module 2 - Writing an Image to different paths (and formats)
============================================================

cv2.imwrite(path, img, params) saves an array to disk.
  * The FILE EXTENSION decides the format (.jpg, .png, .bmp, .webp ...)
  * It returns True/False - it does NOT create missing folders for you!
  * Optional params: JPEG quality (0-100), PNG compression (0-9)
"""

import sys
from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, output_dir  # noqa: E402


def write_and_report(path, img, params=None):
    """Write `img` to `path`, then print success flag and file size."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)   # imwrite fails if the folder is missing
    ok = cv2.imwrite(str(path), img, params or [])
    size_kb = path.stat().st_size / 1024 if ok else 0
    print(f"  {'OK  ' if ok else 'FAIL'} {path.relative_to(BASE_DIR)!s:<45} {size_kb:8.1f} KB")
    return ok


if __name__ == "__main__":
    base_parser("Write images to different paths/formats").parse_args()
    out = output_dir(__file__)
    img = cv2.imread(str(get_image_path("flower.jpg")))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("1) Same image, different formats:")
    for ext in ("png", "jpg", "bmp", "webp"):
        write_and_report(out / "formats" / f"flower.{ext}", img)

    print("\n2) JPEG quality trade-off (smaller file = more artefacts):")
    for q in (95, 50, 10):
        write_and_report(out / "jpeg_quality" / f"flower_q{q}.jpg", img,
                         [cv2.IMWRITE_JPEG_QUALITY, q])

    print("\n3) PNG compression level (lossless - only speed/size change):")
    for level in (0, 9):
        write_and_report(out / "png_compression" / f"flower_c{level}.png", img,
                         [cv2.IMWRITE_PNG_COMPRESSION, level])

    print("\n4) Different (nested) folders + a grayscale copy:")
    write_and_report(out / "grayscale" / "2024" / "flower_gray.png", gray)

    print("\n5) Writing into a folder that does NOT exist (without mkdir):")
    missing = out / "no_such_folder" / "x.png"
    try:
        ok = cv2.imwrite(str(missing), img)
    except cv2.error:            # newer OpenCV versions raise instead of returning False
        ok = False
    print(f"  cv2.imwrite(...) -> {ok}   <- always check the return value!")
