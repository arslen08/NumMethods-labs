import math


def f(x):
    return math.log(x + 1) - 2 * x ** 2 + 1


def df(x):
    return 1 / (x + 1) - 4 * x


def phi(x):
    return math.sqrt((math.log(x + 1) + 1) / 2)


def dphi(x):
    return 1 / (4 * (x + 1) * phi(x))


def d2f(x):
    return -1 / (x + 1) ** 2 - 4


def max_abs(func, a, b, n=1000):
    return max(abs(func(a + (b - a) * i / n)) for i in range(n + 1))


def newton_start(a, b):
    return a if f(a) * d2f(a) > 0 else b


def simple_iteration(x0, eps, q, max_iter=10000):
    xs = [x0]
    x = x0
    
    for _ in range(max_iter):
        x_new = phi(x)
        xs.append(x_new)
    
        if q / (1 - q) * abs(x_new - x) < eps:
            return x_new, xs
    
        x = x_new
    
    return x, xs


def newton(x0, eps, max_iter=10000):
    xs = [x0]
    x = x0
    
    for _ in range(max_iter):
        x_new = x - f(x) / df(x)
        xs.append(x_new)
    
        if abs(x_new - x) < eps:
            return x_new, xs
    
        x = x_new
    
    return x, xs