import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from methods import *

A, B = 0.8, 1.0


def fixed_steps(step, x0, n):
    xs = [x0]
    for _ in range(n):
        xs.append(step(xs[-1]))
    return xs


def main():
    eps = float(input("Точность eps: "))

    q = max_abs(dphi, A, B)
    x0_si = (A + B) / 2
    x0_nw = newton_start(A, B)

    root_si, hist_si = simple_iteration(x0_si, eps, q)
    root_nw, hist_nw = newton(x0_nw, eps)
    root_ref, _ = newton(x0_nw, 1e-15)

    print(f"q = max|phi'| на [{A}; {B}] = {q:.6f}")
    print(f"Метод простой итерации: x = {root_si:.10f}, итераций: {len(hist_si) - 1}")
    print(f"Метод Ньютона:          x = {root_nw:.10f}, итераций: {len(hist_nw) - 1}")

    print("\n k | |x_k - x*| (прост. итер.) | |x_k - x*| (Ньютон)")
    for k in range(max(len(hist_si), len(hist_nw))):
        e1 = f"{abs(hist_si[k] - root_ref):.3e}" if k < len(hist_si) else "-"
        e2 = f"{abs(hist_nw[k] - root_ref):.3e}" if k < len(hist_nw) else "-"
        print(f"{k:2d} | {e1:>25} | {e2:>20}")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    nw_draw = fixed_steps(lambda x: x - f(x) / df(x), x0_nw, 3)
    lo, hi = 0.86, 1.02
    xs = [lo + (hi - lo) * i / 300 for i in range(301)]
    ax1.plot(xs, [f(x) for x in xs], "b-", lw=2, label="f(x) = ln(x+1) − 2x² + 1")
    ax1.axhline(0, color="k", lw=0.8)
    
    for i in range(3):
        xk, xn = nw_draw[i], nw_draw[i + 1]
        ax1.plot([xk, xk], [0, f(xk)], "k:", lw=1)
        ax1.plot([xk, xn], [f(xk), 0], "r--", lw=1.5)
        ax1.plot(xk, f(xk), "ro", ms=5)
        ax1.annotate(f"x{i}", (xk, f(xk)), textcoords="offset points",
                     xytext=(6, -12), color="red", fontweight="bold")
        
    ax1.axvline(root_ref, color="g", lw=1, label=f"x* ≈ {root_ref:.6f}")
    ax1.set_title("Метод Ньютона: касательные")
    ax1.set_xlabel("x"); ax1.set_ylabel("f(x)")
    ax1.set_xlim(lo, hi); ax1.set_ylim(-0.4, 0.15)
    ax1.grid(True); ax1.legend(loc="lower left")

    si_draw = fixed_steps(phi, A, 5)
    lo, hi = 0.78, 0.95
    xs = [lo + (hi - lo) * i / 200 for i in range(201)]
    
    ax2.plot([lo, hi], [lo, hi], "k-", lw=1.5, label="y = x")
    ax2.plot(xs, [phi(x) for x in xs], "g-", lw=2, label="y = φ(x)")
    
    for i in range(5):
        xk, xn = si_draw[i], si_draw[i + 1]
        ax2.plot([xk, xk], [xk, xn], "b-", lw=1.5)
        ax2.plot([xk, xn], [xn, xn], "b-", lw=1.5)
        ax2.plot(xk, xn, "bo", ms=4)
        
    ax2.annotate("x0", (si_draw[0], si_draw[0]), textcoords="offset points",
                 xytext=(-5, -15), color="blue", fontweight="bold")
    ax2.set_title("Простая итерация: лестница (старт x0 = A)")
    ax2.set_xlabel("x"); ax2.set_ylabel("y")
    ax2.set_xlim(lo, hi); ax2.set_ylim(lo, hi)
    ax2.grid(True); ax2.legend(loc="upper left")

    epss = [10 ** (-k) for k in range(1, 13)]
    it_si = [len(simple_iteration(x0_si, e, q)[1]) - 1 for e in epss]
    it_nw = [len(newton(x0_nw, e)[1]) - 1 for e in epss]
    
    ax3.semilogx(epss, it_si, "o-", label="Простая итерация")
    ax3.semilogx(epss, it_nw, "s-", label="Ньютон")
    ax3.invert_xaxis()
    ax3.set_title("Число итераций от заданной точности")
    ax3.set_xlabel("eps"); ax3.set_ylabel("число итераций")
    ax3.grid(True, which="both"); ax3.legend()

    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs.png")
    fig.savefig(out, dpi=150)
    print(f"\nГрафики сохранены в {out}")


if __name__ == "__main__":
    main()