import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from methods import (
    get_nodes_and_values,
    lagrange_poly,
    format_lagrange_poly,
    divided_differences_table,
    newton_poly,
    format_newton_poly
)


def solve_variant(x_nodes, x_star, label):
    y_nodes = get_nodes_and_values(x_nodes)
    dd_table = divided_differences_table(x_nodes, y_nodes)

    val_lagrange = lagrange_poly(x_star, x_nodes, y_nodes)
    val_newton = newton_poly(x_star, x_nodes, dd_table)
    exact_val = math.asin(x_star)

    abs_error = abs(exact_val - val_lagrange)
    diff_lagrange_newton = abs(val_lagrange - val_newton)

    print("\n")
    print(f"ВАРИАНТ {label}: X_i = {x_nodes}, X* = {x_star}")
 
    print("\n1. Исходные узлы интерполяции x_i и значения функции y_i:")
    for i in range(len(x_nodes)):
        print(f"   x_{i} = {x_nodes[i]:5.2f} | y_{i} = {y_nodes[i]:.6f}")

    print("\n2. Интерполяционный многочлен Лагранжа:")
    print(format_lagrange_poly(x_nodes, y_nodes))

    print("\n3. Таблица разделенных разностей:")
    headers = ["x_i", "y_i (0)", "1-й пор.", "2-й пор.", "3-й пор."]
    print(f"   {headers[0]:<6} | {headers[1]:<10} | {headers[2]:<10} | {headers[3]:<10} | {headers[4]:<10}")
    print("   " + "-" * 58)
    for i in range(len(x_nodes)):
        row_str = f"   {x_nodes[i]:<6.2f} | "
        for j in range(len(x_nodes) - i):
            row_str += f"{dd_table[i][j]:<10.6f} | "
        print(row_str)

    print("\n4. Интерполяционный многочлен Ньютона:")
    print(format_newton_poly(x_nodes, dd_table))

    print(f"\n5. Результаты вычислений в точке x* = {x_star}:")
    print(f"   • Значение многочлена Лагранжа L_3(x*): {val_lagrange:.5f}")
    print(f"   • Значение многочлена Ньютона N_3(x*):  {val_newton:.5f}")
    print(f"   • Точное значение функции f(x*):        {exact_val:.5f}")
    print(f"   • Абсолютная погрешность интерполяции:   {abs_error:.5f}")
    print(f"   • Разность между Лагранжем и Ньютоном:  {diff_lagrange_newton:.2e}")

    return x_nodes, y_nodes, dd_table, val_lagrange


def main():
    x_star = 0.1

    nodes_a = [-0.4, -0.1, 0.2, 0.5]
    data_a = solve_variant(nodes_a, x_star, "А")

    nodes_b = [-0.4, 0.0, 0.2, 0.5]
    data_b = solve_variant(nodes_b, x_star, "Б")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    lo, hi = -0.45, 0.55
    xs = [lo + (hi - lo) * i / 300 for i in range(301)]
    y_exact = [math.asin(x) for x in xs]

    variants = [
        (ax1, data_a, "а) X_i = -0.4, -0.1, 0.2, 0.5"),
        (ax2, data_b, "б) X_i = -0.4, 0.0, 0.2, 0.5")
    ]

    for ax, (x_nodes, y_nodes, dd_table, val_lagrange), subtitle in variants:
        y_lagrange = [lagrange_poly(x, x_nodes, y_nodes) for x in xs]
        y_newton = [newton_poly(x, x_nodes, dd_table) for x in xs]

        ax.plot(xs, y_exact, "b-", lw=2, label=r"Исходная $f(x) = \arcsin(x)$")
        ax.plot(xs, y_lagrange, "r--", lw=2, label=r"Многочлен Лагранжа $L_3(x)$")
        ax.plot(xs, y_newton, "g:", lw=2.5, label=r"Многочлен Ньютона $N_3(x)$")

        ax.scatter(x_nodes, y_nodes, color="blue", s=50, zorder=5, label="Узлы интерполяции")
        
        ax.scatter([x_star], [val_lagrange], color="red", marker="*", s=150, zorder=6, 
                   label=f"$x^* = {x_star}$ (y={val_lagrange:.5f})")

        ax.set_title(f"Вариант {subtitle}", fontsize=12)
        ax.set_xlabel("x", fontsize=11)
        ax.set_ylabel("y", fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend(loc="best", fontsize=10)
        ax.set_xlim(lo, hi)

    fig.suptitle("Интерполяция функции arcsin(x) (Вариант 8)", fontsize=14)
    fig.tight_layout()

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "interpolation_graphs.png")
    fig.savefig(out, dpi=150)
    print(f"\nГрафики успешно сохранены в {out}")


if __name__ == "__main__":
    main()