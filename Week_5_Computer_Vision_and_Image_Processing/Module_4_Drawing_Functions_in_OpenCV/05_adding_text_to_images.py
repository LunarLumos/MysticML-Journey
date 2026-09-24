"""
Module 4 - Adding Text to Images
================================

    cv2.putText(img, text, org, fontFace, fontScale, color, thickness, lineType)

  * org = BOTTOM-LEFT corner of the text (x, y)
  * cv2.getTextSize(...) tells you how big the text will be -> use it to centre
    text or draw a background box behind it
  * Hershey fonts only support basic ASCII characters (no emoji/accents)
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402


FONTS = {
    "HERSHEY_SIMPLEX": cv2.FONT_HERSHEY_SIMPLEX,
    "HERSHEY_PLAIN": cv2.FONT_HERSHEY_PLAIN,
    "HERSHEY_DUPLEX": cv2.FONT_HERSHEY_DUPLEX,
    "HERSHEY_COMPLEX": cv2.FONT_HERSHEY_COMPLEX,
    "HERSHEY_TRIPLEX": cv2.FONT_HERSHEY_TRIPLEX,
    "HERSHEY_SCRIPT_SIMPLEX": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
}


def put_centered_text(img, text, y, scale=1.0, color=(255, 255, 255), thickness=2,
                      font=cv2.FONT_HERSHEY_SIMPLEX):
    """Write text horizontally centred at height y using cv2.getTextSize."""
    (tw, th), baseline = cv2.getTextSize(text, font, scale, thickness)
    x = (img.shape[1] - tw) // 2
    cv2.putText(img, text, (x, y), font, scale, color, thickness, cv2.LINE_AA)
    return (x, y - th, tw, th + baseline)


def put_label_with_background(img, text, org, bg=(0, 0, 0), fg=(0, 255, 255)):
    """Draw text on a filled rectangle so it is readable on any background."""
    (tw, th), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
    x, y = org
    cv2.rectangle(img, (x - 4, y - th - 6), (x + tw + 4, y + baseline), bg, -1)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, fg, 1, cv2.LINE_AA)


if __name__ == "__main__":
    args = base_parser("Add text to images").parse_args()
    out = output_dir(__file__)

    # 1) Font gallery
    gallery = np.full((60 + 45 * len(FONTS), 640, 3), 40, dtype=np.uint8)
    put_centered_text(gallery, "OpenCV font gallery", 40, 1.0, (0, 255, 255))
    for i, (name, font) in enumerate(FONTS.items()):
        cv2.putText(gallery, f"{name}: MysticML 123", (15, 90 + i * 45), font, 0.9,
                    (255, 255, 255), 1, cv2.LINE_AA)
    save_image(out, "font_gallery.png", gallery)

    # 2) Text on a real photo - caption bar + labelled point of interest
    sys.path.append(str(BASE_DIR.parent / "assets"))
    from create_sample_images import get_image_path  # noqa: E402

    photo = cv2.imread(str(get_image_path("flower.jpg")))
    put_centered_text(photo, "Flower", 60, 2.0, (255, 255, 255), 4, cv2.FONT_HERSHEY_DUPLEX)
    put_label_with_background(photo, "petal", (420, 250))
    cv2.circle(photo, (410, 255), 5, (0, 255, 255), -1)
    save_image(out, "text_on_photo.png", photo)
    show_images({"Fonts": gallery, "Text on photo": photo}, args.show)
