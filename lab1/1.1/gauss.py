def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    C = [[0.0] * m for _ in range(n)]

    for i in range(n):
        Ai = A[i]
        Ci = C[i]

        for l in range(k):
            a = Ai[l]

            if a == 0.0:
                continue

            Bl = B[l]

            for j in range(m):
                Ci[j] += a * Bl[j]

    return C


def mat_vec(A, x):
    n = len(A)
    y = [0.0] * n

    for i in range(n):
        s = 0.0
        Ai = A[i]

        for j in range(n):
            s += Ai[j] * x[j]

        y[i] = s

    return y


def lu_decomposition(A):
    n = len(A)
    U = [row[:] for row in A]
    L = identity(n)
    P = identity(n)
    swaps = 0

    for k in range(n):
        pivot_row, pivot_val = k, abs(U[k][k])

        for i in range(k + 1, n):
            if abs(U[i][k]) > pivot_val:
                pivot_val, pivot_row = abs(U[i][k]), i

        if pivot_row != k:
            U[k], U[pivot_row] = U[pivot_row], U[k]
            P[k], P[pivot_row] = P[pivot_row], P[k]
            L[k][:k], L[pivot_row][:k] = L[pivot_row][:k], L[k][:k]
            swaps += 1

        pivot = U[k][k]

        for i in range(k + 1, n):
            factor = U[i][k] / pivot
            L[i][k] = factor

            if factor == 0.0:
                continue

            Ui = U[i]
            Uk = U[k]

            for j in range(k, n):
                Ui[j] -= factor * Uk[j]

    return L, U, P, swaps


def forward_substitution(L, b):
    n = len(L)
    y = [0.0] * n

    for i in range(n):
        s = b[i]
        Li = L[i]

        for j in range(i):
            s -= Li[j] * y[j]

        y[i] = s

    return y


def backward_substitution(U, y):
    n = len(U)
    x = [0.0] * n

    for i in range(n - 1, -1, -1):
        s = y[i]
        Ui = U[i]

        for j in range(i + 1, n):
            s -= Ui[j] * x[j]

        x[i] = s / Ui[i]

    return x


def solve_lu(L, U, P, b):
    n = len(b)
    Pb = [sum(P[i][j] * b[j] for j in range(n)) for i in range(n)]
    y = forward_substitution(L, Pb)

    return backward_substitution(U, y)


def inverse_via_lu(L, U, P):
    n = len(L)
    inv = [[0.0] * n for _ in range(n)]

    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        Pe = [P[i][j] for i in range(n)]
        y = forward_substitution(L, Pe)
        x = backward_substitution(U, y)

        for i in range(n):
            inv[i][j] = x[i]

    return inv


def determinant_from_lu(U, swaps):
    det = 1.0

    for i in range(len(U)):
        det *= U[i][i]

    return det * ((-1) ** swaps)