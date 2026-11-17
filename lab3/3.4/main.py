import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from methods import (
    first_derivative_order1,
    first_derivative_left_right,
    first_derivative_order2,
    second_derivative,
)


def main():
    x_star = 1.0
    x_nodes = [-1.0, 0.0, 1.0, 2.0, 3.0]
    y_nodes = [-0.7854, 0.0, 0.78540, 1.1071, 1.249]

    d1_simple, nodes_simple = first_derivative_order1(x_nodes, y_nodes, x_star)

    d1_left, nodes_left, d1_right, nodes_right = first_derivative_left_right(x_nodes, y_nodes, x_star)

    d1_order2, nodes_order2 = first_derivative_order2(x_nodes, y_nodes, x_star)

    d2, nodes_d2 = second_derivative(x_nodes, y_nodes, x_star)

    print("ЗАДАЧА 3.4: ЧИСЛЕННОЕ ДИФФЕРЕНЦИРОВАНИЕ")

    print("\n1. Исходная таблица значений функции:")
    print(f"   {'i':<3} | {'x_i':<8} | {'y_i':<10}")
    print("   " + "-" * 26)
    for i in range(len(x_nodes)):
        print(f"   {i:<3} | {x_nodes[i]:<8.1f} | {y_nodes[i]:<10.5f}")

    print(f"\n2. Точка, в которой выполняется вычисление: x* = {x_star}")

    print("\n3. Узлы, использованные при вычислении:")
    print(f"   • Для производной 1-го порядка (простая): узлы {nodes_simple} → x = {[x_nodes[k] for k in nodes_simple]}")
    print(f"   • Левосторонняя: узлы {nodes_left} → x = {[x_nodes[k] for k in nodes_left]}")
    print(f"   • Правосторонняя: узлы {nodes_right} → x = {[x_nodes[k] for k in nodes_right]}")
    print(f"   • Для производной 2-го порядка точности: узлы {nodes_order2} → x = {[x_nodes[k] for k in nodes_order2]}")
    print(f"   • Для второй производной: узлы {nodes_d2} → x = {[x_nodes[k] for k in nodes_d2]}")

    print("\n4. Значения первой производной:")
    print(f"   • По формуле 1-го порядка (3.22):           y'(x*) = {d1_simple:.6f}")
    print(f"   • Левосторонняя:                            y'(x*) = {d1_left:.6f}")
    print(f"   • Правосторонняя:                           y'(x*) = {d1_right:.6f}")
    print(f"   • По формуле 2-го порядка точности (3.24):  y'(x*) = {d1_order2:.6f}")

    print("\n5. Значение второй производной (формула 3.25):")
    print(f"   y''(x*) = {d2:.6f}")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(x_nodes, y_nodes, color='red', s=70, zorder=5, label='Узлы таблицы')
    ax.axvline(x=x_star, color='gray', linestyle=':', alpha=0.7, label=f'x* = {x_star}')

    x_min, x_max = min(x_nodes) - 0.2, max(x_nodes) + 0.2
    y_star_approx = y_nodes[nodes_simple[0]] + d1_simple * (x_star - x_nodes[nodes_simple[0]])
    x_line = [x_star - 0.8, x_star + 0.8]
    y_line = [y_star_approx + d1_order2 * (xx - x_star) for xx in x_line]
    ax.plot(x_line, y_line, 'b--', linewidth=1.5, label=f"Касательная (y'≈{d1_order2:.3f})")

    ax.set_title('Численное дифференцирование (Вариант 8)', fontsize=13)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best', fontsize=10)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    plot_path = os.path.join(script_dir, "diff_plot.png")
    fig.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f"\nГрафик сохранен в файл: {plot_path}")


if __name__ == "__main__":
    main()