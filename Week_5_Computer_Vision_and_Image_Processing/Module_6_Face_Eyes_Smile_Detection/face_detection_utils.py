"""
Module 6 - Shared face / eyes / smile detection helpers
=======================================================

Used by 02_detect_from_image.py, 03_detect_from_webcam.py and the project in
Project_Face_Smile_Eyes_Detection/. Keeping the logic in ONE place means the
image and webcam versions always behave the same way.

Strategy (the classic, fast approach):
  1. detect FACES in the whole grayscale image
  2. search for EYES only in the UPPER half of each face box
  3. search for a SMILE only in the LOWER half of each face box
Restricting the search area makes detection faster AND removes most false positives.
"""

import sys
from pathlib import Path

import cv2

sys.path.append(str(Path(__file__).resolve().parent.parent / "assets"))
from cv_helpers import load_cascade  # noqa: E402

CASCADE_FILES = {
    "face": "haarcascade_frontalface_default.xml",
    "eyes": "haarcascade_eye.xml",
    "smile": "haarcascade_smile.xml",
}

# detectMultiScale parameters per target:
#   scaleFactor  - how much the image is shrunk at each pyramid step (1.05 slow/accurate .. 1.3 fast)
#   minNeighbors - how many overlapping hits are needed to accept a detection (higher = stricter)
#   minSize      - ignore objects smaller than this (pixels)
PARAMS = {
    "face": dict(scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)),
    "eyes": dict(scaleFactor=1.1, minNeighbors=8, minSize=(12, 12)),
    "smile": dict(scaleFactor=1.1, minNeighbors=15, minSize=(20, 10)),  # strict: mouths are "easy" to find
}

COLORS = {"face": (255, 0, 0), "eyes": (0, 255, 0), "smile": (0, 0, 255)}  # BGR


def load_cascades(targets=("face", "eyes", "smile")):
    """Return {target: cv2.CascadeClassifier} for the requested targets."""
    return {t: load_cascade(CASCADE_FILES[t]) for t in targets}


def detect(gray, cascades):
    """
    Detect faces, then eyes/smiles inside each face.

    Returns a list of dicts: {"face": (x, y, w, h), "eyes": [...], "smile": [...]}
    where eye/smile boxes are already in FULL-image coordinates.
    """
    gray = cv2.equalizeHist(gray)                    # improves contrast -> more robust
    results = []
    faces = cascades["face"].detectMultiScale(gray, **PARAMS["face"])
    for (x, y, w, h) in faces:
        item = {"face": (int(x), int(y), int(w), int(h)), "eyes": [], "smile": []}
        if "eyes" in cascades:
            upper = gray[y:y + h // 2, x:x + w]          # eyes are in the upper half
            for (ex, ey, ew, eh) in cascades["eyes"].detectMultiScale(upper, **PARAMS["eyes"]):
                item["eyes"].append((int(x + ex), int(y + ey), int(ew), int(eh)))
        if "smile" in cascades:
            lower = gray[y + h // 2:y + h, x:x + w]      # mouth is in the lower half
            for (sx, sy, sw, sh) in cascades["smile"].detectMultiScale(lower, **PARAMS["smile"]):
                item["smile"].append((int(x + sx), int(y + h // 2 + sy), int(sw), int(sh)))
        results.append(item)
    return results


def draw(image, results):
    """Draw the boxes of `detect()` onto image (in place) and return it."""
    for item in results:
        for target in ("face", "eyes", "smile"):
            boxes = [item[target]] if target == "face" else item[target]
            for (x, y, w, h) in boxes:
                cv2.rectangle(image, (x, y), (x + w, y + h), COLORS[target], 2)
        x, y = item["face"][:2]
        text = "smiling :)" if item["smile"] else "face"
        cv2.putText(image, text, (x, max(y - 8, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    COLORS["smile"] if item["smile"] else COLORS["face"], 2, cv2.LINE_AA)
    return image


def summary(results):
    """Return a one-line human readable summary of the detections."""
    n_eyes = sum(len(r["eyes"]) for r in results)
    n_smiles = sum(1 for r in results if r["smile"])
    return f"{len(results)} face(s), {n_eyes} eye(s), {n_smiles} smiling face(s)"
