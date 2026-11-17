import re
import sys
from gauss import *


def parse_equation(line, n):
    left, right = line.split("=", 1)
    rhs = float(right.strip())
    coeffs = [0.0] * n
    pattern = re.compile(r"([+-]?)\s*(\d*\.?\d*)\s*x\s*(\d+)")

    for sign, num_str, idx_str in pattern.findall(left):
        idx = int(idx_str) - 1
        val = float(num_str) if num_str else 1.0

        if sign == "-":
            val = -val

        coeffs[idx] += val

    return coeffs, rhs


def read_input(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    n = len(lines)
    A, B = [], []

    for ln in lines:
        coeffs, rhs = parse_equation(ln, n)
        A.append(coeffs)
        B.append(rhs)

    return A, B


def print_matrix(M, name, digits=6, tol=1e-12):
    print(f"\n{name}:")
    fmt = f"  {{:>{digits + 8}.{digits}f}}"

    for row in M:
        print("".join(fmt.format(0.0 if abs(v) < tol else v) for v in row))


def print_vector(v, name, digits=6, tol=1e-12):
    print(f"\n{name}:")
    fmt = f"  {{:>{digits + 8}.{digits}f}}"
    print("".join(fmt.format(0.0 if abs(x) < tol else x) for x in v))


def main():
    input_file = sys.argv[1]
    A, b = read_input(input_file)

    L, U, P, swaps = lu_decomposition(A)
    print_matrix(L, "Матрица L (нижняя треугольная)")
    print_matrix(U, "Матрица U (верхняя треугольная)")

    LU = mat_mul(L, U)
    print_matrix(LU, "L * U")

    print("\nПроверка (P * A = L * U)")
    PA = mat_mul(P, A)
    print_matrix(PA, "P * A")

    x = solve_lu(L, U, P, b)
    print_vector(x, "Решение системы A*x = b")

    A_inv = inverse_via_lu(L, U, P)
    print_matrix(A_inv, "Обратная матрица A^(-1) (через LU)")

    AA_inv = mat_mul(A, A_inv)
    print_matrix(AA_inv, "A * A^(-1)")

    det = determinant_from_lu(U, swaps)
    print(f"\nОпределитель det(A) = {det:.10f}")


if __name__ == "__main__":
    main()