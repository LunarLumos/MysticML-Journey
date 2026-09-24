"""
Module 3 - Writing a video file with cv2.VideoWriter
====================================================

To PLAY a video we first need one - so we MAKE one (fully offline).
cv2.VideoWriter(path, fourcc, fps, (width, height)):
    fourcc  = 4-character codec code, e.g. 'mp4v' (.mp4), 'MJPG' / 'XVID' (.avi)
    fps     = frames per second
    size    = (width, height)  <- note: width first! Every frame must match it.

The actual drawing code lives in ../assets/create_sample_images.py
(make_sample_video) so other modules can reuse the same clip.
"""

import sys
from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_video_path  # noqa: E402
from cv_helpers import base_parser  # noqa: E402

if __name__ == "__main__":
    parser = base_parser("Create the sample video")
    parser.add_argument("--force", action="store_true", help="re-create even if it exists")
    args = parser.parse_args()

    path = get_video_path(force=args.force)
    cap = cv2.VideoCapture(str(path))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    print(f"Sample video ready: {path}")
    print(f"  {frames} frames @ {fps:.0f} FPS, {w}x{h}, {frames / fps:.1f} seconds, "
          f"{path.stat().st_size / 1024:.0f} KB")
