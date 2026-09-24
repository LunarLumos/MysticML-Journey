"""
Module 2 - Displaying an Image
==============================

Two common ways to look at an image:

1. OpenCV window  -> cv2.imshow(title, img) + cv2.waitKey() + cv2.destroyAllWindows()
      * waitKey(0)   waits forever for a key press
      * waitKey(ms)  waits `ms` milliseconds (used for video)
      * the window only draws when waitKey is called!
2. Matplotlib     -> plt.imshow(img)  (remember BGR -> RGB), great in notebooks.

Run:
    python 02_displaying_images.py          # headless: saves outputs/*.png
    python 02_displaying_images.py --show   # opens real OpenCV windows
"""

import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, output_dir, save_image  # noqa: E402


def display_with_opencv(img, show):
    """Show an image in a resizable OpenCV window; report which key closed it."""
    if not show:
        print("(skipping cv2.imshow - pass --show to open a window)")
        return
    cv2.namedWindow("OpenCV window", cv2.WINDOW_NORMAL)   # WINDOW_NORMAL = resizable
    cv2.imshow("OpenCV window", img)
    print("Press any key in the window (or 'q') ...")
    key = cv2.waitKey(0) & 0xFF                              # & 0xFF -> plain ASCII code
    print(f"You pressed: {chr(key)!r} (code {key})")
    cv2.destroyAllWindows()


def display_with_matplotlib(img, save_path):
    """Plot the image with matplotlib (converted to RGB) and save the figure."""
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.set_title("Displayed with matplotlib (RGB)")
    ax.set_xlabel("x (column)")
    ax.set_ylabel("y (row)")                                # note: y grows DOWNWARDS
    fig.savefig(save_path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved -> {save_path}")


if __name__ == "__main__":
    args = base_parser("Display an image").parse_args()
    out = output_dir(__file__)
    img = cv2.imread(str(get_image_path("china.jpg")))

    display_with_opencv(img, args.show)
    display_with_matplotlib(img, out / "display_matplotlib.png")
    save_image(out, "display_opencv_equivalent.png", img)  # what the window would show
