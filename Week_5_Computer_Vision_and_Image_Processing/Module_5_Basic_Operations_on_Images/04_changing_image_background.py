"""
Module 5 - Changing an Image Background
=======================================

Idea: build a MASK (white = foreground, black = background), then combine:
    result = foreground * mask + new_background * (1 - mask)

Method A - Colour key ("green screen"):
    convert to HSV (hue is great for picking a colour), then cv2.inRange()
Method B - Threshold on a plain/bright background (grayscale + threshold)
Bonus  - cv2.bitwise_and / bitwise_or with masks does the same combination.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402



def green_screen_mask(img, lower=(40, 80, 80), upper=(80, 255, 255)):
    """Return a mask that is 255 on the SUBJECT and 0 on green pixels."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(hsv, np.array(lower), np.array(upper))   # 255 where green
    mask = cv2.bitwise_not(green)                                # invert -> subject
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # clean noise
    return mask


def replace_background(fg, mask, new_bg):
    """Put the masked foreground on top of a new background (same size)."""
    new_bg = cv2.resize(new_bg, (fg.shape[1], fg.shape[0]))
    fg_part = cv2.bitwise_and(fg, fg, mask=mask)
    bg_part = cv2.bitwise_and(new_bg, new_bg, mask=cv2.bitwise_not(mask))
    return cv2.add(fg_part, bg_part)


if __name__ == "__main__":
    args = base_parser("Change image background").parse_args()
    out = output_dir(__file__)

    # --- A) Green screen ---------------------------------------------------------
    robot = cv2.imread(str(get_image_path("green_screen.png")))
    china = cv2.imread(str(get_image_path("china.jpg")))
    mask = green_screen_mask(robot)
    composite = replace_background(robot, mask, china)
    print(f"Green screen: {100 * (mask > 0).mean():.1f}% of pixels kept as foreground")

    # Solid colour background + soft (feathered) edges using float blending
    soft = cv2.GaussianBlur(mask, (7, 7), 0).astype(np.float32)[..., None] / 255
    purple = np.full_like(robot, (130, 0, 130))
    soft_result = (robot * soft + purple * (1 - soft)).astype(np.uint8)

    # --- B) Threshold method: logo on a black background -> new background ---------
    logo = cv2.imread(str(get_image_path("logo_rgba.png")), cv2.IMREAD_UNCHANGED)
    logo_bgr, alpha = logo[..., :3], logo[..., 3]      # PNG alpha is already a mask!
    flower = cv2.resize(cv2.imread(str(get_image_path("flower.jpg"))), (200, 200))
    logo_on_flower = replace_background(logo_bgr, alpha, flower)
    gray = cv2.cvtColor(logo_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh_mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)  # mask by brightness
    print(f"Alpha mask vs threshold mask agree on "
          f"{100 * (thresh_mask == alpha).mean():.1f}% of pixels")

    grid = make_grid([robot, mask, composite, soft_result, logo_on_flower, thresh_mask],
                     ["green screen input", "mask (HSV inRange)", "new background",
                      "solid colour + soft edge", "logo via alpha", "threshold mask"], cols=3)
    save_image(out, "background_change.png", grid)
    show_images({"Background change": grid}, args.show)
