"""
Module 7 - Shared helpers for the Face Recognition pipeline
===========================================================

    01_capture_samples.py  ->  dataset/<person_name>/*.png   (grayscale face crops)
    02_train_model.py      ->  models/  (trained recognizer + label names)
    03_test_model.py       ->  predictions on new images / live webcam

Two interchangeable recognizers are provided:

* "lbph"  - OpenCV's Local Binary Patterns Histograms recognizer.
            Needs the contrib build:  pip install opencv-contrib-python
* "eigen" - "Eigenfaces" with scikit-learn: PCA (finds the main directions of
            variation between faces = eigenfaces) + an SVM classifier.
            Works with the normal opencv-python package.

"auto" picks LBPH when cv2.face exists, otherwise Eigenfaces.
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from cv_helpers import load_cascade  # noqa: E402

DATASET_DIR = BASE_DIR / "dataset"
MODELS_DIR = BASE_DIR / "models"
FACE_SIZE = (100, 100)                 # every face crop is resized to 100 x 100 pixels
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".pgm", ".webp"}


# ---------------------------------------------------------------------------
# Face detection + pre-processing (shared by capture, training and testing)
# ---------------------------------------------------------------------------
def face_cascade():
    """Return the frontal-face Haar cascade."""
    return load_cascade("haarcascade_frontalface_default.xml")


def detect_faces(gray, cascade):
    """Return all face boxes (x, y, w, h) found in a grayscale image."""
    return cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))


def largest_face(gray, cascade):
    """Return the crop of the biggest face in the image, or None."""
    faces = detect_faces(gray, cascade)
    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    return gray[y:y + h, x:x + w]


def preprocess(face_gray):
    """Resize to FACE_SIZE and equalize the histogram (reduces lighting differences)."""
    face = cv2.resize(face_gray, FACE_SIZE, interpolation=cv2.INTER_AREA)
    return cv2.equalizeHist(face)


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------
def load_dataset(dataset_dir=DATASET_DIR):
    """
    Read dataset/<person>/*.png into arrays.

    Returns (faces: list[np.ndarray], labels: np.ndarray[int], names: list[str]).
    labels[i] is an index into names.
    """
    dataset_dir = Path(dataset_dir)
    people = sorted(p for p in dataset_dir.iterdir() if p.is_dir()) if dataset_dir.exists() else []
    faces, labels, names = [], [], []
    for person in people:
        files = sorted(f for f in person.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS)
        if not files:
            continue
        names.append(person.name)
        for f in files:
            img = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                faces.append(preprocess(img))
                labels.append(len(names) - 1)
    return faces, np.array(labels, dtype=np.int32), names


# ---------------------------------------------------------------------------
# Synthetic faces - an OFFLINE stand-in for real people, so everything is testable
# ---------------------------------------------------------------------------
def _person_params(rng):
    """Random but FIXED facial proportions that define one synthetic 'person'."""
    return dict(
        face_w=rng.integers(60, 80), face_h=rng.integers(78, 96),
        skin=int(rng.integers(120, 200)), bg=int(rng.integers(20, 90)),
        eye_dx=rng.integers(22, 36), eye_y=rng.integers(-28, -12), eye_r=rng.integers(5, 11),
        brow_tilt=rng.integers(-8, 9), nose_len=rng.integers(14, 32),
        mouth_w=rng.integers(18, 36), mouth_y=rng.integers(34, 52),
        hair=int(rng.integers(0, 3)), hair_tone=int(rng.integers(0, 80)),
    )


def draw_synthetic_face(p, rng):
    """Draw one sample of person `p` with random pose / lighting / expression noise."""
    s = 200
    img = np.full((s, s), p["bg"], dtype=np.uint8)
    c = (s // 2, s // 2 + 5)
    if p["hair"] == 1:                                   # long hair behind the head
        cv2.ellipse(img, (c[0], c[1] - 10), (p["face_w"] + 14, p["face_h"] + 10), 0, 0, 360,
                    p["hair_tone"], -1)
    cv2.ellipse(img, c, (int(p["face_w"]), int(p["face_h"])), 0, 0, 360, p["skin"], -1)
    if p["hair"] in (1, 2):                              # fringe / top hair
        cv2.ellipse(img, (c[0], c[1] - p["face_h"] + 20), (p["face_w"], 30), 0, 180, 360,
                    p["hair_tone"], -1)
    blink = rng.random() < 0.1                           # expression variation
    for side in (-1, 1):
        ex, ey = c[0] + side * p["eye_dx"], c[1] + p["eye_y"]
        if blink:
            cv2.line(img, (ex - p["eye_r"], ey), (ex + p["eye_r"], ey), 30, 2)
        else:
            cv2.circle(img, (ex, ey), int(p["eye_r"]), 245, -1)
            cv2.circle(img, (ex, ey), max(int(p["eye_r"]) // 2, 2), 20, -1)
        by = ey - p["eye_r"] - 8
        cv2.line(img, (ex - 12, by + side * p["brow_tilt"] // 2),
                 (ex + 12, by - side * p["brow_tilt"] // 2), 40, 3)
    cv2.line(img, (c[0], c[1] - 5), (c[0], c[1] - 5 + p["nose_len"]), p["skin"] - 50, 3)
    smile = int(rng.integers(0, 12))
    cv2.ellipse(img, (c[0], c[1] + p["mouth_y"]), (int(p["mouth_w"]), 4 + smile), 0, 0, 180, 60, 3)

    # --- random "photo conditions": pose, scale, lighting, noise ---------------
    angle, scale = rng.uniform(-8, 8), rng.uniform(0.92, 1.08)
    M = cv2.getRotationMatrix2D((s / 2, s / 2), angle, scale)
    M[:, 2] += rng.uniform(-6, 6, 2)
    img = cv2.warpAffine(img, M, (s, s), borderValue=int(p["bg"]))
    img = img.astype(np.float32) * rng.uniform(0.75, 1.2) + rng.uniform(-20, 20)
    img += rng.normal(0, 6, img.shape)
    return cv2.resize(np.clip(img, 0, 255).astype(np.uint8), FACE_SIZE)


SYNTHETIC_PREFIX = "synthetic_person_"


def synthetic_person(person_no, seed=7):
    """Facial proportions of synthetic person number `person_no` (1, 2, ...). Deterministic."""
    return _person_params(np.random.default_rng(seed * 1000 + person_no))


def generate_synthetic_dataset(dataset_dir=DATASET_DIR, people=4, samples=30, seed=7):
    """Create dataset/synthetic_person_X/*.png. Returns the list of person names."""
    names = []
    for no in range(1, people + 1):
        name = f"{SYNTHETIC_PREFIX}{no}"
        params = synthetic_person(no, seed)
        rng = np.random.default_rng(seed * 1000 + 500 + no)      # "photo session" randomness
        folder = Path(dataset_dir) / name
        folder.mkdir(parents=True, exist_ok=True)
        for j in range(samples):
            cv2.imwrite(str(folder / f"{j:03d}.png"), draw_synthetic_face(params, rng))
        names.append(name)
    return names


def new_synthetic_photos(name, n, session_seed=2024, seed=7):
    """Brand-new (never seen in training) samples of an existing synthetic person."""
    no = int(name.removeprefix(SYNTHETIC_PREFIX))
    rng = np.random.default_rng(session_seed * 1000 + no)
    return [draw_synthetic_face(synthetic_person(no, seed), rng) for _ in range(n)]


# ---------------------------------------------------------------------------
# Recognizer wrapper: same API for LBPH (OpenCV contrib) and Eigenfaces (sklearn)
# ---------------------------------------------------------------------------
def lbph_available():
    """True if the opencv-contrib 'face' module is installed."""
    return hasattr(cv2, "face") and hasattr(cv2.face, "LBPHFaceRecognizer_create")


def resolve_method(method):
    """Turn 'auto' into 'lbph' or 'eigen' and validate the choice."""
    if method == "auto":
        return "lbph" if lbph_available() else "eigen"
    if method == "lbph" and not lbph_available():
        raise SystemExit("LBPH needs opencv-contrib:  pip uninstall opencv-python && "
                         "pip install opencv-contrib-python   (or use --method eigen)")
    return method


class FaceRecognizer:
    """
    Unified recognizer.

    predict(face) returns (label, score, confident):
      * LBPH  : score = distance   (LOWER is better,  confident if distance < threshold)
      * eigen : score = probability (HIGHER is better, confident if prob > threshold)
    """

    DEFAULT_THRESHOLD = {"lbph": 80.0, "eigen": 0.5}

    def __init__(self, method="auto", names=None):
        self.method = resolve_method(method)
        self.names = names or []
        self.threshold = self.DEFAULT_THRESHOLD[self.method]
        self.model = None

    # ----- training ----------------------------------------------------------
    def fit(self, faces, labels):
        """Train on a list of FACE_SIZE grayscale crops and integer labels."""
        if self.method == "lbph":
            self.model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8,
                                                            grid_x=8, grid_y=8)
            self.model.train(list(faces), np.asarray(labels, dtype=np.int32))
        else:
            from sklearn.decomposition import PCA
            from sklearn.pipeline import make_pipeline
            from sklearn.svm import SVC

            X = self._flatten(faces)
            n_comp = int(min(50, len(X) - 1, X.shape[1]))
            self.model = make_pipeline(
                PCA(n_components=n_comp, whiten=True, random_state=0),   # the "eigenfaces"
                SVC(kernel="rbf", C=10, gamma="scale", probability=True,
                    class_weight="balanced", random_state=0),
            )
            self.model.fit(X, labels)
        return self

    @staticmethod
    def _flatten(faces):
        """(n, 100, 100) uint8 -> (n, 10000) floats in 0..1."""
        return np.array([f.reshape(-1) for f in faces], dtype=np.float32) / 255.0

    # ----- prediction --------------------------------------------------------
    def predict(self, face):
        """Predict one preprocessed face -> (label, score, confident)."""
        if self.method == "lbph":
            label, dist = self.model.predict(face)
            return int(label), float(dist), dist < self.threshold
        proba = self.model.predict_proba(self._flatten([face]))[0]
        idx = int(np.argmax(proba))
        label = int(self.model.classes_[idx])
        return label, float(proba[idx]), proba[idx] > self.threshold

    def name_of(self, label, confident=True):
        """Human readable name for a label ('Unknown' if not confident)."""
        return self.names[label] if confident and 0 <= label < len(self.names) else "Unknown"

    def describe_score(self, score):
        """Format the score the right way round for each method."""
        return f"dist={score:.1f}" if self.method == "lbph" else f"p={score:.2f}"

    # ----- persistence -------------------------------------------------------
    def save(self, models_dir=MODELS_DIR):
        """Save model + label names into models_dir."""
        models_dir = Path(models_dir)
        models_dir.mkdir(parents=True, exist_ok=True)
        if self.method == "lbph":
            model_file = models_dir / "lbph_model.yml"
            self.model.write(str(model_file))
        else:
            import joblib

            model_file = models_dir / "eigenfaces_model.joblib"
            joblib.dump(self.model, model_file)
        info = {"method": self.method, "names": self.names, "face_size": FACE_SIZE,
                "threshold": self.threshold, "model_file": model_file.name}
        (models_dir / "model_info.json").write_text(json.dumps(info, indent=2))
        return model_file

    @classmethod
    def load(cls, models_dir=MODELS_DIR):
        """Load a recognizer saved with save()."""
        info_file = Path(models_dir) / "model_info.json"
        if not info_file.exists():
            raise SystemExit("No trained model found - run 02_train_model.py first.")
        info = json.loads(info_file.read_text())
        rec = cls(info["method"], info["names"])
        rec.threshold = info["threshold"]
        model_file = Path(models_dir) / info["model_file"]
        if rec.method == "lbph":
            rec.model = cv2.face.LBPHFaceRecognizer_create()
            rec.model.read(str(model_file))
        else:
            import joblib

            rec.model = joblib.load(model_file)
        return rec
