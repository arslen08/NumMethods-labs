import re
import sys
from progon import *


def parse_equation(line, n):
    parts = line.split("=")
    left_side, right_side = parts[0], parts[1]
    d_val = float(right_side.strip())

    coeffs = [0.0] * n

    pattern = re.compile(r"([+-]?\s*\d*\.?\d*)\s*x(\d+)")
    matches = pattern.findall(left_side)

    for coef_str, index_str in matches:
        idx = int(index_str) - 1
        coef_str = coef_str.replace(" ", "")

        if coef_str in ("", "+"):
            val = 1.0

        elif coef_str == "-":
            val = -1.0

        else:
            val = float(coef_str)

        if 0 <= idx < n:
            coeffs[idx] = val

    return coeffs, d_val


def read_system_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [
            line.strip()
            for line in f
            if line.strip()
        ]

    n = len(lines)

    a = [0.0] * n
    b = [0.0] * n
    c = [0.0] * n
    d = [0.0] * n

    for i in range(n):
        coeffs, d_val = parse_equation(lines[i], n)

        b[i] = coeffs[i]
        d[i] = d_val

        if i > 0:
            a[i] = coeffs[i - 1]

        if i < n - 1:
            c[i] = coeffs[i + 1]

    return a, b, c, d


def print_results(P, Q, x):
    n = len(x)

    print("Прогоночные коэффициенты:\n")
    print(f"{'i':<5} | {'P_i':<16} | {'Q_i':<16}")

    for i in range(n):
        print(f"{i+1:<5} | {P[i]:<16.6f} | {Q[i]:<16.6f}")

    print("\nВектор решения (X):\n")

    for i in range(n):
        print(f"{x[i]:10.6f}")


def main():
    file_path = sys.argv[1]

    a, b, c, d = read_system_from_file(file_path)

    if not check_diagonal_dominance(a, b, c):
        print(
            "Диагональное преобладание не выполняется"
        )

    P, Q, x = solve_tridiagonal(a, b, c, d)
    print_results(P, Q, x)


if __name__ == "__main__":
    main()