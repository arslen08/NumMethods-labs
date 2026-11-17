def solve_linear_system(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for col in range(n):
        max_row = col
        max_val = abs(M[col][col])
        for row in range(col + 1, n):
            if abs(M[row][col]) > max_val:
                max_val = abs(M[row][col])
                max_row = row
        if max_row != col:
            M[col], M[max_row] = M[max_row], M[col]

        pivot = M[col][col]
        if abs(pivot) < 1e-15:
            raise ValueError("Матрица вырождена или плохо обусловлена")

        for row in range(col + 1, n):
            factor = M[row][col] / pivot
            for j in range(col, n + 1):
                M[row][j] -= factor * M[col][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        x[i] = s / M[i][i]

    return x


def build_normal_system(x_nodes, y_nodes, degree):
    n_points = len(x_nodes)
    m = degree + 1  

    A = [[0.0 for _ in range(m)] for _ in range(m)]
    b = [0.0 for _ in range(m)]

    for k in range(m):
        for j in range(m):
            s = 0.0
            for i in range(n_points):
                s += x_nodes[i] ** (k + j)
            A[k][j] = s
        s = 0.0
        for i in range(n_points):
            s += y_nodes[i] * (x_nodes[i] ** k)
        b[k] = s

    return A, b


def solve_mnk(x_nodes, y_nodes, degree):
    A, b = build_normal_system(x_nodes, y_nodes, degree)
    coeffs = solve_linear_system(A, b)
    return coeffs


def evaluate_poly(coeffs, x):
    result = 0.0
    for a in reversed(coeffs):
        result = result * x + a
    return result


def compute_mse(x_nodes, y_nodes, coeffs):
    sse = 0.0
    for i in range(len(x_nodes)):
        pred = evaluate_poly(coeffs, x_nodes[i])
        sse += (pred - y_nodes[i]) ** 2
    return sse


def poly_to_string(coeffs, name="P"):
    terms = []
    for i, a in enumerate(coeffs):
        if abs(a) < 1e-12:
            continue
        if i == 0:
            terms.append(f"{a:.6f}")
        elif i == 1:
            sign = "+" if a >= 0 else "-"
            terms.append(f" {sign} {abs(a):.6f}*x")
        else:
            sign = "+" if a >= 0 else "-"
            terms.append(f" {sign} {abs(a):.6f}*x^{i}")
    if not terms:
        return f"{name}(x) = 0"
    s = "".join(terms).lstrip(" +")
    return f"{name}(x) = {s}"