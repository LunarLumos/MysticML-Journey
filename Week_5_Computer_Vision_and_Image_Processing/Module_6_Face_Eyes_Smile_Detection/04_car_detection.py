"""
Module 6 - Car Detection with a Haar Cascade
============================================

The SAME detectMultiScale() code detects cars - you only need a cascade XML that
was trained on cars. OpenCV does NOT ship a car cascade (cv2.data.haarcascades
only has faces, eyes, smiles, bodies, cat faces and licence plates), so:

  * a popular community file is "cars.xml" (trained on rear views of cars,
    e.g. from github.com/andrewssobral/vehicle_detection_haarcascades)
  * the full car-detection project in ../../Projects/Car_Detection/ explains
    how to get a cascade and runs it on a traffic video

Usage:
    python 04_car_detection.py                                     # explains + looks for a cascade
    python 04_car_detection.py --cascade cars.xml --video traffic.mp4 [--show]
    python 04_car_detection.py --cascade cars.xml --image street.jpg

Without a cascade file the script explains what to do and exits normally.
"""

import sys
from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import base_parser, output_dir, save_image  # noqa: E402

PROJECT_DIR = BASE_DIR.parents[1] / "Projects" / "Car_Detection"


def find_cascade(user_path):
    """Return a usable car cascade path: user's choice, or one found in the project folder."""
    candidates = [user_path] if user_path else sorted(PROJECT_DIR.rglob("*car*.xml"))
    for c in candidates:
        if c and Path(c).exists():
            return Path(c)
    return None


def detect_cars(frame, cascade):
    """Detect cars in one BGR frame and draw red boxes. Returns number of cars."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.putText(frame, f"cars: {len(cars)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0, 255, 255), 2, cv2.LINE_AA)
    return len(cars)


def run_video(path, cascade, show, max_frames=200):
    """Run detection on a video file (the same loop as a webcam)."""
    cap = cv2.VideoCapture(str(path))
    frame, n, total = None, 0, 0
    while n < max_frames or show:
        ok, img = cap.read()
        if not ok:
            break
        total += detect_cars(img, cascade)
        frame, n = img, n + 1
        if show:
            cv2.imshow("Car detection (q to quit)", img)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
    cap.release()
    cv2.destroyAllWindows()
    print(f"Processed {n} frames, {total} car detections in total")
    return frame


if __name__ == "__main__":
    parser = base_parser("Car detection with a Haar cascade")
    parser.add_argument("--cascade", type=Path, help="path to a car cascade XML (e.g. cars.xml)")
    parser.add_argument("--video", type=Path, help="traffic video")
    parser.add_argument("--image", type=Path, help="street image")
    args = parser.parse_args()

    cascade_path = find_cascade(args.cascade)
    if cascade_path is None:
        print(__doc__)
        print("No car cascade found.\n"
              f"  -> See {PROJECT_DIR} (README) for the full project,\n"
              "  -> or download a cars.xml cascade and pass --cascade cars.xml --video your_video.mp4")
        sys.exit(0)

    cascade = cv2.CascadeClassifier(str(cascade_path))
    if cascade.empty():
        sys.exit(f"{cascade_path} is not a valid cascade XML file.")
    print(f"Using cascade: {cascade_path}")

    if args.image:
        img = cv2.imread(str(args.image))
        print(f"Cars found: {detect_cars(img, cascade)}")
        save_image(output_dir(__file__), "cars_detected.png", img)
    elif args.video:
        last = run_video(args.video, cascade, args.show)
        if last is not None:
            save_image(output_dir(__file__), "cars_last_frame.png", last)
    else:
        print("Cascade found - now pass --video or --image to run it.")
