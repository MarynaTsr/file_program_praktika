# -*- coding: utf-8 -*-
"""
Обчислювальна практика. Змістовий модуль 4.
Задача Коші для ЗДР. Варіант 9:  y' = x + sin(y/5),  y(1,8) = 2,6,  x ∈ [1,8; 2,8].
Методи: Ейлера, Рунге–Кутта 4-го порядку.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

AUTHOR = "Виконав(ла): ПІБ студента, група ___"
TOPIC = "Змістовий модуль 4. Задача Коші для ЗДР. Варіант 9"


def F(x, y):
    return x + np.sin(y / 5)


def euler(x0, y0, xn, h):
    n = int(round((xn - x0) / h))
    x = x0 + h * np.arange(n + 1)
    y = np.empty(n + 1); y[0] = y0
    for k in range(n):
        y[k + 1] = y[k] + h * F(x[k], y[k])
    return x, y


def runge_kutta4(x0, y0, xn, h):
    n = int(round((xn - x0) / h))
    x = x0 + h * np.arange(n + 1)
    y = np.empty(n + 1); y[0] = y0
    for k in range(n):
        k1 = F(x[k], y[k])
        k2 = F(x[k] + h / 2, y[k] + h * k1 / 2)
        k3 = F(x[k] + h / 2, y[k] + h * k2 / 2)
        k4 = F(x[k] + h, y[k] + h * k3)
        y[k + 1] = y[k] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x, y


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Завдання 4. Задача Коші y' = x + sin(y/5)")
        self.geometry("1100x660")
        hdr = tk.Frame(self, bg="#1f4e79"); hdr.pack(fill="x")
        tk.Label(hdr, text=AUTHOR, fg="white", bg="#1f4e79", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        tk.Label(hdr, text=TOPIC, fg="white", bg="#1f4e79", font=("Arial", 10)).pack(anchor="w", padx=10)
        tk.Label(hdr, text="Задача: знайти наближений розв'язок y(x) задачі Коші y' = x + sin(y/5), y(x0) = y0 на [x0; xn] з кроком h.",
                 fg="#dfe9f5", bg="#1f4e79", font=("Arial", 9)).pack(anchor="w", padx=10, pady=(0, 6))
        body = tk.Frame(self); body.pack(fill="both", expand=True, padx=8, pady=6)
        left = tk.Frame(body); left.pack(side="left", fill="both", expand=True)
        ctl = tk.Frame(left); ctl.pack(fill="x")
        self.ent = {}
        for lbl, v in (("x0", "1.8"), ("y0", "2.6"), ("xn", "2.8"), ("h", "0.1")):
            tk.Label(ctl, text=lbl + " =").pack(side="left")
            e = tk.Entry(ctl, width=7); e.insert(0, v); e.pack(side="left", padx=(0, 6)); self.ent[lbl] = e
        btn = tk.Frame(left); btn.pack(fill="x", pady=4)
        ttk.Button(btn, text="Обчислити (Ейлер і Рунге–Кутта)", command=self.run).pack(side="left", padx=2)
        ttk.Button(btn, text="Очистити", command=lambda: self.out.delete("1.0", "end")).pack(side="left", padx=2)
        self.out = tk.Text(left, font=("Courier New", 9), width=64)
        self.out.pack(fill="both", expand=True)
        fig = Figure(figsize=(4.6, 4.2), dpi=90)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=body)
        self.canvas.get_tk_widget().pack(side="right", fill="both")

    def run(self):
        try:
            x0, y0, xn, h = [float(self.ent[k].get().replace(",", ".")) for k in ("x0", "y0", "xn", "h")]
            if h <= 0 or xn <= x0:
                raise ValueError("Потрібно h > 0 та xn > x0")
            xe, ye = euler(x0, y0, xn, h)
            xr, yr = runge_kutta4(x0, y0, xn, h)
        except Exception as ex:
            messagebox.showerror("Помилка", str(ex)); return
        self.out.insert("end", "h = %g\n%4s %8s %12s %12s %10s\n" % (h, "k", "x_k", "Ейлер", "Рунге–Кутта", "|різниця|"))
        for k in range(len(xe)):
            self.out.insert("end", "%4d %8.3f %12.6f %12.6f %10.2e\n" % (k, xe[k], ye[k], yr[k], abs(ye[k] - yr[k])))
        self.out.insert("end", "\n")
        self.ax.clear()
        self.ax.plot(xe, ye, "s--", ms=3, label="Ейлер")
        self.ax.plot(xr, yr, "o-", ms=3, label="Рунге–Кутта 4")
        self.ax.set_xlabel("x"); self.ax.set_ylabel("y")
        self.ax.grid(alpha=0.3); self.ax.legend(fontsize=8); self.canvas.draw()


if __name__ == "__main__":
    app = App()
    import os
    if os.environ.get("SNAP"):
        app.after(300, app.run)
    app.mainloop()
