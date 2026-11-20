from methods import (
    first_derivative_order2,
    second_derivative,
)


def format_nodes(indices, x_nodes, y_nodes):
    """Вспомогательная функция для красивого вывода пар (x, y) по индексам."""
    pairs = [f"({x_nodes[k]:.1f}, {y_nodes[k]:.5f})" for k in indices]
    return "[" + ", ".join(pairs) + "]"


def main():
    x_star = 1.0
    x_nodes = [-1.0, 0.0, 1.0, 2.0, 3.0]
    y_nodes = [-0.7854, 0.0, 0.78540, 1.1071, 1.249]

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
    print(f"   {format_nodes(nodes_order2, x_nodes, y_nodes)}")

    print("\n4. Значение первой производной:")
    print(f"   y'(x*) = {d1_order2:.6f}")

    print("\n5. Значение второй производной:")
    print(f"   y''(x*) = {d2:.6f}")


if __name__ == "__main__":
    main()