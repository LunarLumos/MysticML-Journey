"""
Module 1 · Script 03 – Operations and Functions on NumPy Arrays
===============================================================

Covers: element-wise arithmetic, comparison operators, broadcasting,
universal functions (ufuncs), aggregate functions and the `axis` argument.
"""

import numpy as np


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def arithmetic() -> None:
    """Element-wise arithmetic between arrays and with scalars."""
    section("1️⃣  Element-wise arithmetic")
    a = np.array([10, 20, 30, 40])
    b = np.array([1, 2, 3, 4])
    print("a      =", a)
    print("b      =", b)
    print("a + b  =", a + b)
    print("a - b  =", a - b)
    print("a * b  =", a * b)
    print("a / b  =", a / b)
    print("a // b =", a // b)
    print("a % 3  =", a % 3)
    print("b ** 2 =", b**2)


def comparisons() -> None:
    """Comparison operators return boolean arrays."""
    section("2️⃣  Comparisons -> boolean arrays")
    scores = np.array([45, 82, 67, 91, 38])
    passed = scores >= 50
    print("scores        :", scores)
    print("scores >= 50  :", passed)
    print("how many pass :", passed.sum())
    print("any > 90?     :", np.any(scores > 90))
    print("all > 30?     :", np.all(scores > 30))
    print("array_equal   :", np.array_equal([1, 2], np.array([1, 2])))


def broadcasting() -> None:
    """Show how NumPy stretches smaller arrays to match bigger ones."""
    section("3️⃣  Broadcasting")
    matrix = np.arange(1, 7).reshape(2, 3)
    row = np.array([10, 20, 30])
    col = np.array([[100], [200]])
    print("matrix (2x3):\n", matrix)
    print("matrix + 5 (scalar is broadcast):\n", matrix + 5)
    print("matrix + row (1x3 stretched down):\n", matrix + row)
    print("matrix + col (2x1 stretched across):\n", matrix + col)
    print("Rule: trailing dimensions must be equal or one of them must be 1.")


def ufuncs() -> None:
    """Universal functions operate on every element."""
    section("4️⃣  Universal functions (ufuncs)")
    x = np.array([1, 4, 9, 16])
    print("x           :", x)
    print("np.sqrt(x)  :", np.sqrt(x))
    print("np.square(x):", np.square(x))
    print("np.log(x)   :", np.round(np.log(x), 3))
    print("np.add(x, 1):", np.add(x, 1))
    print("np.maximum(x, 5):", np.maximum(x, 5))


def aggregates() -> None:
    """Summary statistics, overall and along an axis."""
    section("5️⃣  Aggregate functions and axis")
    sales = np.array([[120, 150, 90], [200, 80, 110]])
    print("sales (rows = shops, cols = days):\n", sales)
    print("sum()        :", sales.sum())
    print("sum(axis=0)  :", sales.sum(axis=0), "-> per column (per day)")
    print("sum(axis=1)  :", sales.sum(axis=1), "-> per row (per shop)")
    print("mean()       :", sales.mean())
    print("min / max    :", sales.min(), "/", sales.max())
    print("argmax()     :", sales.argmax(), "(index in the flattened array)")
    print("std()        :", round(sales.std(), 2))
    print("cumsum()     :", sales.cumsum())
    print("median       :", np.median(sales))
    print("percentile 75:", np.percentile(sales, 75))


if __name__ == "__main__":
    arithmetic()
    comparisons()
    broadcasting()
    ufuncs()
    aggregates()
