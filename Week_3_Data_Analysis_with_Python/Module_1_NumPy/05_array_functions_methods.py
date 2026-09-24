"""
Module 1 · Script 05 – Array Functions and Methods
==================================================

Covers: reshape / ravel / flatten / transpose, concatenate / stack / split,
sort / argsort, unique, where, clip, insert / append / delete, and searching.
"""

import numpy as np


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def reshaping() -> None:
    """Change the shape of an array without changing its data."""
    section("1️⃣  Reshaping")
    arr = np.arange(12)
    print("arr:", arr)
    print("reshape(3, 4):\n", arr.reshape(3, 4))
    print("reshape(2, -1)  (-1 = 'work it out'):\n", arr.reshape(2, -1))
    m = arr.reshape(3, 4)
    print("m.T (transpose) shape:", m.T.shape)
    print("m.ravel()   :", m.ravel(), "(view when possible)")
    print("m.flatten() :", m.flatten(), "(always a copy)")
    print("np.expand_dims(arr, 0).shape:", np.expand_dims(arr, 0).shape)


def joining_splitting() -> None:
    """Combine arrays and split them apart."""
    section("2️⃣  Joining and splitting")
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    print("concatenate axis=0:\n", np.concatenate([a, b], axis=0))
    print("concatenate axis=1:\n", np.concatenate([a, b], axis=1))
    print("np.stack([a, b]).shape:", np.stack([a, b]).shape, "(new axis)")
    print("vstack:\n", np.vstack([a, b]))
    print("hstack:\n", np.hstack([a, b]))
    parts = np.split(np.arange(9), 3)
    print("np.split(arange(9), 3):", parts)
    print("np.array_split(arange(7), 3):", np.array_split(np.arange(7), 3))


def sorting_searching() -> None:
    """Sort arrays and find things in them."""
    section("3️⃣  Sorting and searching")
    arr = np.array([42, 7, 19, 7, 88, 3])
    print("arr              :", arr)
    print("np.sort(arr)     :", np.sort(arr))
    print("descending       :", np.sort(arr)[::-1])
    print("np.argsort(arr)  :", np.argsort(arr), "(indices that would sort)")
    print("np.unique(arr)   :", np.unique(arr))
    values, counts = np.unique(arr, return_counts=True)
    print("unique + counts  :", dict(zip(values.tolist(), counts.tolist())))
    print("np.where(arr > 10):", np.where(arr > 10), "(positions)")
    print("np.where(arr > 10, 'big', 'small'):", np.where(arr > 10, "big", "small"))
    print("np.argmax / argmin:", np.argmax(arr), "/", np.argmin(arr))
    print("np.searchsorted([1,3,5,7], 4):", np.searchsorted([1, 3, 5, 7], 4))
    m = np.array([[3, 1, 2], [9, 7, 8]])
    print("sort each row (axis=1):\n", np.sort(m, axis=1))


def editing() -> None:
    """Insert, append, delete and clip values (each returns a NEW array)."""
    section("4️⃣  Insert / append / delete / clip")
    arr = np.array([1, 2, 3, 4, 5])
    print("np.append(arr, [6, 7]) :", np.append(arr, [6, 7]))
    print("np.insert(arr, 1, 99)  :", np.insert(arr, 1, 99))
    print("np.delete(arr, [0, -1]):", np.delete(arr, [0, -1]))
    print("np.clip(arr, 2, 4)     :", np.clip(arr, 2, 4))
    print("arr unchanged          :", arr)


if __name__ == "__main__":
    reshaping()
    joining_splitting()
    sorting_searching()
    editing()
