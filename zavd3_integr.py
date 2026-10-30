# -*- coding: utf-8 -*-
"""
Обчислювальна практика. Змістовий модуль 3.
Чисельне інтегрування. Варіант 9:  f(x) = lg(x + 1) · sin(2x + 3).
Методи: формула трапецій, формула Сімпсона (парабол).
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

AUTHOR = "Виконав(ла): ПІБ студента, група ___"
TOPIC = "Змістовий модуль 3. Чисельне інтегрування. Варіант 9"


def f(x):
    return np.log10(x + 1) * np.sin(2 * x + 3)


def trapezoid(a, b, n):
    """Складена формула трапецій: h·[(y0 + yn)/2 + y1 + ... + y(n-1)]."""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h * ((y[0] + y[-1]) / 2 + y[1:-1].sum())


def simpson(a, b, n):
    """Складена формула Сімпсона (n — парне): h/3·[y0 + 4(y1+y3+...) + 2(y2+y4+...) + yn]."""
    if n % 2:
        raise ValueError("Для формули Сімпсона кількість відрізків n має бути парною")
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3 * (y[0] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum() + y[-1])


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Завдання 3. Чисельне інтегрування f(x) = lg(x+1)·sin(2x+3)")
        self.geometry("1100x640")
        hdr = tk.Frame(self, bg="#1f4e79"); hdr.pack(fill="x")
        tk.Label(hdr, text=AUTHOR, fg="white", bg="#1f4e79", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        tk.Label(hdr, text=TOPIC, fg="white", bg="#1f4e79", font=("Arial", 10)).pack(anchor="w", padx=10)
        tk.Label(hdr, text="Задача: обчислити визначений інтеграл від f(x) на [a; b] (a > −1). "
                           "Введіть межі a, b та кількість відрізків n (для Сімпсона — парне).",
                 fg="#dfe9f5", bg="#1f4e79", font=("Arial", 9)).pack(anchor="w", padx=10, pady=(0, 6))
        body = tk.Frame(self); body.pack(fill="both", expand=True, padx=8, pady=6)
        left = tk.Frame(body); left.pack(side="left", fill="both", expand=True)
        ctl = tk.Frame(left); ctl.pack(fill="x")
        self.ea, self.eb, self.en = [tk.Entry(ctl, width=8) for _ in range(3)]
        for lbl, e, v in (("a =", self.ea, "0"), ("b =", self.eb, "1"), ("n =", self.en, "10")):
            tk.Label(ctl, text=lbl).pack(side="left"); e.insert(0, v); e.pack(side="left", padx=(0, 6))
        btn = tk.Frame(left); btn.pack(fill="x", pady=4)
        ttk.Button(btn, text="Формула трапецій", command=lambda: self.run("trap")).pack(side="left", padx=2)
        ttk.Button(btn, text="Формула Сімпсона", command=lambda: self.run("simp")).pack(side="left", padx=2)
        ttk.Button(btn, text="Очистити", command=lambda: self.out.delete("1.0", "end")).pack(side="left", padx=2)
        self.out = tk.Text(left, font=("Courier New", 9), width=64)
        self.out.pack(fill="both", expand=True)
        fig = Figure(figsize=(4.6, 4.2), dpi=90)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=body)
        self.canvas.get_tk_widget().pack(side="right", fill="both")

    def run(self, method):
        try:
            a, b = float(self.ea.get().replace(",", ".")), float(self.eb.get().replace(",", "."))
            n = int(self.en.get())
            if a <= -1 or b <= -1:
                raise ValueError("Функція lg(x+1) визначена лише при x > −1")
            if n < 1 or a >= b:
                raise ValueError("Потрібно a < b та n ≥ 1")
            rule = trapezoid if method == "trap" else simpson
            name = "трапецій" if method == "trap" else "Сімпсона"
            I_n, I_2n = rule(a, b, n), rule(a, b, 2 * n)
        except Exception as ex:
            messagebox.showerror("Помилка", str(ex)); return
        p = 2 if method == "trap" else 4
        runge = abs(I_2n - I_n) / (2 ** p - 1)          # оцінка похибки за правилом Рунге
        self.out.insert("end", "=== Формула %s, [%g; %g] ===\n" % (name, a, b))
        self.out.insert("end", "I(n=%d)  = %.8f\nI(n=%d) = %.8f\n" % (n, I_n, 2 * n, I_2n))
        self.out.insert("end", "Оцінка похибки (правило Рунге) ≈ %.2e\n\n" % runge)
        xs = np.linspace(a, b, 300)
        xn = np.linspace(a, b, n + 1)
        self.ax.clear(); self.ax.axhline(0, color="gray", lw=0.8)
        self.ax.fill_between(xs, f(xs), alpha=0.25, color="#1f77b4")
        self.ax.plot(xs, f(xs), color="#1f77b4", label="f(x) = lg(x+1)·sin(2x+3)")
        self.ax.plot(xn, f(xn), "o-" if method == "trap" else "o", ms=3, color="#d62728", lw=0.8, label="вузли, n=%d" % n)
        self.ax.grid(alpha=0.3); self.ax.legend(fontsize=8); self.canvas.draw()


if __name__ == "__main__":
    app = App()
    import os
    if os.environ.get("SNAP"):
        app.after(300, lambda: app.run("trap")); app.after(400, lambda: app.run("simp"))
    app.mainloop()
