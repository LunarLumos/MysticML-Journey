"""
Module 2 - Reading an Image with different modes
================================================

cv2.imread(path, flag) loads an image file into a NumPy array.
The `flag` (read mode) decides HOW it is decoded:

    cv2.IMREAD_COLOR      (1)  -> 3 channels BGR, alpha dropped   (default)
    cv2.IMREAD_GRAYSCALE  (0)  -> 1 channel, brightness only
    cv2.IMREAD_UNCHANGED (-1)  -> as stored, keeps alpha channel (4 channels)
    cv2.IMREAD_REDUCED_COLOR_2 -> colour, width & height halved while decoding

IMPORTANT: cv2.imread does NOT raise an error for a wrong path - it returns None!
"""

import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, output_dir, show_images  # noqa: E402

READ_MODES = {
    "IMREAD_COLOR": cv2.IMREAD_COLOR,
    "IMREAD_GRAYSCALE": cv2.IMREAD_GRAYSCALE,
    "IMREAD_UNCHANGED": cv2.IMREAD_UNCHANGED,
    "IMREAD_REDUCED_COLOR_2": cv2.IMREAD_REDUCED_COLOR_2,
}


def read_in_all_modes(path):
    """Read the same file with every mode and print what we get."""
    images = {}
    print(f"\nFile: {Path(path).name}")
    for name, flag in READ_MODES.items():
        img = cv2.imread(str(path), flag)
        images[name] = img
        channels = 1 if img.ndim == 2 else img.shape[2]
        print(f"  {name:<24} shape={str(img.shape):<16} channels={channels} dtype={img.dtype}")
    return images


def safe_imread(path, flag=cv2.IMREAD_COLOR):
    """imread that raises a helpful error instead of silently returning None."""
    img = cv2.imread(str(path), flag)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img


if __name__ == "__main__":
    args = base_parser("Read an image in different modes").parse_args()
    out = output_dir(__file__)

    photo_modes = read_in_all_modes(get_image_path("flower.jpg"))
    logo_modes = read_in_all_modes(get_image_path("logo_rgba.png"))  # has an alpha channel

    # --- The classic beginner trap: OpenCV = BGR, Matplotlib = RGB -------------
    bgr = photo_modes["IMREAD_COLOR"]
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(bgr);  axes[0].set_title("BGR shown as RGB (wrong colours!)")
    axes[1].imshow(rgb);  axes[1].set_title("IMREAD_COLOR -> converted to RGB")
    axes[2].imshow(photo_modes["IMREAD_GRAYSCALE"], cmap="gray")
    axes[2].set_title("IMREAD_GRAYSCALE")
    axes[3].imshow(cv2.cvtColor(logo_modes["IMREAD_UNCHANGED"], cv2.COLOR_BGRA2RGBA))
    axes[3].set_title("IMREAD_UNCHANGED (alpha kept)")
    for ax in axes:
        ax.axis("off")
    fig.tight_layout()
    save_path = out / "read_modes.png"
    fig.savefig(save_path, dpi=100)
    plt.close(fig)
    print(f"\nComparison figure saved -> {save_path}")

    # --- What happens with a wrong path? ---------------------------------------
    print("\ncv2.imread('does_not_exist.jpg') returns:", cv2.imread("does_not_exist.jpg"))
    try:
        safe_imread("does_not_exist.jpg")
    except FileNotFoundError as err:
        print("safe_imread raised ->", err)

    show_images({"Colour": bgr, "Grayscale": photo_modes["IMREAD_GRAYSCALE"]}, args.show)
