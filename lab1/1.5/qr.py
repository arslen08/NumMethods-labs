import math


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def matmul(A, B):
    n = len(A)
    m = len(B[0])
    k = len(B)
    C = [[0.0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            s = 0.0
            for t in range(k):
                s += A[i][t] * B[t][j]

            C[i][j] = s

    return C


def copy_matrix(A):
    return [row[:] for row in A]


def householder_vector(b):
    n = len(b)
    norm_b = math.sqrt(sum(x * x for x in b))

    if norm_b == 0.0:
        return [0.0] * n

    sign_b0 = 1.0 if b[0] >= 0 else -1.0
    v = [0.0] * n
    v[0] = b[0] + sign_b0 * norm_b

    for i in range(1, n):
        v[i] = b[i]

    return v


def apply_householder_left(A, v, row_start):
    n = len(A)
    m = len(A[0])
    v_norm_sq = sum(x * x for x in v)

    if v_norm_sq == 0.0:
        return A

    w = [0.0] * m

    for j in range(m):
        s = 0.0

        for i in range(row_start, n):
            s += A[i][j] * v[i - row_start]

        w[j] = s

    factor = 2.0 / v_norm_sq

    for i in range(row_start, n):
        vi = v[i - row_start]

        for j in range(m):
            A[i][j] -= factor * vi * w[j]

    return A


def qr_decomposition(A):
    n = len(A)
    R = copy_matrix(A)
    Q = identity(n)

    for k in range(n - 1):
        b = [R[i][k] for i in range(k, n)]
        v = householder_vector(b)

        apply_householder_left(R, v, k)

        v_norm_sq = sum(x * x for x in v)

        if v_norm_sq == 0.0:
            continue

        factor = 2.0 / v_norm_sq

        for i in range(n):
            s = 0.0

            for t in range(k, n):
                s += Q[i][t] * v[t - k]

            for t in range(k, n):
                Q[i][t] -= factor * s * v[t - k]

    return Q, R


def qr_algorithm(A, eps=0.01, max_iter=100000):
    n = len(A)
    Ak = copy_matrix(A)
    tol = eps * eps

    it = 0

    for it in range(max_iter):
        Q, R = qr_decomposition(Ak)
        Ak = matmul(R, Q)

        off = 0.0

        for i in range(1, n):
            for j in range(i):
                off = max(off, abs(Ak[i][j]))

        if off < tol:
            break

    eigenvalues = extract_eigenvalues(Ak, tol)

    return eigenvalues, it + 1


def extract_eigenvalues(A, eps=1e-4):
    n = len(A)
    eigenvalues = []
    i = 0

    while i < n:
        if i == n - 1:
            eigenvalues.append(A[i][i])
            i += 1

        elif abs(A[i + 1][i]) < eps:
            eigenvalues.append(A[i][i])
            i += 1

        else:
            a = A[i][i]
            b = A[i][i + 1]
            c = A[i + 1][i]
            d = A[i + 1][i + 1]

            trace = a + d
            det = a * d - b * c
            disc = trace * trace - 4.0 * det

            if disc >= 0:
                sqrt_disc = math.sqrt(disc)
                eigenvalues.append((trace + sqrt_disc) / 2.0)
                eigenvalues.append((trace - sqrt_disc) / 2.0)

            else:
                sqrt_disc = math.sqrt(-disc)
                real = trace / 2.0
                imag = sqrt_disc / 2.0
                eigenvalues.append(complex(real, imag))
                eigenvalues.append(complex(real, -imag))
            i += 2

    return eigenvalues