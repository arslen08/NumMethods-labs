import re
import sys
import numpy as np
from solver import *


def parse_system_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [
            line.strip()
            for line in f
            if line.strip()
        ]

    n = len(lines)
    A = [[0.0] * n for _ in range(n)]
    b = [0.0] * n

    pattern = re.compile(r"([+-]?\s*\d*\.?\d*)\s*x(\d+)")

    for i in range(n):
        parts = lines[i].split("=")
        left, right = parts[0], parts[1]
        b[i] = float(right.strip())

        matches = pattern.findall(left)

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
                A[i][idx] = val

    alpha = [[0.0] * n for _ in range(n)]
    beta = [0.0] * n

    for i in range(n):
        beta[i] = b[i] / A[i][i]

        for j in range(n):
            if i != j:
                alpha[i][j] = -A[i][j] / A[i][i]

    return alpha, beta, A, b


def check_diagonal_dominance(A):
    n = len(A)

    for i in range(n):
        diag = abs(A[i][i])
        off = sum(abs(A[i][j]) for j in range(n) if j != i)

        if diag <= off:
            return False

    return True


def main():
    file_path = sys.argv[1]

    eps = 0.01

    alpha, beta, A, b = parse_system_from_file(file_path)

    ok_diag = check_diagonal_dominance(A)

    print(f"Заданная точность: eps = {eps}")

    x_iter, k_iter = simple_iteration_method(alpha, beta, eps)
    x_seid, k_seid = seidel_method(alpha, beta, eps)

    x_exact = np.linalg.solve(np.array(A), np.array(b))

    print("\nКоличество итераций:")
    print(f"   Метод простых итераций: {k_iter}")
    print(f"   Метод Зейделя: {k_seid}")
    print("\nСравнение решений:")
    print(f"   {'i':>3} | {'Эталон':>12} | {'Прост. итер.':>12} | "
          f"{'Зейдель':>12}")
    print("   " + "-" * 78)

    for i in range(len(x_exact)):
        exact_i = x_exact[i]
        it_i = x_iter[i]
        se_i = x_seid[i]
        err_it = abs(it_i - exact_i)
        err_se = abs(se_i - exact_i)
        print(f"   {i + 1:>3} | {exact_i:>12.6f} | {it_i:>12.6f} | "
              f"{se_i:>12.6f}")

    print("\nСравнение методов по скорости сходимости:")
    print(
        f"   Метод Зейделя сошёлся на {k_iter - k_seid} итерации(-ий) быстрее "
        f"(в {k_iter / k_seid:.1f} раза)."
    )


if __name__ == "__main__":
    main()