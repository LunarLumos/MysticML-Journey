"""
Module 5 - Edge Detection
=========================

An EDGE is where brightness changes quickly -> large image gradient.

| Method     | How                                                        |
|------------|------------------------------------------------------------|
| Sobel      | 1st derivative in x (Gx) and y (Gy); magnitude = sqrt(Gx^2 + Gy^2) |
| Laplacian  | 2nd derivative, finds edges in all directions at once      |
| Canny      | blur -> Sobel -> thin edges (non-max suppression) -> 2 thresholds (hysteresis) |

Use a float depth (cv2.CV_64F) for Sobel/Laplacian, otherwise negative
gradients get cut to 0; convert back with cv2.convertScaleAbs().

With --show a trackbar window lets you tune the two Canny thresholds live.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402



def sobel_edges(gray):
    """Return (|Gx|, |Gy|, magnitude) as uint8 images."""
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = cv2.magnitude(gx, gy)
    return cv2.convertScaleAbs(gx), cv2.convertScaleAbs(gy), cv2.convertScaleAbs(mag)


def canny_tuner(gray):
    """Interactive Canny thresholds with trackbars (needs a GUI)."""
    win = "Canny (ESC to close)"
    cv2.namedWindow(win)
    cv2.createTrackbar("low", win, 50, 500, lambda v: None)
    cv2.createTrackbar("high", win, 150, 500, lambda v: None)
    while True:
        lo, hi = cv2.getTrackbarPos("low", win), cv2.getTrackbarPos("high", win)
        cv2.imshow(win, cv2.Canny(gray, lo, hi))
        if cv2.waitKey(30) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = base_parser("Edge detection").parse_args()
    out = output_dir(__file__)
    img = cv2.imread(str(get_image_path("china.jpg")))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)          # less noise -> cleaner edges

    gx, gy, mag = sobel_edges(blurred)
    lap = cv2.convertScaleAbs(cv2.Laplacian(blurred, cv2.CV_64F, ksize=3))
    canny = cv2.Canny(blurred, 50, 150)
    canny_tight = cv2.Canny(blurred, 150, 300)
    print(f"Canny(50,150) edge pixels : {np.count_nonzero(canny):,}")
    print(f"Canny(150,300) edge pixels: {np.count_nonzero(canny_tight):,}  (higher thresholds = fewer edges)")

    grid = make_grid([img, gx, gy, mag, lap, canny],
                     ["original", "Sobel X", "Sobel Y", "Sobel magnitude", "Laplacian",
                      "Canny 50/150"], cols=3)
    save_image(out, "edges.png", grid)
    if args.show:
        show_images({"Edge detection": grid}, True)
        canny_tuner(blurred)
