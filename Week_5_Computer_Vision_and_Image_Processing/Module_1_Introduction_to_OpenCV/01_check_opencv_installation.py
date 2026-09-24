"""
Module 1 - Installing OpenCV-Python: verify your installation
=============================================================

Run this right after `pip install opencv-python` to check that:
  * cv2 imports and which version you have
  * NumPy works together with it (OpenCV images ARE NumPy arrays)
  * the Haar cascade XML files (used in Module 6) are available
  * whether the optional "contrib" modules (cv2.face, used in Module 7) exist
  * whether a GUI backend is present (cv2.imshow needs one - the
    "headless" package has none, which is fine for servers)
"""

import sys
from pathlib import Path

import numpy as np


# ------------------------------------------------------------------
# 1. Import check
# ------------------------------------------------------------------
def check_import():
    """Import cv2 and print its version, or explain how to install it."""
    try:
        import cv2
    except ImportError:
        print("OpenCV is NOT installed. Install it with:\n"
              "    pip install opencv-python            # normal desktop package\n"
              "    pip install opencv-contrib-python    # + extra modules (cv2.face)\n"
              "    pip install opencv-python-headless   # servers / no GUI")
        sys.exit(1)
    print(f"Python version  : {sys.version.split()[0]}")
    print(f"OpenCV version  : {cv2.__version__}")
    print(f"NumPy version   : {np.__version__}")
    return cv2


# ------------------------------------------------------------------
# 2. Feature checks
# ------------------------------------------------------------------
def check_features(cv2):
    """Report on cascades, contrib modules, GUI support and video I/O."""
    cascade_dir = Path(cv2.data.haarcascades)
    cascades = sorted(p.name for p in cascade_dir.glob("*.xml"))
    print(f"\nHaar cascades folder : {cascade_dir}")
    print(f"Number of cascades   : {len(cascades)}")
    for name in cascades:
        print(f"   - {name}")

    # OpenCV 5.x removed the classic Haar CascadeClassifier from the main package.
    has_cascade = hasattr(cv2, "CascadeClassifier") and len(cascades) > 0
    print(f"\ncv2.CascadeClassifier available : {has_cascade}")
    if not has_cascade:
        print("   !! Modules 6-7 need Haar cascades -> pip install \"opencv-python>=4.9,<5\"")

    has_face = hasattr(cv2, "face")
    print(f"cv2.face (contrib) available    : {has_face}"
          + ("" if has_face else "  -> Module 7 will use the scikit-learn fallback"))

    # Build information tells us which GUI / video backends were compiled in
    build = cv2.getBuildInformation()
    gui_lines = [ln.strip() for ln in build.splitlines() if "GUI" in ln][:2]
    print("GUI backend info                :", " | ".join(gui_lines) or "unknown")

    # Quick smoke test: create an image, blur it, and encode it to PNG in memory
    img = np.random.default_rng(0).integers(0, 256, (100, 100, 3), dtype=np.uint8)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    ok, png = cv2.imencode(".png", blurred)
    print(f"Smoke test (blur + PNG encode): {'OK' if ok else 'FAILED'} "
          f"({len(png)} bytes)")


if __name__ == "__main__":
    print("=" * 60)
    print("OpenCV installation check")
    print("=" * 60)
    check_features(check_import())
