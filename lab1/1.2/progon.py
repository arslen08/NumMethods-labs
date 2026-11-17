def check_diagonal_dominance(a, b, c):
    n = len(b)

    for i in range(n):
        abs_b = abs(b[i])
        abs_a = abs(a[i]) if i > 0 else 0.0
        abs_c = abs(c[i]) if i < n - 1 else 0.0

        if abs_b < (abs_a + abs_c):
            return False

    return True


def forward_step(a, b, c, d):
    n = len(b)
    P = [0.0] * n
    Q = [0.0] * n

    P[0] = -c[0] / b[0]
    Q[0] = d[0] / b[0]

    for i in range(1, n - 1):
        denom = b[i] + a[i] * P[i - 1]

        P[i] = -c[i] / denom
        Q[i] = (d[i] - a[i] * Q[i - 1]) / denom

    denom_n = b[n - 1] + a[n - 1] * P[n - 2]

    P[n - 1] = 0.0
    Q[n - 1] = (d[n - 1] - a[n - 1] * Q[n - 2]) / denom_n

    return P, Q


def backward_step(P, Q):
    n = len(P)
    x = [0.0] * n

    x[n - 1] = Q[n - 1]

    for i in range(n - 2, -1, -1):
        x[i] = P[i] * x[i + 1] + Q[i]

    return x


def solve_tridiagonal(a, b, c, d):
    P, Q = forward_step(a, b, c, d)
    x = backward_step(P, Q)

    return P, Q, x