import math


def left_rectangles(f, a, b, h):
    n = int(round((b - a) / h))
    s = 0.0
    x = a
    for i in range(n):
        s += f(x)
        x += h
    return s * h


def right_rectangles(f, a, b, h):
    n = int(round((b - a) / h))
    s = 0.0
    x = a + h
    for i in range(n):
        s += f(x)
        x += h
    return s * h


def mid_rectangles(f, a, b, h):
    n = int(round((b - a) / h))
    s = 0.0
    x = a + h / 2.0
    for i in range(n):
        s += f(x)
        x += h
    return s * h


def trapezoidal(f, a, b, h):
    n = int(round((b - a) / h))
    s = (f(a) + f(b)) / 2.0
    x = a + h
    for i in range(1, n):
        s += f(x)
        x += h
    return s * h


def simpson(f, a, b, h):
    n = int(round((b - a) / h))
    if n % 2 != 0:
        n += 1
        h = (b - a) / n
    s = f(a) + f(b)
    x = a + h
    for i in range(1, n):
        coef = 4.0 if i % 2 == 1 else 2.0
        s += coef * f(x)
        x += h
    return s * h / 3.0


def runge_romberg(F_h, F_kh, k, p):
    return F_h + (F_h - F_kh) / (k ** p - 1.0)


def estimate_error(F_h, F_kh, k, p):
    return abs(F_h - F_kh) / (k ** p - 1.0)