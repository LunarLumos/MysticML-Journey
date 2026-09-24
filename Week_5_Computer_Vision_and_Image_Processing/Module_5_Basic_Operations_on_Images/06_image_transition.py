"""
Module 5 - Image Transition (cross-fade)
========================================

A cross-fade blends image A into image B over time:

    frame(alpha) = (1 - alpha) * A + alpha * B,   alpha: 0 -> 1

cv2.addWeighted(A, 1 - alpha, B, alpha, 0) computes exactly this (with
saturation to 0..255). Both images must have the SAME size and type.

Saves:
    outputs/transition.mp4 (or .avi)  - the video
    outputs/transition.gif            - animated GIF (needs Pillow)
    outputs/transition_frames.png     - a strip of key frames
Also shows a "wipe" transition (slide the boundary) for comparison.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent / "assets"))
from create_sample_images import get_image_path  # noqa: E402
from cv_helpers import base_parser, make_grid, output_dir, save_image, show_images  # noqa: E402



def crossfade_frames(a, b, steps=30):
    """Return a list of frames blending a -> b with cv2.addWeighted."""
    return [cv2.addWeighted(a, 1 - t, b, t, 0) for t in np.linspace(0, 1, steps)]


def wipe_frames(a, b, steps=30):
    """Left-to-right wipe: columns of b progressively replace columns of a."""
    frames = []
    for t in np.linspace(0, 1, steps):
        f = a.copy()
        x = int(t * a.shape[1])
        f[:, :x] = b[:, :x]
        frames.append(f)
    return frames


def write_video(frames, path, fps=15):
    """Write frames to a video file (mp4v, falling back to MJPG/avi)."""
    h, w = frames[0].shape[:2]
    for code, suffix in (("mp4v", ".mp4"), ("MJPG", ".avi")):
        target = Path(path).with_suffix(suffix)
        writer = cv2.VideoWriter(str(target), cv2.VideoWriter_fourcc(*code), fps, (w, h))
        if writer.isOpened():
            for f in frames:
                writer.write(f)
            writer.release()
            print(f"  saved -> {target}")
            return target
    print("  (no video codec available - skipped video)")
    return None


def write_gif(frames, path, fps=15):
    """Save an animated GIF with Pillow (optional dependency)."""
    try:
        from PIL import Image
    except ImportError:
        print("  (Pillow not installed - skipped GIF)")
        return None
    pil = [Image.fromarray(cv2.cvtColor(cv2.resize(f, (320, 214)), cv2.COLOR_BGR2RGB))
           for f in frames]
    pil[0].save(path, save_all=True, append_images=pil[1:], duration=int(1000 / fps), loop=0)
    print(f"  saved -> {path}")
    return path


if __name__ == "__main__":
    parser = base_parser("Image transition (cross-fade)")
    parser.add_argument("--steps", type=int, default=30, help="frames per transition")
    args = parser.parse_args()
    out = output_dir(__file__)

    a = cv2.imread(str(get_image_path("china.jpg")))
    b = cv2.imread(str(get_image_path("flower.jpg")))
    b = cv2.resize(b, (a.shape[1], a.shape[0]))       # sizes must match!

    fade = crossfade_frames(a, b, args.steps)
    wipe = wipe_frames(b, a, args.steps)
    all_frames = fade + [b] * 10 + wipe + [a] * 10     # hold each image for a moment
    print(f"Generated {len(all_frames)} frames")

    write_video(all_frames, out / "transition.mp4")
    write_gif(fade + fade[::-1], out / "transition.gif")
    keys = [fade[i] for i in np.linspace(0, len(fade) - 1, 5).astype(int)]
    save_image(out, "transition_frames.png",
               make_grid(keys, [f"alpha={t:.2f}" for t in np.linspace(0, 1, 5)], cols=5,
                         cell=(240, 160)))

    if args.show:
        for f in all_frames:
            cv2.imshow("Transition (q to stop)", f)
            if cv2.waitKey(40) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()
