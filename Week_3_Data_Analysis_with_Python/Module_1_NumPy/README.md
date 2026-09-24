# Module 1 – NumPy
> Week 3 · Data Analysis with Python   |   ⬅ Previous: [Week 2 – Module 9 MySQL Joins](../../Week_2_Data_Analysis_with_MySQL/Module_9_MySQL_Joins)  ·  Next ➡: [Module 2 – Introduction to Pandas](../Module_2_Introduction_to_Pandas)

## 🎯 Learning Objectives
- Install NumPy and explain why arrays beat Python lists for numeric work
- Create arrays in many ways (`array`, `zeros`, `arange`, `linspace`, `eye`, …)
- Index, slice, mask and reshape arrays confidently
- Use element-wise maths, broadcasting, aggregate and linear-algebra functions
- Generate reproducible random numbers within a range

## ✅ Syllabus Checklist
- [x] Installing NumPy | Introduction to NumPy Arrays
- [x] Different operations and functions on NumPy Arrays
- [x] NumPy operations and different functions
- [x] Creating different arrays using NumPy
- [x] Array Indexing and Slicing | Array Functions and Methods
- [x] Different Mathematical Functions | Different Matrix Operations
- [x] Random Numbers | Generate Numbers between a range

## 📖 Concepts

### Installing & importing
```bash
pip install numpy
```
```python
import numpy as np
```

### The `ndarray`
A NumPy array is a **grid of values that all share one dtype**, stored in one block of memory. That's why it is fast and why `arr * 2` multiplies every element (a list would repeat itself).

| Attribute | Meaning | `np.array([[1,2,3],[4,5,6]])` |
|---|---|---|
| `ndim` | number of dimensions | `2` |
| `shape` | size of each dimension | `(2, 3)` |
| `size` | total elements | `6` |
| `dtype` | element type | `int64` |

### Creating arrays
| Function | Example | Result |
|---|---|---|
| `np.zeros(shape)` | `np.zeros((2,2))` | 2×2 of 0.0 |
| `np.ones`, `np.full` | `np.full(3, 7)` | `[7 7 7]` |
| `np.eye(n)` | `np.eye(3)` | identity matrix |
| `np.arange(start, stop, step)` | `np.arange(0, 10, 3)` | `[0 3 6 9]` |
| `np.linspace(start, stop, n)` | `np.linspace(0, 1, 5)` | 5 evenly spaced incl. end |

### Indexing & slicing
`arr[start:stop:step]` for 1-D, `m[rows, cols]` for 2-D. Boolean masks: `arr[arr > 5]`. **Slices are views** – modifying them modifies the original; use `.copy()` when you need independence.

### Broadcasting
Arrays of different shapes can be combined if, comparing shapes from the right, each dimension is equal **or** one of them is 1:
```python
np.ones((2, 3)) + np.array([10, 20, 30])   # (2,3) + (3,) -> (2,3)
```

### The `axis` argument
`axis=0` collapses rows (result per **column**); `axis=1` collapses columns (result per **row**).

### Matrix operations
`A * B` is element-wise; `A @ B` (or `np.dot`, `np.matmul`) is the matrix product:
$$ (AB)_{ij} = \sum_k A_{ik} B_{kj} $$
`np.linalg` gives `det`, `inv`, `solve`, `eig`, `matrix_rank`.

### Random numbers
```python
rng = np.random.default_rng(seed=42)   # reproducible generator
rng.integers(1, 7, size=5)             # ints in [1, 7)
rng.uniform(10, 20, size=3)            # floats in [10, 20)
rng.normal(170, 10, size=1000)         # mean 170, std 10
```

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `numpy_basics.py` | The learner's original quick tour: creation, attributes, slicing, math, reshape, stacking, stats |
| `01_numpy_introduction.py` | Install check, ndarray attributes, list vs array behaviour & speed |
| `02_array_creation.py` | `array`, `zeros`, `ones`, `full`, `eye`, `arange`, `linspace`, `*_like`, `diag`, `astype` |
| `03_array_operations.py` | Element-wise arithmetic, comparisons, broadcasting, ufuncs, aggregates & `axis` |
| `04_indexing_slicing.py` | 1-D/2-D/3-D indexing, slicing, fancy & boolean indexing, view vs copy |
| `05_array_functions_methods.py` | reshape/ravel/transpose, concatenate/stack/split, sort/argsort/unique/where, insert/append/delete |
| `06_mathematical_functions.py` | Rounding, powers/logs, trig, statistics, cumulative functions, NaN-aware functions |
| `07_matrix_operations.py` | `@`/dot, transpose, determinant, inverse, rank, trace, `linalg.solve`, eigenvalues |
| `08_random_numbers.py` | `default_rng`, seeds, numbers in a range, distributions, choice/shuffle, legacy API |

## ▶️ How to Run
```bash
cd Week_3_Data_Analysis_with_Python/Module_1_NumPy
python 01_numpy_introduction.py
python 02_array_creation.py
# … and so on up to 08_random_numbers.py
python numpy_basics.py
```

## 🧠 Key Takeaways
- Arrays are homogeneous and vectorised: write `arr * 2`, not a loop.
- Slices are views; `.copy()` when you need a separate array.
- Learn `axis=0` (down the columns) vs `axis=1` (across the rows).
- `*` is element-wise, `@` is matrix multiplication.
- Always seed your random generator for reproducible experiments.

## 📝 Practice Exercises
1. Create a 5×5 array with values 1–25 and extract its border elements only.
2. Given `scores = rng.integers(0, 101, 30)`, count how many are ≥ 40 and replace all < 40 with 40.
3. Normalise each column of a random 4×3 matrix to mean 0 and std 1 using broadcasting.
4. Solve the system `x + 2y + z = 8`, `2x - y + 3z = 13`, `3x + y - z = 2` with `np.linalg.solve`.
5. Simulate rolling two dice 10,000 times and find the most common total.
