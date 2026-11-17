import sys
import numpy as np
from qr import *


def read_matrix_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    matrix = []

    for line in lines:
        row = [float(x) for x in line.split()]
        matrix.append(row)

    return matrix


def print_matrix(matrix, name, precision=6):
    print(f"\n{name}:")
    for row in matrix:
        print("  " + "  ".join(f"{val:>{precision + 6}.{precision}f}" for val in row))


def print_eigenvalues(eigenvalues, eps):
    """Выводит собственные значения."""
    print(f"\nНайденные собственные значения (eps = {eps}):")
    for idx, lam in enumerate(eigenvalues, 1):
        if isinstance(lam, complex):
            print(f"  λ{idx} = {lam.real:.6f} {lam.imag:+.6f}i")
        else:
            print(f"  λ{idx} = {lam:.6f}")


def main():
    file_path = sys.argv[1]

    A = read_matrix_from_file(file_path)
    print_matrix(A, "Исходная матрица A")

    Q, R = qr_decomposition(A)
    print_matrix(Q, "Матрица Q")
    print_matrix(R, "Матрица R")

    print_matrix(matmul(Q, R), "Проверка Q * R = А")

    eps = 0.01  
    eigenvalues, iters = qr_algorithm(A, eps=eps, max_iter=10000)
    print_eigenvalues(eigenvalues, eps)

    np_eig = np.linalg.eigvals(np.array(A, dtype=float))
    print("\nСобственные значения (NumPy, для сравнения):")
    for idx, lam in enumerate(np_eig, 1):
        if isinstance(lam, complex) or abs(lam.imag) > 1e-12:
            print(f"  λ{idx} = {lam.real:.6f} {lam.imag:+.6f}i")
        else:
            print(f"  λ{idx} = {lam.real:.6f}")


if __name__ == "__main__":
    main()