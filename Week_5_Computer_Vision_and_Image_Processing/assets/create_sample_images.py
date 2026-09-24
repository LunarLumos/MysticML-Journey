"""
Week 5 - Shared sample images & video generator
================================================

Every script in Week 5 needs some pictures to work on. Instead of committing
big binary files to git, this helper CREATES them on demand (offline!):

    images/china.jpg        - real photo bundled with scikit-learn
    images/flower.jpg       - real photo bundled with scikit-learn
    images/shapes.png       - synthetic: coloured shapes drawn with OpenCV
    images/green_screen.png - synthetic: a "character" on a pure green background
    images/logo_rgba.png    - synthetic: 4-channel PNG with transparency (alpha)
    images/face.png         - a real face photo (scikit-image "astronaut") if
                              scikit-image is installed, otherwise a drawn face
    videos/sample_video.mp4 - synthetic 4-second animation (bouncing ball)

Usage
-----
    python create_sample_images.py          # create everything
    python create_sample_images.py --force  # re-create even if files exist

Other scripts import it like this:

    sys.path.append(str(BASE_DIR.parent / "assets"))
    from create_sample_images import get_image_path, get_video_path
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
VIDEOS_DIR = BASE_DIR / "videos"

RNG_SEED = 42  # everything synthetic is seeded -> identical every run


# ---------------------------------------------------------------------------
# Individual generators (each returns a BGR / BGRA numpy array)
# ---------------------------------------------------------------------------
def _sklearn_photo(filename):
    """Return one of scikit-learn's bundled photos ('china.jpg' / 'flower.jpg') as BGR."""
    from sklearn.datasets import load_sample_image

    rgb = load_sample_image(filename)          # scikit-learn gives RGB order
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)  # OpenCV works in BGR order


def make_shapes_image(height=400, width=600):
    """Draw a colourful synthetic image: gradient background + basic shapes."""
    # Horizontal blue->purple gradient background
    gradient = np.linspace(60, 200, width, dtype=np.uint8)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :, 0] = gradient              # Blue channel increases left -> right
    img[:, :, 2] = gradient[::-1] // 2   # a bit of red on the left

    cv2.rectangle(img, (40, 40), (220, 180), (0, 200, 255), -1)          # orange box
    cv2.circle(img, (400, 120), 80, (0, 255, 0), -1)                      # green circle
    cv2.ellipse(img, (150, 300), (100, 50), 30, 0, 360, (255, 255, 0), -1)  # cyan ellipse
    triangle = np.array([[420, 250], [540, 370], [300, 370]], np.int32)
    cv2.fillPoly(img, [triangle], (0, 0, 255))                            # red triangle
    cv2.putText(img, "OpenCV", (230, 230), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, (255, 255, 255), 3, cv2.LINE_AA)
    return img


def make_green_screen_image(height=400, width=600):
    """A simple 'character' (robot) standing in front of a pure green screen."""
    img = np.full((height, width, 3), (0, 255, 0), dtype=np.uint8)  # BGR pure green

    # Body, head, eyes, arms, legs of a friendly robot
    cv2.rectangle(img, (240, 170), (360, 320), (200, 120, 40), -1)   # body (blue-ish)
    cv2.rectangle(img, (255, 80), (345, 165), (180, 180, 180), -1)   # head (grey)
    cv2.circle(img, (280, 115), 12, (0, 0, 255), -1)                 # left eye (red)
    cv2.circle(img, (320, 115), 12, (0, 0, 255), -1)                 # right eye
    cv2.line(img, (275, 145), (325, 145), (40, 40, 40), 4)           # mouth
    cv2.line(img, (300, 80), (300, 50), (60, 60, 60), 4)             # antenna
    cv2.circle(img, (300, 45), 8, (0, 215, 255), -1)                 # antenna light
    cv2.rectangle(img, (200, 180), (235, 290), (150, 90, 30), -1)    # left arm
    cv2.rectangle(img, (365, 180), (400, 290), (150, 90, 30), -1)    # right arm
    cv2.rectangle(img, (255, 325), (290, 390), (90, 90, 90), -1)     # left leg
    cv2.rectangle(img, (310, 325), (345, 390), (90, 90, 90), -1)     # right leg
    cv2.putText(img, "Mystic-Bot", (230, 250), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2, cv2.LINE_AA)
    return img


def make_logo_rgba(size=200):
    """A round logo with a transparent background (4 channels: B, G, R, Alpha)."""
    img = np.zeros((size, size, 4), dtype=np.uint8)  # alpha=0 -> fully transparent
    c = size // 2
    cv2.circle(img, (c, c), c - 10, (255, 90, 30, 255), -1)          # opaque blue disc
    cv2.putText(img, "ML", (c - 45, c + 25), cv2.FONT_HERSHEY_DUPLEX,
                2.0, (255, 255, 255, 255), 4, cv2.LINE_AA)
    return img


