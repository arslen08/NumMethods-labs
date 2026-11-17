import math


def get_max_off_diagonal(A):
    n = len(A)
    p, q = 0, 1
    max_val = 0.0

    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[i][j]) > max_val:
                max_val = abs(A[i][j])
                p, q = i, j

    return p, q, max_val


def off_diagonal_norm(A):
    n = len(A)
    s = 0.0

    for i in range(n):
        for j in range(i + 1, n):
            s += A[i][j] ** 2

    return math.sqrt(2 * s)


def mat_mul(A, B):
    n = len(A)
    C = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))

    return C


def transpose(A):
    n = len(A)

    return [[A[j][i] for j in range(n)] for i in range(n)]


def jacobi_rotation_method(A_init, eps):
    n = len(A_init)
    A = [row.copy() for row in A_init]

    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    k = 0

    while True:
        p, q, max_val = get_max_off_diagonal(A)

        if off_diagonal_norm(A) < eps:
            break

        k += 1

        if abs(A[p][p] - A[q][q]) < 1e-12:
            phi = math.pi / 4

        else:
            phi = 0.5 * math.atan(2 * A[p][q] / (A[p][p] - A[q][q]))

        c = math.cos(phi)
        s = math.sin(phi)

        U = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        U[p][p] = c
        U[p][q] = -s
        U[q][p] = s
        U[q][q] = c

        UT = transpose(U)
        A = mat_mul(mat_mul(UT, A), U)

        V = mat_mul(V, U)

    eigenvalues = [A[i][i] for i in range(n)]

    return eigenvalues, V, k