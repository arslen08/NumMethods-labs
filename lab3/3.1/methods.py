import math


def get_nodes_and_values(x_nodes):
    return [math.asin(x) for x in x_nodes]


def lagrange_basis(x, i, nodes):
    l_i = 1.0
    for j in range(len(nodes)):
        if j != i:
            l_i *= (x - nodes[j]) / (nodes[i] - nodes[j])
    return l_i


def lagrange_poly(x, nodes, values):
    L_x = 0.0
    for i in range(len(nodes)):
        L_x += values[i] * lagrange_basis(x, i, nodes)
    return L_x


def format_lagrange_poly(nodes, values):
    n = len(nodes) - 1
    terms = []
    for i in range(len(nodes)):
        denom = 1.0
        diff_terms = []
        for j in range(len(nodes)):
            if j != i:
                denom *= (nodes[i] - nodes[j])
                diff_terms.append(f"(x - ({nodes[j]}))")
        coef = values[i] / denom
        terms.append(f"{coef:+.6f} * " + " * ".join(diff_terms))
    return f"L_{n}(x) =\n  " + "\n  ".join(terms)


def divided_differences_table(nodes, values):
    n = len(nodes)
    table = [[0.0] * n for _ in range(n)]

    for i in range(n):
        table[i][0] = values[i]

    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (nodes[i + j] - nodes[i])

    return table


def newton_poly(x, nodes, dd_table):
    n = len(nodes)
    N_x = dd_table[0][0]
    product_term = 1.0

    for k in range(1, n):
        product_term *= (x - nodes[k - 1])
        N_x += dd_table[0][k] * product_term

    return N_x


def format_newton_poly(nodes, dd_table):
    n = len(nodes) - 1
    terms = [f"{dd_table[0][0]:.6f}"]
    product_str = ""
    for k in range(1, len(nodes)):
        product_str += f"(x - ({nodes[k - 1]}))"
        coef = dd_table[0][k]
        terms.append(f"{coef:+.6f} * {product_str}")
    return f"N_{n}(x) = " + " ".join(terms)