"""
Module 6 - Detect Eyes / Face / Smile from the Live Webcam
==========================================================

Exactly the same detection as on a single image - just inside a video loop.

    python 03_detect_from_webcam.py --show       # live window, press q to quit
    python 03_detect_from_webcam.py              # headless: process 30 frames, save the last
Tip: detection is faster on a smaller frame -> --scale 0.5 halves width/height.
No camera? The script prints a message and exits normally.
"""

import sys
import time
from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import NO_CAMERA_MSG, base_parser, open_camera, output_dir, save_image  # noqa: E402
from face_detection_utils import detect, draw, load_cascades, summary  # noqa: E402

if __name__ == "__main__":
    parser = base_parser("Live face/eyes/smile detection")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--scale", type=float, default=1.0, help="resize factor for speed")
    parser.add_argument("--frames", type=int, default=30, help="frames to process without --show")
    args = parser.parse_args()

    cascades = load_cascades()
    cap = open_camera(args.camera)
    if cap is None:
        print(NO_CAMERA_MSG)
        sys.exit(0)

    count, start, frame, results = 0, time.time(), None, []
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)                         # mirror view feels natural
            if args.scale != 1.0:
                frame = cv2.resize(frame, None, fx=args.scale, fy=args.scale)
            results = detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cascades)
            draw(frame, results)
            count += 1
            fps = count / (time.time() - start)
            cv2.putText(frame, f"{summary(results)} | {fps:.1f} FPS", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2, cv2.LINE_AA)
            if args.show:
                cv2.imshow("Face / Eyes / Smile (q to quit)", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            elif count >= args.frames:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    print(f"Processed {count} frames. Last frame: {summary(results)}")
    if frame is not None:
        save_image(output_dir(__file__), "webcam_detection_last_frame.jpg", frame)
