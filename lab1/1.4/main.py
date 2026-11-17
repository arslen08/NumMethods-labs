import sys
from jacobi import *


def read_matrix_from_file(file_path):
    matrix = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line and not line.startswith("#"):
                row = list(map(float, line.split()))
                matrix.append(row)

    return matrix


def print_matrix(M, name):
    print(f"\n   Матрица {name}:")

    for row in M:
        print("     ".join(f"{x:10.6f}" for x in row))


def main():
    file_path = sys.argv[1]
    eps = 0.01

    A = read_matrix_from_file(file_path)
    n = len(A)

    eigenvalues, V, k = jacobi_rotation_method(A, eps)

    print(f"Заданная точность вычислений: eps = {eps}")

    print("\nНайденные собственные значения:")
    for i, val in enumerate(eigenvalues):
        print(f"   λ[{i+1}] = {val:10.6f}")

    print("\n3. Собственные векторы и матрица V:")
    for j in range(n):
        vec = [V[i][j] for i in range(n)]
        vec_str = ", ".join(f"{x:9.6f}" for x in vec)
        print(f"   h[{j+1}] = ({vec_str})")

    print()
    print_matrix(V, "V (матрица собственных векторов)")

    Lambda = [
        [eigenvalues[i] if i == j else 0.0 for j in range(n)]
        for i in range(n)
    ]

    AV = mat_mul(A, V)
    VL = mat_mul(V, Lambda)

    print("\nПроверка A · V = V · Λ:")
    print_matrix(AV, "A · V")
    print_matrix(VL, "V · Λ")


if __name__ == "__main__":
    main()