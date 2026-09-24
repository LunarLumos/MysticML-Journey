"""
Module 3 - Convolution, Pooling and Flatten BY HAND (NumPy)
===========================================================
Before using Keras' Conv2D, let's see what it actually computes.

  * Convolution : slide a small kernel (e.g. 3x3) over the image; at every
                  position multiply element-wise and sum -> one output pixel.
                  Different kernels detect different features (edges, blur...).
  * ReLU        : keep positive responses, zero out the rest.
  * Max pooling : take the max of every 2x2 block -> image half as big,
                  keeps the strongest signal, adds a bit of shift-invariance.
  * Flatten     : unroll the final 2-D feature maps into a 1-D vector for
                  the Dense layers.

Image: sklearn's bundled sample photo "china.jpg" (no download needed).

Run:
    python 01_convolution_pooling_numpy.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_sample_image

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------
def conv2d(image, kernel, stride=1, padding=0):
    """Naive 2-D convolution (really cross-correlation, like deep-learning libs).

    output size = (H + 2*padding - kH) // stride + 1
    """
    if padding:
        image = np.pad(image, padding, mode="constant")
    kh, kw = kernel.shape
    out_h = (image.shape[0] - kh) // stride + 1
    out_w = (image.shape[1] - kw) // stride + 1
    out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            patch = image[i * stride:i * stride + kh, j * stride:j * stride + kw]
            out[i, j] = np.sum(patch * kernel)          # multiply & sum
    return out


def relu(x):
    return np.maximum(0, x)


def max_pool(feature_map, size=2, stride=2):
    """Keep the max value of each size x size window."""
    out_h = (feature_map.shape[0] - size) // stride + 1
    out_w = (feature_map.shape[1] - size) // stride + 1
    out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            out[i, j] = feature_map[i * stride:i * stride + size,
                                    j * stride:j * stride + size].max()
    return out


KERNELS = {
    "Vertical edges (Sobel-x)": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float),
    "Horizontal edges (Sobel-y)": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], float),
    "Blur (box 3x3)": np.ones((3, 3)) / 9,
    "Sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], float),
}


def tiny_example():
    """Tiny 5x5 example you can verify with pen and paper."""
    img = np.array([
        [0, 0, 0, 9, 9],
        [0, 0, 0, 9, 9],
        [0, 0, 0, 9, 9],
        [0, 0, 0, 9, 9],
        [0, 0, 0, 9, 9],
    ], dtype=float)
    k = KERNELS["Vertical edges (Sobel-x)"]
    fmap = conv2d(img, k)
    print("5x5 input (dark left, bright right):\n", img.astype(int))
    print("\n3x3 vertical-edge kernel:\n", k.astype(int))
    print("\nFeature map (3x3) - big values where the edge is:\n", fmap.astype(int))
    print("\nAfter 2x2 max pool (stride 1 here, to keep it visible):\n",
          max_pool(fmap, size=2, stride=1).astype(int))
    print("\nFlatten ->", max_pool(fmap, 2, 1).ravel().astype(int), "\n")


def image_demo():
    """Apply every kernel to a real photo, then ReLU + max pool, and plot."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    rgb = load_sample_image("china.jpg")                      # (427, 640, 3)
    gray = rgb.mean(axis=2)[::4, ::4] / 255.0                 # downsample for speed
    print(f"Grayscale image shape: {gray.shape}")

    fig, axes = plt.subplots(3, len(KERNELS) + 1, figsize=(18, 10))
    axes[0, 0].imshow(gray, cmap="gray")
    axes[0, 0].set_title(f"Input {gray.shape}")
    for r in (1, 2):
        axes[r, 0].axis("off")

    for col, (name, kernel) in enumerate(KERNELS.items(), start=1):
        fmap = conv2d(gray, kernel, padding=1)                # 'same' size output
        activated = relu(fmap)
        pooled = max_pool(activated)
        print(f"{name:<28} conv {fmap.shape} -> pool {pooled.shape} "
              f"-> flatten {pooled.size} values")
        axes[0, col].imshow(fmap, cmap="gray")
        axes[0, col].set_title(f"Conv: {name}", fontsize=9)
        axes[1, col].imshow(activated, cmap="gray")
        axes[1, col].set_title(f"ReLU {activated.shape}", fontsize=9)
        axes[2, col].imshow(pooled, cmap="gray")
        axes[2, col].set_title(f"MaxPool 2x2 {pooled.shape}", fontsize=9)
    for ax in axes.ravel():
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    out = OUTPUT_DIR / "convolution_pooling.png"
    plt.savefig(out, dpi=110)
    plt.close()
    print(f"\nSaved plot -> {out}")


if __name__ == "__main__":
    tiny_example()
    image_demo()
