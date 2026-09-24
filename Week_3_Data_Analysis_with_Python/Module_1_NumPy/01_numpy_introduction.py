"""
Module 1 · Script 01 – Installing NumPy & Introduction to NumPy Arrays
=====================================================================

Install NumPy (run once in your terminal / virtual environment):

    pip install numpy

This script shows:
  * how to import NumPy and check its version
  * what an ndarray is and its most important attributes
  * why NumPy arrays beat Python lists for numeric work (speed + vectorisation)
"""

import sys
import time

import numpy as np


def section(title: str) -> None:
    """Print a pretty section header so the output is easy to read."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def show_version() -> None:
    """Print Python and NumPy versions (useful when debugging installs)."""
    section("1️⃣  Checking the installation")
    print(f"Python version : {sys.version.split()[0]}")
    print(f"NumPy version  : {np.__version__}")


def array_basics() -> None:
    """Create a first array and inspect its attributes."""
    section("2️⃣  Your first NumPy array")
    marks = np.array([78, 85, 92, 66, 70])
    print("marks            :", marks)
    print("type(marks)      :", type(marks))
    print("marks.ndim       :", marks.ndim, "(number of dimensions)")
    print("marks.shape      :", marks.shape, "(length of each dimension)")
    print("marks.size       :", marks.size, "(total number of elements)")
    print("marks.dtype      :", marks.dtype, "(data type of every element)")
    print("marks.itemsize   :", marks.itemsize, "bytes per element")
    print("marks.nbytes     :", marks.nbytes, "bytes in total")

    section("3️⃣  A 2-D array (matrix)")
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(matrix)
    print("shape:", matrix.shape, "| ndim:", matrix.ndim, "| size:", matrix.size)

    section("4️⃣  Arrays are homogeneous (one dtype for all elements)")
    mixed = np.array([1, 2.5, 3])
    print("np.array([1, 2.5, 3]) ->", mixed, "dtype:", mixed.dtype)
    print("Upcast to string      ->", np.array([1, "two", 3.0]))
    print("Explicit dtype        ->", np.array([1, 2, 3], dtype=np.float32))


def list_vs_array() -> None:
    """Compare Python lists and NumPy arrays – behaviour and speed."""
    section("5️⃣  Python list vs NumPy array – behaviour")
    py_list = [1, 2, 3]
    arr = np.array(py_list)
    print("list * 2  ->", py_list * 2, "   (repeats the list!)")
    print("array * 2 ->", arr * 2, "        (multiplies every element)")
    print("list + [10] ->", py_list + [10], "(concatenation)")
    print("array + 10  ->", arr + 10, "     (element-wise addition)")

    section("6️⃣  Python list vs NumPy array – speed")
    n = 1_000_000
    numbers = list(range(n))
    numbers_arr = np.arange(n)

    start = time.perf_counter()
    _ = [x * x for x in numbers]
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    _ = numbers_arr * numbers_arr
    arr_time = time.perf_counter() - start

    print(f"Squaring {n:,} numbers")
    print(f"  list comprehension : {list_time * 1000:8.2f} ms")
    print(f"  NumPy vectorised   : {arr_time * 1000:8.2f} ms")
    if arr_time > 0:
        print(f"  NumPy was ~{list_time / arr_time:.0f}x faster")


if __name__ == "__main__":
    show_version()
    array_basics()
    list_vs_array()
