"""
Project - Face / Smile / Eyes Detection from Image and Webcam
=============================================================

One command-line tool that works on:
  * single images           --image photo.jpg
  * a whole folder          --folder my_photos/
  * the live webcam         --webcam  (press s to save a snapshot, q to quit)
Without arguments it runs a built-in DEMO on the offline sample images
(a real portrait, its mirror image, a 2-person collage and a photo with no face).

Every processed image is saved to outputs/ and a CSV report is written to
outputs/detections_report.csv.

    python face_smile_eyes_detector.py                 # demo, headless
    python face_smile_eyes_detector.py --image me.jpg --show
    python face_smile_eyes_detector.py --webcam --show
"""

import csv
import sys
import time
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent))                      # Module 6 detection helpers
sys.path.append(str(BASE_DIR.parents[1] / "assets"))       # Week 5 shared assets
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import NO_CAMERA_MSG, base_parser, open_camera, output_dir, save_image, show_images  # noqa: E402
from face_detection_utils import detect, draw, load_cascades, summary  # noqa: E402

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


# ---------------------------------------------------------------------------
# Demo inputs (all offline)
# ---------------------------------------------------------------------------
def demo_images():
    """Return {name: image} built from the Week 5 sample assets."""
    face = cv2.imread(str(get_image_path("face.png")))
    china = cv2.imread(str(get_image_path("china.jpg")))
    small = cv2.resize(face, (256, 256))
    collage = np.hstack([small, cv2.flip(small, 1)])       # two "people" side by side
    return {
        "portrait": face,
        "portrait_mirrored": cv2.flip(face, 1),
        "two_people_collage": collage,
        "no_face_landscape": china,
    }


# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------
def process_image(name, image, cascades, out_dir, rows):
    """Detect, annotate, save and append a report row. Returns the annotated image."""
    start = time.perf_counter()
    results = detect(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cascades)
    ms = 1000 * (time.perf_counter() - start)
    annotated = draw(image.copy(), results)
    save_image(out_dir, f"{name}_detected.png", annotated)
    rows.append({
        "image": name,
        "width": image.shape[1], "height": image.shape[0],
        "faces": len(results),
        "eyes": sum(len(r["eyes"]) for r in results),
        "smiling_faces": sum(1 for r in results if r["smile"]),
        "time_ms": round(ms, 1),
    })
    print(f"  {name:<22} -> {summary(results)}  ({ms:.0f} ms)")
    return annotated


def run_webcam(cascades, out_dir, camera, show, frames):
    """Live detection loop. 's' saves a snapshot, 'q' quits."""
    cap = open_camera(camera)
    if cap is None:
        print(NO_CAMERA_MSG)
        return
    n = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            results = detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cascades)
            draw(frame, results)
            cv2.putText(frame, summary(results), (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 255), 2, cv2.LINE_AA)
            n += 1
            if show:
                cv2.imshow("Face/Smile/Eyes detector (s = save, q = quit)", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("s"):
                    save_image(out_dir, f"webcam_snapshot_{n}.png", frame)
                elif key == ord("q"):
                    break
            elif n >= frames:
                save_image(out_dir, "webcam_last_frame.png", frame)
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    print(f"Processed {n} webcam frames.")


def write_report(rows, path):
    """Write the detection results as CSV."""
    if not rows:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Report written -> {path}")


if __name__ == "__main__":
    parser = base_parser("Face / Smile / Eyes detection from image and webcam")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--image", type=Path, help="a single image")
    group.add_argument("--folder", type=Path, help="a folder of images")
    group.add_argument("--webcam", action="store_true", help="use the live webcam")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--frames", type=int, default=30, help="webcam frames without --show")
    args = parser.parse_args()

    cascades = load_cascades()
    out = output_dir(__file__)

    if args.webcam:
        run_webcam(cascades, out, args.camera, args.show, args.frames)
        sys.exit(0)

    if args.image:
        inputs = {args.image.stem: cv2.imread(str(args.image))}
    elif args.folder:
        inputs = {p.stem: cv2.imread(str(p)) for p in sorted(args.folder.iterdir())
                  if p.suffix.lower() in IMAGE_EXTENSIONS}
    else:
        print("No input given - running the offline DEMO on sample images:")
        inputs = demo_images()

    report, shown = [], {}
    for name, img in inputs.items():
        if img is None:
            print(f"  {name}: could not read - skipped")
            continue
        shown[name] = process_image(name, img, cascades, out, report)
    write_report(report, out / "detections_report.csv")
    show_images(shown, args.show)
