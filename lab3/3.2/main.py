import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from methods import build_cubic_spline, evaluate_spline

def main():
    x_nodes = [-0.4, -0.1, 0.2, 0.5, 0.8]
    y_nodes = [-0.41152, -0.10017, 0.20136, 0.52360, 0.92730]
    x_star = 0.1
    
    exact_val = math.asin(x_star)

    a, b, c, d = build_cubic_spline(x_nodes, y_nodes)

    print("ЗАДАЧА 3.2: КУБИЧЕСКИЙ СПЛАЙН (ВАРИАНТ 8)")
    print("=" * 60)

    print("\n1. Исходные узлы и табличные значения функции:")
    print(f"   {'i':<3} | {'x_i':<8} | {'f(x_i)':<10}")
    print("   " + "-" * 26)
    for i in range(len(x_nodes)):
        print(f"   {i:<3} | {x_nodes[i]:<8.2f} | {y_nodes[i]:<10.5f}")

    print("\n2. Коэффициенты сплайна S_i(x) = a_i + b_i(x - x_{i-1}) + c_i(x - x_{i-1})^2 + d_i(x - x_{i-1})^3:")
    print(f"   {'Интервал':<12} | {'a_i':<10} | {'b_i':<10} | {'c_i':<10} | {'d_i':<10}")
    print("   " + "-" * 62)
    for i in range(len(a)):
        print(f"   [{x_nodes[i]:4.1f}, {x_nodes[i+1]:4.1f}] | {a[i]:>10.5f} | {b[i]:>10.5f} | {c[i]:>10.5f} | {d[i]:>10.5f}")

    S_star, interval_idx = evaluate_spline(x_star, x_nodes, a, b, c, d)

    print(f"\n3. Результаты вычислений в точке x* = {x_star}:")
    print(f"   • Значение сплайна S(x*):         {S_star:.6f}")
    print(f"   • Номер интервала (с 0):          {interval_idx} (отрезок [{x_nodes[interval_idx]}; {x_nodes[interval_idx+1]}])")
    

    print("\n4. Проверка прохождения сплайна через исходные узлы:")
    max_node_error = 0.0
    for i in range(len(x_nodes)):
        val, _ = evaluate_spline(x_nodes[i], x_nodes, a, b, c, d)
        err = abs(val - y_nodes[i])
        max_node_error = max(max_node_error, err)
        print(f"   S({x_nodes[i]:5.2f}) = {val:.5f} | f({x_nodes[i]:5.2f}) = {y_nodes[i]:.5f} | Разница: {err:.2e}")

    print("\n5. Проверка нулевой кривизны на концах (граничные условия):")
    S_double_left = 2 * c[0]
    dx_right = x_nodes[-1] - x_nodes[-2]
    S_double_right = 2 * c[-1] + 6 * d[-1] * dx_right
    
    print(f"   • S''(x_0) = {S_double_left:.2e} (должно быть 0)")
    print(f"   • S''(x_n) = {S_double_right:.2e} (должно быть 0)")

    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(len(a)):
        x_interval = []
        y_interval = []
        num_pts = 50
        step = (x_nodes[i+1] - x_nodes[i]) / (num_pts - 1)
        for k in range(num_pts):
            xx = x_nodes[i] + k * step
            x_interval.append(xx)
            y_val, _ = evaluate_spline(xx, x_nodes, a, b, c, d)
            y_interval.append(y_val)
        
        label = "Кубический сплайн" if i == 0 else ""
        ax.plot(x_interval, y_interval, 'b-', linewidth=2, label=label)

    ax.scatter(x_nodes, y_nodes, color='red', s=60, zorder=5, label='Табличные узлы')
    ax.scatter([x_star], [S_star], color='green', marker='*', s=200, zorder=6, 
               label=f'x* = {x_star} (S = {S_star:.5f})')

    ax.set_title('Кубический сплайн (Вариант 8, табличные данные)', fontsize=13)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best', fontsize=11)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    plot_path = os.path.join(script_dir, "cubic_spline_plot.png")
    
    fig.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"\nГрафик успешно сохранен в файл: {plot_path}")


if __name__ == "__main__":
    main()