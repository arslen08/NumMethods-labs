def solve_tridiagonal(a, b, c, d):
    n = len(d)
    c_star = [0.0] * n
    d_star = [0.0] * n
    
    c_star[0] = c[0] / b[0]
    d_star[0] = d[0] / b[0]
    
    for i in range(1, n):
        denom = b[i] - a[i] * c_star[i - 1]
        c_star[i] = c[i] / denom if i < n - 1 else 0.0
        d_star[i] = (d[i] - a[i] * d_star[i - 1]) / denom
        
    x = [0.0] * n
    x[-1] = d_star[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_star[i] - c_star[i] * x[i + 1]
        
    return x


def build_cubic_spline(x_nodes, y_nodes):
    n = len(x_nodes) - 1  
    h = [x_nodes[i+1] - x_nodes[i] for i in range(n)] 

    c = [0.0] * (n + 1)
    
    size = n - 1  
    
    if size >= 1:
        A = [0.0] * size
        B = [0.0] * size
        C = [0.0] * size
        D = [0.0] * size
        
        for i in range(size):
            if i == 0:
                A[i] = 0.0
                B[i] = 2 * (h[0] + h[1])
                C[i] = h[1]
                D[i] = 3 * ((y_nodes[2] - y_nodes[1]) / h[1] - (y_nodes[1] - y_nodes[0]) / h[0])
            elif i == size - 1:
                A[i] = h[n-2]
                B[i] = 2 * (h[n-2] + h[n-1])
                C[i] = 0.0
                D[i] = 3 * ((y_nodes[n] - y_nodes[n-1]) / h[n-1] - (y_nodes[n-1] - y_nodes[n-2]) / h[n-2])
            else:
                A[i] = h[i]
                B[i] = 2 * (h[i] + h[i+1])
                C[i] = h[i+1]
                D[i] = 3 * ((y_nodes[i+2] - y_nodes[i+1]) / h[i+1] - (y_nodes[i+1] - y_nodes[i]) / h[i])
        
        c_mid = solve_tridiagonal(A, B, C, D)
        for k in range(size):
            c[k + 1] = c_mid[k]  
    
    a = [0.0] * n
    b = [0.0] * n
    d = [0.0] * n
    
    for i in range(n):
        a[i] = y_nodes[i]
        b[i] = (y_nodes[i+1] - y_nodes[i]) / h[i] - (h[i] / 3.0) * (2.0 * c[i] + c[i+1])
        d[i] = (c[i+1] - c[i]) / (3.0 * h[i])

    return a, b, c, d


def evaluate_spline(x, x_nodes, a, b, c, d):
    n = len(x_nodes) - 1
    
    interval_idx = 0
    for i in range(n):
        if x_nodes[i] <= x <= x_nodes[i+1]:
            interval_idx = i
            break
            
    if x < x_nodes[0]:
        interval_idx = 0
    if x > x_nodes[-1]:
        interval_idx = n - 1

    dx = x - x_nodes[interval_idx]
    
    S_x = a[interval_idx] + b[interval_idx] * dx + c[interval_idx] * (dx ** 2) + d[interval_idx] * (dx ** 3)
    
    return S_x, interval_idx