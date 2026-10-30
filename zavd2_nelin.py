# -*- coding: utf-8 -*-
"""
Обчислювальна практика. Змістовий модуль 2.
Розв'язування нелінійних рівнянь. Варіант 9:  x^2 - 4 sin x = 1.
Методи: половинного ділення (бісекцій), Ньютона (дотичних).
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

AUTHOR = "Виконав(ла): ПІБ студента, група ___"
TOPIC = "Змістовий модуль 2. Розв'язування нелінійних рівнянь. Варіант 9"


def f(x):
    return x ** 2 - 4 * np.sin(x) - 1


def df(x):                      # перша похідна
    return 2 * x - 4 * np.cos(x)


def d2f(x):                     # друга похідна
    return 2 + 4 * np.sin(x)


def bisection(a, b, eps):
    if f(a) * f(b) > 0:
        raise ValueError("На кінцях відрізка f(x) має однакові знаки — кореня не відокремлено")
    rows = []
    k = 0
    while abs(b - a) > eps:
        c = (a + b) / 2
        rows.append((k, a, b, c, f(c)))
        if f(c) == 0:
            return c, k + 1, rows
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        k += 1
    return (a + b) / 2, k, rows


def newton(a, b, eps, max_iter=100):
    if f(a) * f(b) > 0:
        raise ValueError("На кінцях відрізка f(x) має однакові знаки")
    # початкове наближення — той кінець, де f(x)·f''(x) > 0 (умова Фур'є)
    x = a if f(a) * d2f(a) > 0 else b
    rows = []
    for k in range(1, max_iter + 1):
        x_new = x - f(x) / df(x)
        rows.append((k, x, f(x), df(x), x_new))
        if abs(x_new - x) < eps:
            return x_new, k, rows
        x = x_new
    raise RuntimeError("Метод Ньютона не збігся")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Завдання 2. Нелінійне рівняння x² − 4·sin x = 1")
        self.geometry("1100x660")
        hdr = tk.Frame(self, bg="#1f4e79"); hdr.pack(fill="x")
        tk.Label(hdr, text=AUTHOR, fg="white", bg="#1f4e79", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        tk.Label(hdr, text=TOPIC, fg="white", bg="#1f4e79", font=("Arial", 10)).pack(anchor="w", padx=10)
        tk.Label(hdr, text="Задача: уточнити корінь рівняння x² − 4·sin x − 1 = 0 на відрізку [a; b] з точністю ε. "
                           "Введіть a, b, ε і натисніть кнопку методу.",
                 fg="#dfe9f5", bg="#1f4e79", font=("Arial", 9)).pack(anchor="w", padx=10, pady=(0, 6))
        body = tk.Frame(self); body.pack(fill="both", expand=True, padx=8, pady=6)
        left = tk.Frame(body); left.pack(side="left", fill="both", expand=True)
        ctl = tk.Frame(left); ctl.pack(fill="x")
        self.ea, self.eb, self.ee = [tk.Entry(ctl, width=8) for _ in range(3)]
        for lbl, e, v in (("a =", self.ea, "2"), ("b =", self.eb, "2.5"), ("ε =", self.ee, "0.0001")):
            tk.Label(ctl, text=lbl).pack(side="left"); e.insert(0, v); e.pack(side="left", padx=(0, 6))
        btn = tk.Frame(left); btn.pack(fill="x", pady=4)
        ttk.Button(btn, text="Метод бісекцій", command=self.run_bis).pack(side="left", padx=2)
        ttk.Button(btn, text="Метод Ньютона", command=self.run_newton).pack(side="left", padx=2)
        ttk.Button(btn, text="Очистити", command=lambda: self.out.delete("1.0", "end")).pack(side="left", padx=2)
        self.out = tk.Text(left, font=("Courier New", 9), width=66)
        self.out.pack(fill="both", expand=True)
        fig = Figure(figsize=(4.6, 4.2), dpi=90)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=body)
        self.canvas.get_tk_widget().pack(side="right", fill="both")
        self.plot()

    def params(self):
        return [float(e.get().replace(",", ".")) for e in (self.ea, self.eb, self.ee)]

    def plot(self, root=None):
        xs = np.linspace(-2, 3.5, 400)
        self.ax.clear(); self.ax.axhline(0, color="gray", lw=0.8)
        self.ax.plot(xs, f(xs), color="#1f77b4", label="f(x) = x² − 4sin x − 1")
        if root is not None:
            self.ax.plot(root, 0, "o", color="#d62728", label="x* = %.5f" % root)
        self.ax.grid(alpha=0.3); self.ax.legend(fontsize=8); self.canvas.draw()

    def run_bis(self):
        try:
            a, b, eps = self.params(); x, k, rows = bisection(a, b, eps)
        except Exception as ex:
            messagebox.showerror("Помилка", str(ex)); return
        self.out.insert("end", "=== Метод бісекцій на [%g; %g], ε=%g ===\n" % (a, b, eps))
        self.out.insert("end", "%3s %10s %10s %10s %11s\n" % ("k", "a", "b", "c", "f(c)"))
        for r in rows:
            self.out.insert("end", "%3d %10.6f %10.6f %10.6f %11.2e\n" % r)
        self.out.insert("end", "Корінь x* = %.6f, ітерацій: %d, f(x*) = %.2e\n\n" % (x, k, f(x)))
        self.plot(x)

    def run_newton(self):
        try:
            a, b, eps = self.params(); x, k, rows = newton(a, b, eps)
        except Exception as ex:
            messagebox.showerror("Помилка", str(ex)); return
        self.out.insert("end", "=== Метод Ньютона на [%g; %g], ε=%g ===\n" % (a, b, eps))
        self.out.insert("end", "%3s %10s %11s %10s %10s\n" % ("k", "x_k", "f(x_k)", "f'(x_k)", "x_k+1"))
        for r in rows:
            self.out.insert("end", "%3d %10.6f %11.2e %10.5f %10.6f\n" % r)
        self.out.insert("end", "Корінь x* = %.6f, ітерацій: %d, f(x*) = %.2e\n\n" % (x, k, f(x)))
        self.plot(x)


if __name__ == "__main__":
    app = App()
    import os
    if os.environ.get("SNAP"):
        app.after(300, app.run_bis); app.after(400, app.run_newton)
    app.mainloop()