def make_drawn_face(size=400, seed=RNG_SEED):
    """
    Fallback 'face' drawn with OpenCV primitives.
    NOTE: Haar cascades are trained on REAL faces, so they may not detect
    this cartoon. Install scikit-image (or pass --image your_photo.jpg) for
    a proper detection demo.
    """
    rng = np.random.default_rng(seed)
    img = np.full((size, size, 3), 235, dtype=np.uint8)
    img += rng.integers(0, 10, img.shape, dtype=np.uint8)            # light noise
    c = size // 2
    cv2.ellipse(img, (c, c), (120, 155), 0, 0, 360, (150, 180, 225), -1)   # skin
    cv2.ellipse(img, (c - 45, c - 35), (22, 12), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(img, (c + 45, c - 35), (22, 12), 0, 0, 360, (255, 255, 255), -1)
    cv2.circle(img, (c - 45, c - 35), 8, (40, 30, 20), -1)            # pupils
    cv2.circle(img, (c + 45, c - 35), 8, (40, 30, 20), -1)
    cv2.line(img, (c - 70, c - 65), (c - 20, c - 60), (40, 40, 60), 5)  # eyebrows
    cv2.line(img, (c + 20, c - 60), (c + 70, c - 65), (40, 40, 60), 5)
    cv2.line(img, (c, c - 20), (c - 10, c + 25), (110, 130, 180), 3)    # nose
    cv2.ellipse(img, (c, c + 60), (45, 20), 0, 10, 170, (60, 60, 170), 4)  # smile
    return img


def make_face_image():
    """Return (image, source_description) - a real face if scikit-image is available."""
    try:
        from skimage import data  # optional dependency, ships sample photos offline

        rgb = data.astronaut()  # NASA portrait of astronaut Eileen Collins (public domain)
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), "scikit-image data.astronaut() (public domain)"
    except Exception:  # ImportError or missing data file
        return make_drawn_face(), "synthetic drawn face (install scikit-image for a real photo)"


# ---------------------------------------------------------------------------
# Synthetic video
# ---------------------------------------------------------------------------
def make_sample_video(path, seconds=4, fps=25, width=640, height=360):
    """Write a short 'bouncing ball' animation with cv2.VideoWriter. Returns the real path."""
    path = Path(path)
    # 'mp4v' works on most OpenCV builds; fall back to MJPG/.avi if it does not.
    for fourcc_code, suffix in (("mp4v", ".mp4"), ("MJPG", ".avi")):
        out_path = path.with_suffix(suffix)
        writer = cv2.VideoWriter(str(out_path), cv2.VideoWriter_fourcc(*fourcc_code),
                                 fps, (width, height))
        if writer.isOpened():
            break
    else:
        raise RuntimeError("Could not open any cv2.VideoWriter codec on this system.")

    x, y, dx, dy, r = 80, 80, 9, 6, 30
    for i in range(seconds * fps):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (40 + i % 60, 30, 60)                        # slowly changing background
        x, y = x + dx, y + dy
        if not r <= x <= width - r:
            dx = -dx
        if not r <= y <= height - r:
            dy = -dy
        cv2.circle(frame, (x, y), r, (0, 200, 255), -1)
        cv2.putText(frame, f"Frame {i + 1:03d}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2, cv2.LINE_AA)
        writer.write(frame)                                     # frames must be BGR uint8
    writer.release()
    return out_path


# ---------------------------------------------------------------------------
# Public helpers used by all the module scripts
# ---------------------------------------------------------------------------
_GENERATORS = {
    "china.jpg": lambda: _sklearn_photo("china.jpg"),
    "flower.jpg": lambda: _sklearn_photo("flower.jpg"),
    "shapes.png": make_shapes_image,
    "green_screen.png": make_green_screen_image,
    "logo_rgba.png": make_logo_rgba,
    "face.png": lambda: make_face_image()[0],
}


def get_image_path(name, force=False):
    """Return the path to a sample image, creating it first if needed."""
    if name not in _GENERATORS:
        raise ValueError(f"Unknown sample image '{name}'. Choose from {list(_GENERATORS)}")
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    path = IMAGES_DIR / name
    if force or not path.exists():
        cv2.imwrite(str(path), _GENERATORS[name]())
    return path


def get_video_path(force=False):
    """Return the path to the sample video, creating it first if needed."""
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    for existing in (VIDEOS_DIR / "sample_video.mp4", VIDEOS_DIR / "sample_video.avi"):
        if existing.exists() and not force:
            return existing
    return make_sample_video(VIDEOS_DIR / "sample_video.mp4")


def create_all(force=False):
    """Create every sample image + the sample video and print a summary."""
    print("Creating Week 5 sample assets ...")
    for name in _GENERATORS:
        path = get_image_path(name, force=force)
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        print(f"  {name:<18} shape={str(img.shape):<15} -> {path}")
    print(f"  face.png source: {make_face_image()[1]}")
    video = get_video_path(force=force)
    print(f"  {'sample video':<18} -> {video}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Week 5 sample images and video.")
    parser.add_argument("--force", action="store_true", help="re-create files even if they exist")
    create_all(force=parser.parse_args().force)
