"""
Module 7 - Step 1: Capturing Samples
====================================

Builds the training set:  dataset/<person_name>/000.png, 001.png, ...
Each file is a 100x100 GRAYSCALE crop of just the face.

Four ways to get samples:

  1) Webcam (the classic way)
        python 01_capture_samples.py --name alice --count 50 --show
     Look at the camera, move your head a little, change expression.
     (Without --show it captures silently until --count faces are saved.)

  2) Import existing photos of ONE person from a folder
        python 01_capture_samples.py --name alice --from-folder ~/Pictures/alice
     Folder of sub-folders (one per person)? Leave out --name:
        python 01_capture_samples.py --from-folder ~/Pictures/people

  3) Synthetic people (offline, for testing the pipeline - NOT real faces)
        python 01_capture_samples.py --synthetic --people 4 --count 30

  4) Olivetti faces (40 real people, downloads ~4 MB once from the internet)
        python 01_capture_samples.py --olivetti --people 5

Privacy note: face images are personal data. dataset/ is git-ignored - keep it that way.
"""

import sys
from pathlib import Path

import cv2

from face_recognition_utils import (DATASET_DIR, IMAGE_EXTENSIONS, detect_faces,  # noqa: E402
                                    face_cascade, generate_synthetic_dataset, largest_face,
                                    preprocess)

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import NO_CAMERA_MSG, base_parser, open_camera  # noqa: E402


def next_index(folder):
    """Continue numbering after files that already exist (so re-runs add samples)."""
    existing = [int(p.stem) for p in folder.glob("*.png") if p.stem.isdigit()]
    return max(existing, default=-1) + 1


# ---------------------------------------------------------------------------
# 1) Webcam
# ---------------------------------------------------------------------------
def capture_from_webcam(name, count, camera, show):
    """Save `count` face crops of `name` from the webcam."""
    cap = open_camera(camera)
    if cap is None:
        print(NO_CAMERA_MSG)
        return 0
    cascade = face_cascade()
    folder = DATASET_DIR / name
    folder.mkdir(parents=True, exist_ok=True)
    idx, saved, frame_no = next_index(folder), 0, 0
    try:
        while saved < count:
            ok, frame = cap.read()
            if not ok:
                break
            frame_no += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(gray, cascade)
            if len(faces) and frame_no % 3 == 0:          # every 3rd frame -> more variety
                x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
                cv2.imwrite(str(folder / f"{idx:03d}.png"), preprocess(gray[y:y + h, x:x + w]))
                idx, saved = idx + 1, saved + 1
            if show:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{name}: {saved}/{count}  (q = stop)", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow("Capturing samples", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            elif frame_no > count * 20:                    # safety stop: no face in view
                print("Stopping - not enough faces detected in front of the camera.")
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return saved


# ---------------------------------------------------------------------------
# 2) Import from a folder
# ---------------------------------------------------------------------------
def import_person(src, name, cascade):
    """Detect + crop the face in every image of `src` and store it as person `name`."""
    folder = DATASET_DIR / name
    folder.mkdir(parents=True, exist_ok=True)
    idx, saved, skipped = next_index(folder), 0, 0
    for path in sorted(src.iterdir()):
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        gray = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        face = largest_face(gray, cascade) if gray is not None else None
        if face is None:
            # Already a tight face crop (e.g. a previous dataset)? keep the whole image.
            if gray is not None and gray.shape[0] <= 150 and gray.shape[1] <= 150:
                face = gray
            else:
                skipped += 1
                continue
        cv2.imwrite(str(folder / f"{idx:03d}.png"), preprocess(face))
        idx, saved = idx + 1, saved + 1
    print(f"  {name:<20} imported {saved} face(s), skipped {skipped} image(s) without a face")
    return saved


def import_from_folder(src, name):
    """Import one person (name given) or one person per sub-folder (name omitted)."""
    src = Path(src).expanduser()
    if not src.is_dir():
        raise SystemExit(f"Folder not found: {src}")
    cascade = face_cascade()
    if name:
        return import_person(src, name, cascade)
    return sum(import_person(sub, sub.name, cascade)
               for sub in sorted(src.iterdir()) if sub.is_dir())


# ---------------------------------------------------------------------------
# 4) Olivetti (optional, network on first use)
# ---------------------------------------------------------------------------
def import_olivetti(people):
    """Save the first `people` subjects of the Olivetti faces dataset (10 images each)."""
    try:
        from sklearn.datasets import fetch_olivetti_faces

        data = fetch_olivetti_faces()            # cached in ~/scikit_learn_data after 1st time
    except Exception as err:                     # no internet, SSL problems, ...
        print(f"Could not download Olivetti faces ({err.__class__.__name__}: {err}).\n"
              "Use --synthetic for an offline dataset instead.")
        return 0
    saved = 0
    for img, label in zip(data.images, data.target):
        if label >= people:
            continue
        folder = DATASET_DIR / f"olivetti_person_{label + 1:02d}"
        folder.mkdir(parents=True, exist_ok=True)
        face = (img * 255).astype("uint8")       # floats 0..1 -> uint8
        cv2.imwrite(str(folder / f"{next_index(folder):03d}.png"), preprocess(face))
        saved += 1
    return saved


if __name__ == "__main__":
    parser = base_parser("Capture face samples for the recognizer")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--from-folder", type=Path, help="import photos from this folder")
    source.add_argument("--synthetic", action="store_true", help="generate synthetic people")
    source.add_argument("--olivetti", action="store_true", help="use Olivetti faces (network)")
    parser.add_argument("--name", help="person name (folder name in dataset/)")
    parser.add_argument("--count", type=int, default=30, help="samples to capture per person")
    parser.add_argument("--people", type=int, default=4, help="people for --synthetic/--olivetti")
    parser.add_argument("--camera", type=int, default=0)
    args = parser.parse_args()

    if args.synthetic:
        names = generate_synthetic_dataset(people=args.people, samples=args.count)
        print(f"Generated {args.count} synthetic samples for each of: {', '.join(names)}")
    elif args.olivetti:
        print(f"Saved {import_olivetti(args.people)} Olivetti face images")
    elif args.from_folder:
        print(f"Imported {import_from_folder(args.from_folder, args.name)} face(s) in total")
    else:
        if not args.name:
            parser.error("--name is required for webcam capture (e.g. --name alice)")
        n = capture_from_webcam(args.name, args.count, args.camera, args.show)
        print(f"Saved {n} face sample(s) for '{args.name}'")
    print(f"Dataset folder: {DATASET_DIR}")
