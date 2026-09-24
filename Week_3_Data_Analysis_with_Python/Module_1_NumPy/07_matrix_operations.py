"""
Module 1 · Script 07 – Different Matrix Operations
==================================================

Covers: element-wise vs matrix multiplication, dot/matmul/@, transpose,
determinant, inverse, rank, trace, solving linear systems, eigenvalues
and the outer product.
"""

import numpy as np


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def multiplication() -> None:
    """Element-wise product vs true matrix product."""
    section("1️⃣  Element-wise vs matrix multiplication")
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print("A:\n", A)
    print("B:\n", B)
    print("A * B  (element-wise):\n", A * B)
    print("A @ B  (matrix product):\n", A @ B)
    print("np.dot(A, B) == np.matmul(A, B) == A @ B:",
          np.array_equal(np.dot(A, B), np.matmul(A, B)))
    print("Dot product of vectors [1,2,3]·[4,5,6] =", np.dot([1, 2, 3], [4, 5, 6]))


def matrix_properties() -> None:
    """Transpose, determinant, inverse, rank and trace."""
    section("2️⃣  Transpose, determinant, inverse, rank, trace")
    A = np.array([[4, 7], [2, 6]])
    print("A:\n", A)
    print("A.T:\n", A.T)
    det = np.linalg.det(A)
    print("det(A)   :", round(det, 3))
    A_inv = np.linalg.inv(A)
    print("inv(A):\n", A_inv.round(3))
    print("A @ inv(A) ≈ I:\n", (A @ A_inv).round(3))
    print("rank(A)  :", np.linalg.matrix_rank(A))
    print("trace(A) :", np.trace(A), "(sum of diagonal)")


def linear_system() -> None:
    """Solve   2x + y = 5   and   x + 3y = 10."""
    section("3️⃣  Solving a system of linear equations")
    coefficients = np.array([[2, 1], [1, 3]])
    constants = np.array([5, 10])
    solution = np.linalg.solve(coefficients, constants)
    print("2x +  y = 5")
    print(" x + 3y = 10")
    print(f"Solution: x = {solution[0]:.2f}, y = {solution[1]:.2f}")
    print("Check (A @ solution):", coefficients @ solution)


def eigen_and_outer() -> None:
    """Eigenvalues/eigenvectors and outer product."""
    section("4️⃣  Eigenvalues & eigenvectors")
    M = np.array([[2, 0], [0, 3]])
    values, vectors = np.linalg.eig(M)
    print("M:\n", M)
    print("eigenvalues :", values)
    print("eigenvectors:\n", vectors)

    section("5️⃣  Outer product & identity")
    print("np.outer([1,2,3], [1,2]):\n", np.outer([1, 2, 3], [1, 2]))
    I = np.eye(2)
    A = np.array([[1, 2], [3, 4]])
    print("A @ I == A:", np.array_equal(A @ I, A))


if __name__ == "__main__":
    multiplication()
    matrix_properties()
    linear_system()
    eigen_and_outer()
