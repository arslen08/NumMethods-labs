import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from methods import solve_mnk, evaluate_poly, compute_mse, poly_to_string


def main():
    x_nodes = [-0.7, -0.4, -0.1, 0.2, 0.5, 0.8]
    y_nodes = [-0.7754, -0.41152, -0.10017, 0.20136, 0.5236, 0.9273]

    coeffs1 = solve_mnk(x_nodes, y_nodes, degree=1)
    coeffs2 = solve_mnk(x_nodes, y_nodes, degree=2)
    coeffs3 = solve_mnk(x_nodes, y_nodes, degree=3)

    mse1 = compute_mse(x_nodes, y_nodes, coeffs1)
    mse2 = compute_mse(x_nodes, y_nodes, coeffs2)
    mse3 = compute_mse(x_nodes, y_nodes, coeffs3)

    print("ЗАДАЧА 3.3: МЕТОД НАИМЕНЬШИХ КВАДРАТОВ")

    print("\n1. Исходные узлы и значения функции:")
    print(f"   {'i':<3} | {'x_i':<8} | {'y_i':<10}")
    print("   " + "-" * 26)
    for i in range(len(x_nodes)):
        print(f"   {i:<3} | {x_nodes[i]:<8.1f} | {y_nodes[i]:<10.5f}")

    print("\n2. Коэффициенты многочленов:")
    print("\n   Многочлен 1-й степени P1(x) = a0 + a1*x:")
    print(f"   a0 = {coeffs1[0]:.6f}")
    print(f"   a1 = {coeffs1[1]:.6f}")

    print("\n   Многочлен 2-й степени P2(x) = a0 + a1*x + a2*x^2:")
    print(f"   a0 = {coeffs2[0]:.6f}")
    print(f"   a1 = {coeffs2[1]:.6f}")
    print(f"   a2 = {coeffs2[2]:.6f}")

    print("\n   Многочлен 3-й степени P3(x) = a0 + a1*x + a2*x^2 + a3*x^3:")
    print(f"   a0 = {coeffs3[0]:.6f}")
    print(f"   a1 = {coeffs3[1]:.6f}")
    print(f"   a2 = {coeffs3[2]:.6f}")
    print(f"   a3 = {coeffs3[3]:.6f}")

    print("\n3. Многочлены в явном виде:")
    print(f"   {poly_to_string(coeffs1, 'P1')}")
    print(f"   {poly_to_string(coeffs2, 'P2')}")
    print(f"   {poly_to_string(coeffs3, 'P3')}")

    print("\n4. Суммы квадратов ошибок (Φ / MSE):")
    print(f"   MSE1 (степень 1) = {mse1:.6e}")
    print(f"   MSE2 (степень 2) = {mse2:.6e}")
    print(f"   MSE3 (степень 3) = {mse3:.6e}")

    errors = [(1, mse1), (2, mse2), (3, mse3)]
    best_deg, best_mse = min(errors, key=lambda t: t[1])
    print(f"\n5. Сравнение:")
    print(f"   Наименьшая сумма квадратов ошибок у многочлена степени {best_deg}")
    print(f"   (MSE = {best_mse:.6e}). Он лучше приближает исходные данные.")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(x_nodes, y_nodes, color='red', s=70, zorder=5, label='Исходные узлы')

    x_min = min(x_nodes) - 0.1
    x_max = max(x_nodes) + 0.1
    num_pts = 300
    step = (x_max - x_min) / (num_pts - 1)
    x_plot = [x_min + i * step for i in range(num_pts)]

    y1 = [evaluate_poly(coeffs1, xx) for xx in x_plot]
    y2 = [evaluate_poly(coeffs2, xx) for xx in x_plot]
    y3 = [evaluate_poly(coeffs3, xx) for xx in x_plot]

    ax.plot(x_plot, y1, 'b-', linewidth=2, label=f'P1(x) (MSE={mse1:.2e})')
    ax.plot(x_plot, y2, 'g--', linewidth=2, label=f'P2(x) (MSE={mse2:.2e})')
    ax.plot(x_plot, y3, 'm-.', linewidth=2, label=f'P3(x) (MSE={mse3:.2e})')

    ax.set_title('Метод наименьших квадратов (Вариант 8)\nПриближающие многочлены 1-й, 2-й и 3-й степени', fontsize=12)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best', fontsize=10)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    plot_path = os.path.join(script_dir, "mnk_plot.png")
    fig.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f"\nГрафик успешно сохранен в файл: {plot_path}")


if __name__ == "__main__":
    main()