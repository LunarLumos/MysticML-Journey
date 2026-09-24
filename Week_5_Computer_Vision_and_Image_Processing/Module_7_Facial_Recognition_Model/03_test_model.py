"""
Module 7 - Step 3: Testing the Face Recognition Model
=====================================================

Loads the model saved by 02_train_model.py and recognises faces in NEW input:

    python 03_test_model.py                          # offline test on new, unseen samples
    python 03_test_model.py --image group_photo.jpg  # detect + recognise every face in a photo
    python 03_test_model.py --test-dir my_test_faces # folder of face crops/photos
    python 03_test_model.py --webcam --show          # live recognition, q to quit

Faces whose score is worse than the model's threshold are labelled "Unknown"
(tune with --threshold). Results are saved into outputs/.

Default offline test:
  * synthetic people -> brand-new synthetic photos (different random pose/lighting)
  * real people      -> dataset images with fresh random changes (brightness,
                        shift, noise). Only a rough check - use --test-dir with
                        photos that were NOT used for training for an honest score.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

from face_recognition_utils import (IMAGE_EXTENSIONS, SYNTHETIC_PREFIX, FaceRecognizer,
                                    detect_faces, face_cascade, load_dataset,
                                    new_synthetic_photos, preprocess)

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import (NO_CAMERA_MSG, base_parser, make_grid, open_camera,  # noqa: E402
                        output_dir, save_image, show_images)


def annotate_face(image, box, rec, face):
    """Predict one face crop and write the name + score above its box."""
    label, score, confident = rec.predict(face)
    name = rec.name_of(label, confident)
    x, y, w, h = box
    color = (0, 200, 0) if confident else (0, 0, 255)
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    cv2.putText(image, f"{name} ({rec.describe_score(score)})", (x, max(y - 8, 15)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
    return name


def augment(face, rng):
    """Random brightness/shift/noise so a dataset image looks like a new photo."""
    M = np.float32([[1, 0, rng.integers(-4, 5)], [0, 1, rng.integers(-4, 5)]])
    img = cv2.warpAffine(face, M, face.shape[::-1], borderMode=cv2.BORDER_REPLICATE)
    img = img.astype(np.float32) * rng.uniform(0.8, 1.2) + rng.normal(0, 5, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)


def offline_test(rec, per_person=10, seed=0):
    """Build a labelled test set, predict it and return (accuracy, tiles, titles)."""
    faces, labels, names = load_dataset()
    rng = np.random.default_rng(seed)
    samples = []                                     # (true_name, preprocessed face)
    for i, name in enumerate(rec.names):
        if name.startswith(SYNTHETIC_PREFIX):
            photos = new_synthetic_photos(name, per_person)
        else:
            idx = np.flatnonzero(labels == names.index(name)) if name in names else []
            if len(idx) == 0:
                continue
            photos = [augment(faces[j], rng) for j in rng.choice(idx, per_person)]
        samples += [(name, preprocess(p)) for p in photos]

    correct, accepted, tiles, titles = 0, 0, [], []
    for true_name, face in samples:
        label, score, confident = rec.predict(face)
        best_guess = rec.name_of(label)             # ignoring the threshold
        pred = rec.name_of(label, confident)        # "Unknown" if not confident
        correct += best_guess == true_name
        accepted += pred == true_name
        tile = cv2.cvtColor(face, cv2.COLOR_GRAY2BGR)
        # green = correct, orange = right person but "Unknown", red = wrong person
        color = (0, 200, 0) if pred == true_name else (0, 0, 255)
        if best_guess == true_name and not confident:
            color = (0, 165, 255)
        cv2.rectangle(tile, (0, 0), (99, 99), color, 3)
        tiles.append(tile)
        titles.append(f"{pred.replace(SYNTHETIC_PREFIX, 'P')} {rec.describe_score(score)}")
    n = max(len(samples), 1)
    acc = correct / n
    print(f"Offline test on {len(samples)} new photos:")
    print(f"  identity accuracy (best match)       : {correct}/{len(samples)} = {acc:.3f}")
    print(f"  correct AND confident (threshold)    : {accepted}/{len(samples)} = {accepted / n:.3f}"
          f"  (threshold = {rec.threshold})")
    return acc, tiles, titles


def recognise_image(rec, path, cascade):
    """Detect every face in a photo and label it. Returns the annotated image."""
    img = cv2.imread(str(path))
    if img is None:
        raise SystemExit(f"Could not read {path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    boxes = detect_faces(gray, cascade)
    if len(boxes) == 0 and max(gray.shape) <= 150:     # already a face crop
        boxes = [(0, 0, gray.shape[1], gray.shape[0])]
    for (x, y, w, h) in boxes:
        name = annotate_face(img, (x, y, w, h), rec, preprocess(gray[y:y + h, x:x + w]))
        print(f"  {path.name}: face at {(int(x), int(y), int(w), int(h))} -> {name}")
    if len(boxes) == 0:
        print(f"  {path.name}: no face found")
    return img


def live_recognition(rec, cascade, camera, show, frames=30):
    """Webcam loop: detect faces, recognise, draw."""
    cap = open_camera(camera)
    if cap is None:
        print(NO_CAMERA_MSG)
        return None
    frame, n = None, 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for (x, y, w, h) in detect_faces(gray, cascade):
                annotate_face(frame, (x, y, w, h), rec, preprocess(gray[y:y + h, x:x + w]))
            n += 1
            if show:
                cv2.imshow("Face recognition (q to quit)", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            elif n >= frames:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return frame


if __name__ == "__main__":
    parser = base_parser("Test the trained face recognizer")
    parser.add_argument("--image", type=Path, help="photo to recognise faces in")
    parser.add_argument("--test-dir", type=Path, help="folder of test images")
    parser.add_argument("--webcam", action="store_true")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--threshold", type=float,
                        help="LBPH: max distance (default 80) | eigen: min probability (0.5)")
    args = parser.parse_args()

    rec = FaceRecognizer.load()
    if args.threshold is not None:
        rec.threshold = args.threshold
    print(f"Loaded '{rec.method}' model for {len(rec.names)} people: {', '.join(rec.names)}")
    out = output_dir(__file__)

    if args.webcam:
        last = live_recognition(rec, face_cascade(), args.camera, args.show)
        if last is not None:
            save_image(out, "webcam_recognition.png", last)
    elif args.image or args.test_dir:
        cascade = face_cascade()
        paths = [args.image] if args.image else sorted(
            p for p in args.test_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
        results = {p.stem: recognise_image(rec, p, cascade) for p in paths}
        for name, img in results.items():
            save_image(out, f"recognised_{name}.png", img)
        show_images(results, args.show)
    else:
        acc, tiles, titles = offline_test(rec)
        grid = make_grid(tiles, titles, cols=8, cell=(150, 150))
        save_image(out, "offline_test_predictions.png", grid)
        show_images({"Predictions": grid}, args.show)
