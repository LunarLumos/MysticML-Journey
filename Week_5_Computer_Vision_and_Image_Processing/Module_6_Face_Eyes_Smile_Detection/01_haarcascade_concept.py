"""
Module 6 - The Haar Cascade concept (Viola-Jones, 2001)
=======================================================

1. HAAR-LIKE FEATURES - tiny black/white rectangle patterns. A feature's value is
       sum(pixels under WHITE) - sum(pixels under BLACK)
   e.g. the eye region is darker than the cheeks below it -> "edge" feature.
2. INTEGRAL IMAGE - a table where each entry holds the sum of all pixels above-left.
   Any rectangle sum then needs only 4 look-ups -> features are super cheap.
3. ADABOOST - from ~160,000 possible features, training picks the few thousand
   that best separate faces from non-faces (weak classifiers -> strong classifier).
4. CASCADE - the classifiers are grouped into STAGES. A window must pass stage 1
   (very few features) to reach stage 2, and so on. Most non-face windows are
   rejected in the first stages, which is why detection is fast.
5. SLIDING WINDOW + IMAGE PYRAMID - detectMultiScale moves a window over the
   image at many scales (scaleFactor) and merges overlapping hits (minNeighbors).

This script:
  * draws the basic Haar feature types      -> outputs/haar_feature_types.png
  * builds an integral image and checks a rectangle sum
  * computes a real "eyes darker than cheeks" feature on a face
  * reads the XML of the face cascade and counts its stages/features
  * lists all cascades that ship with OpenCV
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402


def draw_feature_types(cell=120):
    """Return an image showing the 5 classic Haar-like feature shapes."""
    W, B = 255, 0
    patterns = {
        "edge (vertical)": [[W, B]],
        "edge (horizontal)": [[W], [B]],
        "line (vertical)": [[W, B, W]],
        "line (horizontal)": [[W], [B], [W]],
        "four-rectangle": [[W, B], [B, W]],
    }
    tiles = []
    for name, pat in patterns.items():
        pat = np.array(pat, dtype=np.uint8)
        tile = cv2.resize(pat, (cell, cell), interpolation=cv2.INTER_NEAREST)
        tile = cv2.copyMakeBorder(tile, 30, 5, 5, 5, cv2.BORDER_CONSTANT, value=128)
        cv2.putText(tile, name, (4, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.38, 255, 1, cv2.LINE_AA)
        tiles.append(tile)
    return np.hstack(tiles)


def rect_sum(integral, x, y, w, h):
    """Sum of pixels in rectangle (x, y, w, h) using only 4 integral-image look-ups."""
    return (integral[y + h, x + w] - integral[y, x + w]
            - integral[y + h, x] + integral[y, x])


def cascade_structure(xml_path):
    """Return (window_size, n_stages, n_weak_classifiers, n_features) of a cascade XML."""
    root = ET.parse(xml_path).getroot().find("cascade")
    size = (int(root.find("width").text), int(root.find("height").text))
    stages = root.find("stages")
    n_weak = sum(len(s.find("weakClassifiers")) for s in stages)
    n_features = len(root.find("features"))
    return size, len(stages), n_weak, n_features


if __name__ == "__main__":
    args = base_parser("Haar cascade concept").parse_args()
    out = output_dir(__file__)

    # 1) Feature shapes
    features = draw_feature_types()
    save_image(out, "haar_feature_types.png", features)

    # 2) Integral image: sum of a rectangle in O(1)
    gray = cv2.cvtColor(cv2.imread(str(get_image_path("face.png"))), cv2.COLOR_BGR2GRAY)
    integral = cv2.integral(gray)          # shape (h+1, w+1), an extra row/column of zeros
    x, y, w, h = 50, 60, 40, 30
    fast, slow = rect_sum(integral, x, y, w, h), int(gray[y:y + h, x:x + w].sum())
    print(f"Integral image shape {integral.shape} for image {gray.shape}")
    print(f"Rectangle sum via integral image = {fast}, via NumPy = {slow}, equal: {fast == slow}")

    # 3) A real 2-rectangle feature on the detected face: eyes band vs cheeks band
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.1, 5) if not face_cascade.empty() else []
    if len(faces):
        fx, fy, fw, fh = faces[0]
        band_h = fh // 6
        eyes_y, cheeks_y = fy + int(fh * 0.25), fy + int(fh * 0.25) + band_h
        eyes = rect_sum(integral, fx, eyes_y, fw, band_h) / (fw * band_h)
        cheeks = rect_sum(integral, fx, cheeks_y, fw, band_h) / (fw * band_h)
        print(f"Face found at {tuple(int(v) for v in faces[0])}: mean brightness "
              f"eyes band = {eyes:.1f}, cheeks band = {cheeks:.1f} "
              f"-> feature value (cheeks - eyes) = {cheeks - eyes:.1f}")
        vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(vis, (fx, eyes_y), (fx + fw, eyes_y + band_h), (0, 0, 0), 2)
        cv2.rectangle(vis, (fx, cheeks_y), (fx + fw, cheeks_y + band_h), (255, 255, 255), 2)
        save_image(out, "haar_feature_on_face.png", vis)
    else:
        print("No face found in face.png (install scikit-image for a real photo).")

    # 4) What is inside a cascade file?
    xml = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    size, n_stages, n_weak, n_feat = cascade_structure(xml)
    print(f"\n{xml.name}: window {size[0]}x{size[1]} px, {n_stages} stages, "
          f"{n_weak} weak classifiers, {n_feat} Haar features")

    # 5) All cascades shipped with OpenCV
    print("\nCascades bundled with OpenCV (cv2.data.haarcascades):")
    for p in sorted(Path(cv2.data.haarcascades).glob("*.xml")):
        print("  -", p.name)
    show_images({"Haar feature types": features}, args.show)
