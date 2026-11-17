import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from methods import *

X0 = [2.5, 1.7]
D1, D2 = (2.3, 2.7), (1.5, 1.9)


def fixed_steps(step, x0, n):
    xs = [list(x0)]
    for _ in range(n):
        xs.append(step(xs[-1]))
    return xs


def newton_step(x):
    dx = solve_2x2(jacobian(x), [-v for v in F(x)])
    return [x[0] + dx[0], x[1] + dx[1]]


def curves(ax, x1_lim, x2_lim, n=600):
    a = A
    t = [2 * math.pi * i / n for i in range(n + 1)]
    ax.plot([a * math.cos(v) for v in t], [a * math.sin(v) for v in t],
            color="tab:blue", label="x1² + x2² = a²")
    lo, hi = x2_lim
    x2s = [lo + (hi - lo) * i / n for i in range(n + 1)]
    ax.plot([math.exp(v) - a for v in x2s], x2s,
            color="tab:orange", label="x1 = exp(x2) − a")


def main():
    eps = float(input("Точность eps: "))

    q = max_dphi_norm(D1, D2)
    root_si, hist_si = simple_iteration(X0, eps, q)
    root_nw, hist_nw = newton(X0, eps)

    exact = fixed_steps(newton_step, X0, 20)[-1]

    print(f"q = max||phi'|| на D = {q:.6f}")
    print(f"Метод простой итерации: x1 = {root_si[0]:.10f}, x2 = {root_si[1]:.10f}, "
          f"итераций: {len(hist_si) - 1}")
    print(f"Метод Ньютона:          x1 = {root_nw[0]:.10f}, x2 = {root_nw[1]:.10f}, "
          f"итераций: {len(hist_nw) - 1}")

    print("\n k | ||x_k - x*|| (прост. итер.) | ||x_k - x*|| (Ньютон)")
    for k in range(max(len(hist_si), len(hist_nw))):
        e1 = f"{norm([hist_si[k][0] - exact[0], hist_si[k][1] - exact[1]]):.3e}" if k < len(hist_si) else "-"
        e2 = f"{norm([hist_nw[k][0] - exact[0], hist_nw[k][1] - exact[1]]):.3e}" if k < len(hist_nw) else "-"
        print(f"{k:2d} | {e1:>27} | {e2:>22}")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    curves(ax1, (-4, 4), (-3.5, 3.0))
    ax1.add_patch(plt.Rectangle((D1[0], D2[0]), D1[1] - D1[0], D2[1] - D2[0],
                                fill=False, ec="k", ls="--", lw=1.2,
                                label="область D"))
    ax1.plot(*X0, "ro", ms=6, label=f"x⁰ = {tuple(X0)}")
    ax1.plot(*exact, "g*", ms=12, label="корень x*")
    ax1.set_title("Графическая локализация корня")
    ax1.set_xlabel("x1"); ax1.set_ylabel("x2")
    ax1.set_xlim(-4, 4.5); ax1.set_ylim(-4, 4)
    ax1.set_aspect("equal")
    ax1.grid(True); ax1.legend(loc="lower right", fontsize=8)

    w = 0.04
    win1 = (exact[0] - w, X0[0] + 0.01)
    win2 = (exact[1] - w, exact[1] + w)
    curves(ax2, win1, win2)
    si_pts = fixed_steps(phi, X0, 5)
    nw_pts = fixed_steps(newton_step, X0, 3)
    ax2.plot([p[0] for p in si_pts], [p[1] for p in si_pts], "bo-", ms=5, lw=1,
             alpha=0.8, label="простая итерация")
    ax2.plot([p[0] for p in nw_pts], [p[1] for p in nw_pts], "rs--", ms=6, lw=1,
             alpha=0.8, label="Ньютон")
    ax2.plot(*X0, "k^", ms=9, label="x⁰")
    ax2.plot(*exact, "g*", ms=14, label="x*")
    ax2.set_title("Приближения вблизи корня (увеличено)")
    ax2.set_xlabel("x1"); ax2.set_ylabel("x2")
    ax2.set_xlim(*win1); ax2.set_ylim(*win2)
    ax2.grid(True); ax2.legend(loc="upper left", fontsize=8)

    epss = [10 ** (-k) for k in range(1, 13)]
    it_si = [len(simple_iteration(X0, e, q)[1]) - 1 for e in epss]
    it_nw = [len(newton(X0, e)[1]) - 1 for e in epss]
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