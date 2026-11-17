def get_norm(v):
    return max(abs(x) for x in v)


def vector_sub(v1, v2):
    return [x - y for x, y in zip(v1, v2)]


def simple_iteration_method(alpha, beta, eps):
    n = len(beta)
    x = beta.copy()
    k = 0

    while True:
        k += 1
        x_new = [0.0] * n

        for i in range(n):
            s = sum(alpha[i][j] * x[j] for j in range(n))
            x_new[i] = s + beta[i]

        diff = vector_sub(x_new, x)
        err = get_norm(diff)

        if err < eps:
            return x_new, k

        x = x_new


def seidel_method(alpha, beta, eps):
    n = len(beta)
    x = beta.copy() 
    k = 0

    while True:
        k += 1
        x_new = x.copy()

        for i in range(n):
            s = sum(alpha[i][j] * x_new[j] for j in range(n))
            x_new[i] = s + beta[i]

        diff = vector_sub(x_new, x)
        err = get_norm(diff)

        if err < eps:
            return x_new, k

        x = x_new