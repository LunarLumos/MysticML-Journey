"""
Module 6 - Detect Eyes / Face / Smile from any Image
====================================================

    python 02_detect_from_image.py                        # sample face (assets/images/face.png)
    python 02_detect_from_image.py --image my_photo.jpg   # your own photo
    python 02_detect_from_image.py --targets face eyes    # skip smile
    python 02_detect_from_image.py --show                 # open a window too

Colours: face = blue, eyes = green, smile = red. Result -> outputs/detected_<name>.png
"""

import sys
from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, output_dir, save_image, show_images  # noqa: E402
from face_detection_utils import detect, draw, load_cascades, summary  # noqa: E402

if __name__ == "__main__":
    parser = base_parser("Detect faces, eyes and smiles in an image")
    parser.add_argument("--image", type=Path, default=None, help="image path (default: sample face)")
    parser.add_argument("--targets", nargs="+", default=["face", "eyes", "smile"],
                        choices=["face", "eyes", "smile"])
    args = parser.parse_args()

    path = args.image or get_image_path("face.png")
    img = cv2.imread(str(path))
    if img is None:
        sys.exit(f"Could not read image: {path}")

    cascades = load_cascades(set(args.targets) | {"face"})   # face is always needed first
    results = detect(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cascades)

    print(f"Image: {path.name} {img.shape}")
    print("Result:", summary(results))
    for i, r in enumerate(results, 1):
        print(f"  face {i}: box={r['face']} eyes={len(r['eyes'])} smile={'yes' if r['smile'] else 'no'}")
    if not results:
        print("  Tip: Haar cascades need a fairly frontal, well-lit face. "
              "Try another photo or lower minNeighbors in face_detection_utils.py.")

    annotated = draw(img.copy(), results)
    save_image(output_dir(__file__), f"detected_{path.stem}.png", annotated)
    show_images({"Detections": annotated}, args.show)
