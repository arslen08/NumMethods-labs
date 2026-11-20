def select_three_nodes(x_nodes, x_star):
    n = len(x_nodes)
    idx = 0
    for k in range(n):
        if x_nodes[k] <= x_star + 1e-12:
            idx = k

    if idx == 0:
        j = 0
    elif idx >= n - 1:
        j = n - 3
    else:
        j = idx - 1
        if j + 2 >= n:
            j = n - 3
    return j


def first_derivative_order2(x_nodes, y_nodes, x_star):
    j = select_three_nodes(x_nodes, x_star)

    x0, x1, x2 = x_nodes[j], x_nodes[j + 1], x_nodes[j + 2]
    y0, y1, y2 = y_nodes[j], y_nodes[j + 1], y_nodes[j + 2]

    term1 = (y1 - y0) / (x1 - x0)
    term2 = (y2 - y1) / (x2 - x1)
    deriv = term1 + (term2 - term1) * (2 * x_star - x0 - x1) / (x2 - x0)

    return deriv, (j, j + 1, j + 2)


def second_derivative(x_nodes, y_nodes, x_star):
    j = select_three_nodes(x_nodes, x_star)

    x0, x1, x2 = x_nodes[j], x_nodes[j + 1], x_nodes[j + 2]
    y0, y1, y2 = y_nodes[j], y_nodes[j + 1], y_nodes[j + 2]

    term1 = (y1 - y0) / (x1 - x0)
    term2 = (y2 - y1) / (x2 - x1)
    deriv2 = 2.0 * (term2 - term1) / (x2 - x0)

    return deriv2, (j, j + 1, j + 2)