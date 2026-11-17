import math
from methods import (
    left_rectangles, right_rectangles, mid_rectangles,
    trapezoidal, simpson,
    runge_romberg, estimate_error
)


def f(x):
    return 1.0 / (x * x + 4.0)


def main():
    a = -2.0
    b = 2.0
    h1 = 1.0
    h2 = 0.5
    k = h1 / h2  # = 2

    exact = 0.5 * (math.atan(b / 2.0) - math.atan(a / 2.0))

    methods = [
        ("Левые прямоугольники", left_rectangles, 1),
        ("Правые прямоугольники", right_rectangles, 1),
        ("Средние прямоугольники", mid_rectangles, 2),
        ("Трапеций", trapezoidal, 2),
        ("Симпсона", simpson, 4),
    ]

    results = []
    for name, method, p in methods:
        I_h1 = method(f, a, b, h1)
        I_h2 = method(f, a, b, h2)
        I_rr = runge_romberg(I_h2, I_h1, k, p)  
        err_est = estimate_error(I_h2, I_h1, k, p)
        abs_err_h2 = abs(I_h2 - exact)
        abs_err_rr = abs(I_rr - exact)
        results.append({
            "name": name,
            "p": p,
            "I_h1": I_h1,
            "I_h2": I_h2,
            "I_rr": I_rr,
            "err_est": err_est,
            "abs_err_h2": abs_err_h2,
            "abs_err_rr": abs_err_rr,
        })

    print("ЗАДАЧА 3.5: ЧИСЛЕННОЕ ИНТЕГРИРОВАНИЕ")
    print(f"\nФункция: f(x) = 1/(x² + 4)")
    print(f"Отрезок: [{a}, {b}]")
    print(f"Шаги: h1 = {h1}, h2 = {h2}")
    print(f"Точное значение интеграла: {exact:.10f}")

    print("\n" + "-" * 95)
    print(f"{'Метод':<24} | {'I(h1)':>12} | {'I(h2)':>12} | {'p':>3} | {'I_RR':>12} | {'Оц.погр.h2':>12}")
    print("-" * 95)

    for r in results:
        print(f"{r['name']:<24} | {r['I_h1']:12.8f} | {r['I_h2']:12.8f} | {r['p']:3d} | "
              f"{r['I_rr']:12.8f} | {r['err_est']:12.2e}")

    print("-" * 95)

    print("\nАбсолютные погрешности (относительно точного значения):")
    print(f"{'Метод':<24} | {'|I(h2)-exact|':>14} | {'|I_RR-exact|':>14}")
    print("-" * 60)
    for r in results:
        print(f"{r['name']:<24} | {r['abs_err_h2']:14.2e} | {r['abs_err_rr']:14.2e}")

    best = min(results, key=lambda r: r['abs_err_rr'])
    print(f"\nНаиболее точный результат дал метод: {best['name']}")
    print(f"  (уточнённое значение I_RR = {best['I_rr']:.10f}, "
          f"абс. погрешность = {best['abs_err_rr']:.2e})")

if __name__ == "__main__":
    main()