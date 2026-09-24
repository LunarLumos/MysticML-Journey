"""
Module 1 · Script 02 – Creating Different Arrays using NumPy
============================================================

Covers: np.array, zeros, ones, full, empty, eye/identity, arange, linspace,
logspace, *_like helpers, diag, tile/repeat and changing dtypes.
"""

import numpy as np


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def from_python_objects() -> None:
    """Build arrays from lists / tuples / nested lists."""
    section("1️⃣  From Python lists and tuples")
    print("1-D :", np.array([1, 2, 3]))
    print("2-D :\n", np.array([[1, 2], [3, 4]]))
    print("3-D shape:", np.array([[[1], [2]], [[3], [4]]]).shape)
    print("From tuple:", np.array((5, 6, 7)))


def placeholder_arrays() -> None:
    """Arrays pre-filled with constant values."""
    section("2️⃣  Placeholder arrays")
    print("np.zeros((2, 3)):\n", np.zeros((2, 3)))
    print("np.ones((2, 3), dtype=int):\n", np.ones((2, 3), dtype=int))
    print("np.full((2, 2), 7):\n", np.full((2, 2), 7))
    print("np.eye(3):\n", np.eye(3))
    print("np.identity(2):\n", np.identity(2))
    # np.empty does NOT initialise memory – values are whatever was there.
    print("np.empty((2, 2)) shape:", np.empty((2, 2)).shape, "(values are garbage!)")


def ranges() -> None:
    """Evenly spaced numbers."""
    section("3️⃣  Ranges of numbers")
    print("np.arange(10)          :", np.arange(10))
    print("np.arange(2, 20, 3)    :", np.arange(2, 20, 3))
    print("np.arange(0, 1, 0.25)  :", np.arange(0, 1, 0.25))
    print("np.linspace(0, 1, 5)   :", np.linspace(0, 1, 5))
    print("np.logspace(0, 3, 4)   :", np.logspace(0, 3, 4))


def like_helpers() -> None:
    """Create arrays with the same shape as another array."""
    section("4️⃣  *_like helpers")
    template = np.array([[1, 2, 3], [4, 5, 6]])
    print("template:\n", template)
    print("np.zeros_like:\n", np.zeros_like(template))
    print("np.ones_like:\n", np.ones_like(template))
    print("np.full_like(template, 9):\n", np.full_like(template, 9))


def special_arrays() -> None:
    """Diagonal, repeated and tiled arrays, plus dtype conversion."""
    section("5️⃣  Special arrays")
    print("np.diag([1, 2, 3]):\n", np.diag([1, 2, 3]))
    print("np.repeat([1, 2], 3):", np.repeat([1, 2], 3))
    print("np.tile([1, 2], 3)  :", np.tile([1, 2], 3))
    print("np.arange(1, 10).reshape(3, 3):\n", np.arange(1, 10).reshape(3, 3))

    section("6️⃣  Changing dtype with astype()")
    floats = np.array([1.7, 2.2, 3.9])
    print("floats            :", floats)
    print("astype(int)       :", floats.astype(int), "(truncates, does not round)")
    print("astype(str)       :", floats.astype(str))
    print("bool array        :", np.array([0, 1, 2]).astype(bool))


if __name__ == "__main__":
    from_python_objects()
    placeholder_arrays()
    ranges()
    like_helpers()
    special_arrays()
