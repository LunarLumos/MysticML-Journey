"""
Module 3 - Capture an Image using the Webcam
============================================

Live preview; press
    c / SPACE  -> save a snapshot into outputs/ (timestamped file name)
    q / ESC    -> quit

Headless (no --show): waits a moment for the camera to adjust its exposure,
then captures ONE photo automatically (--count N to take more).
No camera -> friendly message, exit code 0.
"""

import sys
import time
from datetime import datetime
from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import NO_CAMERA_MSG, base_parser, open_camera, output_dir, save_image  # noqa: E402


def snapshot_name():
    """File name like capture_20240131_142501_123.png (unique per capture)."""
    return f"capture_{datetime.now():%Y%m%d_%H%M%S_%f}"[:-3] + ".png"


def interactive_capture(cap, out):
    """Preview loop; save a frame whenever the user presses 'c' or SPACE."""
    saved = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        preview = frame.copy()                 # draw help text on a COPY, save the clean frame
        cv2.putText(preview, f"c/SPACE = capture | q = quit | saved: {saved}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("Capture", preview)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("c"), ord(" ")):
            save_image(out, snapshot_name(), frame)
            saved += 1
        elif key in (ord("q"), 27):
            break
    return saved


def auto_capture(cap, out, count, warmup_frames=15):
    """Headless mode: skip warm-up frames (auto-exposure), then save `count` photos."""
    for _ in range(warmup_frames):
        cap.read()
    saved = 0
    for _ in range(count):
        ok, frame = cap.read()
        if ok:
            save_image(out, snapshot_name(), frame)
            saved += 1
        time.sleep(0.2)
    return saved


if __name__ == "__main__":
    parser = base_parser("Capture images from the webcam")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--count", type=int, default=1, help="photos to take in headless mode")
    args = parser.parse_args()

    cap = open_camera(args.camera)
    if cap is None:
        print(NO_CAMERA_MSG)
        sys.exit(0)
    out = output_dir(__file__)
    try:
        n = interactive_capture(cap, out) if args.show else auto_capture(cap, out, args.count)
        print(f"Done - {n} image(s) saved in {out}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
