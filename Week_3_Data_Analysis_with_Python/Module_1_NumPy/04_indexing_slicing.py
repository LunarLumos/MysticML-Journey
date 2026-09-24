"""
Module 1 · Script 04 – Array Indexing and Slicing
=================================================

Covers: indexing 1-D/2-D/3-D arrays, negative indices, slicing with steps,
fancy (integer-list) indexing, boolean masking and the view-vs-copy trap.
"""

import numpy as np


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def one_dimensional() -> None:
    """Indexing and slicing a 1-D array."""
    section("1️⃣  1-D indexing & slicing   arr[start:stop:step]")
    arr = np.arange(10, 100, 10)
    print("arr        :", arr)
    print("arr[0]     :", arr[0])
    print("arr[-1]    :", arr[-1])
    print("arr[2:5]   :", arr[2:5])
    print("arr[:3]    :", arr[:3])
    print("arr[::2]   :", arr[::2])
    print("arr[::-1]  :", arr[::-1], "(reversed)")


def two_dimensional() -> None:
    """Indexing and slicing a 2-D array (rows, columns)."""
    section("2️⃣  2-D indexing & slicing   arr[rows, cols]")
    m = np.arange(1, 13).reshape(3, 4)
    print("m:\n", m)
    print("m[1, 2]      :", m[1, 2], "(row 1, col 2)")
    print("m[-1, -1]    :", m[-1, -1])
    print("m[0]         :", m[0], "(whole first row)")
    print("m[:, 1]      :", m[:, 1], "(whole second column)")
    print("m[0:2, 1:3]:\n", m[0:2, 1:3])
    print("m[::2, ::2]:\n", m[::2, ::2])


def three_dimensional() -> None:
    """A quick look at 3-D indexing (depth, rows, cols)."""
    section("3️⃣  3-D indexing")
    cube = np.arange(24).reshape(2, 3, 4)
    print("cube.shape      :", cube.shape)
    print("cube[1]:\n", cube[1])
    print("cube[1, 2, 3]   :", cube[1, 2, 3])
    print("cube[:, 0, 0]   :", cube[:, 0, 0])


def fancy_and_boolean() -> None:
    """Select with lists of indices or with boolean masks."""
    section("4️⃣  Fancy indexing (list of positions)")
    arr = np.array([5, 15, 25, 35, 45])
    print("arr[[0, 2, 4]] :", arr[[0, 2, 4]])
    m = np.arange(1, 10).reshape(3, 3)
    print("m[[0, 2]] (rows 0 and 2):\n", m[[0, 2]])

    section("5️⃣  Boolean indexing (masks)")
    temps = np.array([18, 25, 31, 12, 28, 35])
    print("temps               :", temps)
    print("temps > 25          :", temps > 25)
    print("temps[temps > 25]   :", temps[temps > 25])
    print("(temps>15)&(temps<30):", temps[(temps > 15) & (temps < 30)])
    print("(temps<15)|(temps>30):", temps[(temps < 15) | (temps > 30)])
    hot = temps.copy()
    hot[hot > 30] = 30
    print("clip hot days to 30 :", hot)


def view_vs_copy() -> None:
    """Slices are VIEWS – changing them changes the original."""
    section("6️⃣  View vs copy")
    original = np.array([1, 2, 3, 4, 5])
    view = original[1:4]
    view[0] = 99
    print("After changing the slice, original =", original, "<- changed!")

    original = np.array([1, 2, 3, 4, 5])
    copy = original[1:4].copy()
    copy[0] = 99
    print("After changing a .copy(), original =", original, "<- unchanged")


if __name__ == "__main__":
    one_dimensional()
    two_dimensional()
    three_dimensional()
    fancy_and_boolean()
    view_vs_copy()
