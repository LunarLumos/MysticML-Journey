"""
Module 3 - Using the Webcam | Webcam Resolution
===============================================

cv2.VideoCapture(0) opens the default camera (0 = first, 1 = second ...).
A video is just a loop of images:  while True: ok, frame = cap.read()

Resolution is controlled with properties:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.get(cv2.CAP_PROP_FRAME_WIDTH)      # ALWAYS read back - the camera may
                                           # silently pick the closest supported size

Run:
    python 01_webcam_resolution.py --show                    # live window, 'q' to quit
    python 01_webcam_resolution.py --width 1280 --height 720 # request HD
    python 01_webcam_resolution.py --probe                   # test common resolutions
    (no --show: grabs ~60 frames, measures FPS, saves the last frame)
No camera? The script prints a message and exits normally.
"""

import sys
import time
from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import NO_CAMERA_MSG, base_parser, open_camera, output_dir, save_image  # noqa: E402

COMMON_RESOLUTIONS = [(320, 240), (640, 480), (1280, 720), (1920, 1080)]


def set_resolution(cap, width, height):
    """Ask the camera for width x height and return what it actually gave us."""
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def probe_resolutions(cap):
    """Try a list of common resolutions and report which ones the camera supports."""
    print("Requested      -> Actual")
    for w, h in COMMON_RESOLUTIONS:
        actual = set_resolution(cap, w, h)
        flag = "OK" if actual == (w, h) else "adjusted"
        print(f"  {w:>4} x {h:<4} -> {actual[0]:>4} x {actual[1]:<4} {flag}")


def run(cap, show, max_frames=60):
    """Read frames, draw the resolution + FPS on them; show live or save the last one."""
    frame, count, start = None, 0, time.time()
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Failed to read a frame - stopping.")
            break
        count += 1
        fps = count / max(time.time() - start, 1e-6)
        h, w = frame.shape[:2]
        cv2.putText(frame, f"{w}x{h}  {fps:.1f} FPS", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        if show:
            cv2.imshow("Webcam (press q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        elif count >= max_frames:
            break
    print(f"Read {count} frames at ~{count / max(time.time() - start, 1e-6):.1f} FPS")
    return frame


if __name__ == "__main__":
    parser = base_parser("Webcam basics and resolution")
    parser.add_argument("--camera", type=int, default=0, help="camera index (default 0)")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--probe", action="store_true", help="test common resolutions")
    args = parser.parse_args()

    cap = open_camera(args.camera)
    if cap is None:
        print(NO_CAMERA_MSG)
        sys.exit(0)

    try:
        if args.probe:
            probe_resolutions(cap)
        actual = set_resolution(cap, args.width, args.height)
        print(f"Requested {args.width}x{args.height}, camera gave {actual[0]}x{actual[1]}")
        last = run(cap, args.show)
        if last is not None:
            save_image(output_dir(__file__), "webcam_last_frame.jpg", last)
    finally:
        cap.release()               # ALWAYS release the camera so other apps can use it
        cv2.destroyAllWindows()
