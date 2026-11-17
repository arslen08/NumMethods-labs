import math

A = 3.0


def F(x):
    x1, x2 = x
    
    return [x1 ** 2 + x2 ** 2 - A ** 2,
            x1 - math.exp(x2) + A]


def jacobian(x):
    x1, x2 = x
    
    return [[2 * x1, 2 * x2],
            [1.0, -math.exp(x2)]]


def phi(x):
    x1, x2 = x
    
    return [math.sqrt(A ** 2 - x2 ** 2), math.log(x1 + A)]


def dphi_norm(x):
    x1, x2 = x
    row1 = abs(x2) / math.sqrt(A ** 2 - x2 ** 2)
    row2 = 1 / (x1 + A)
    
    return max(row1, row2)


def max_dphi_norm(x1_range, x2_range, n=100):
    q = 0.0
    
    for i in range(n + 1):
        for j in range(n + 1):
            x1 = x1_range[0] + (x1_range[1] - x1_range[0]) * i / n
            x2 = x2_range[0] + (x2_range[1] - x2_range[0]) * j / n
            q = max(q, dphi_norm([x1, x2]))
    
    return q


def solve_2x2(M, b):
    a = [M[0][:] + [b[0]], M[1][:] + [b[1]]]
    
    if abs(a[1][0]) > abs(a[0][0]):
        a[0], a[1] = a[1], a[0]
    
    k = a[1][0] / a[0][0]
    a[1] = [a[1][j] - k * a[0][j] for j in range(3)]
    x2 = a[1][2] / a[1][1]
    x1 = (a[0][2] - a[0][1] * x2) / a[0][0]
    
    return [x1, x2]


def norm(v):
    return max(abs(c) for c in v)


def simple_iteration(x0, eps, q, max_iter=10000):
    xs = [list(x0)]
    x = list(x0)
    
    for _ in range(max_iter):
        x_new = phi(x)
        xs.append(x_new)
    
        if q / (1 - q) * norm([x_new[i] - x[i] for i in range(2)]) < eps:
            return x_new, xs
        x = x_new
    
    return x, xs


def newton(x0, eps, max_iter=10000):
    xs = [list(x0)]
    x = list(x0)
    
    for _ in range(max_iter):
        dx = solve_2x2(jacobian(x), [-v for v in F(x)])
        x_new = [x[0] + dx[0], x[1] + dx[1]]
        xs.append(x_new)
    
        if norm(dx) < eps:
            return x_new, xs
    
        x = x_new
    
    return x, xs