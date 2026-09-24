"""
Week 5 - Tiny helpers shared by the module scripts
===================================================

Why? Every script follows the same rule:
    * results are ALWAYS saved into an ``outputs/`` folder next to the script
    * windows (cv2.imshow) are opened ONLY when you pass ``--show``
This keeps the scripts runnable on servers / CI where there is no screen.
"""

import argparse
from pathlib import Path

import cv2
import numpy as np


def base_parser(description):
    """Return an ArgumentParser that already knows the common ``--show`` flag."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--show", action="store_true",
                        help="open OpenCV windows (press any key to close them)")
    return parser


def output_dir(script_file):
    """Create (if needed) and return the outputs/ folder next to ``script_file``."""
    out = Path(script_file).resolve().parent / "outputs"
    out.mkdir(exist_ok=True)
    return out


def save_image(out_dir, filename, image):
    """Save an image into ``out_dir`` and print where it went. Returns the path."""
    path = Path(out_dir) / filename
    cv2.imwrite(str(path), image)
    print(f"  saved -> {path}")
    return path


def show_images(windows, show):
    """
    Display ``{window_title: image}`` with cv2.imshow when ``show`` is True.

    cv2.waitKey(0) waits for ANY key; destroyAllWindows() closes everything.
    """
    if not show:
        return
    for title, image in windows.items():
        cv2.imshow(title, image)
    print("Press any key in an image window to continue ...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def to_bgr(image):
    """Make any image (gray / BGR / BGRA) 3-channel BGR so it can be stacked."""
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return image


def label(image, text):
    """Return a copy of ``image`` with a caption bar written on top."""
    img = to_bgr(image).copy()
    cv2.rectangle(img, (0, 0), (img.shape[1], 28), (0, 0, 0), -1)
    cv2.putText(img, text, (6, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 1, cv2.LINE_AA)
    return img


def make_grid(images, titles=None, cols=3, cell=(300, 220)):
    """
    Put several images into one 'contact sheet' so a single PNG shows a comparison.

    ``cell`` = (width, height) each image is resized to.
    """
    titles = titles or [""] * len(images)
    tiles = [label(cv2.resize(to_bgr(im), cell), t) for im, t in zip(images, titles)]
    while len(tiles) % cols:                        # pad the last row with black tiles
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
    return np.vstack(rows)


def open_camera(index=0):
    """
    Try to open a webcam. Returns an opened cv2.VideoCapture or None.

    A camera "opens" on some systems even though it cannot deliver frames,
    so we also try to read one frame before declaring success.
    """
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        cap.release()
        return None
    ok, _ = cap.read()
    if not ok:
        cap.release()
        return None
    return cap


NO_CAMERA_MSG = (
    "No webcam found (or permission denied). Nothing to do - exiting gracefully.\n"
    "Tip: plug in a camera / allow camera access for your terminal, "
    "or try another index with --camera 1."
)


def load_cascade(filename):
    """
    Load one of the Haar cascade XML files that ship with OpenCV (cv2.data.haarcascades).

    Exits with a helpful message if the cascade is unavailable (e.g. OpenCV 5.x,
    which dropped CascadeClassifier from the main package).
    """
    if not hasattr(cv2, "CascadeClassifier"):
        raise SystemExit("This OpenCV build has no CascadeClassifier (OpenCV 5.x?).\n"
                         "Install the 4.x series:  pip install \"opencv-python>=4.9,<5\"")
    path = Path(cv2.data.haarcascades) / filename
    cascade = cv2.CascadeClassifier(str(path))
    if cascade.empty():
        raise SystemExit(f"Could not load cascade file: {path}")
    return cascade
