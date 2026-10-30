# -*- coding: utf-8 -*-
"""
Обчислювальна практика. Математичне моделювання.
Задача 1: як далеко видно з літака горизонт  l = sqrt((2R + h)·h).
Задача 2: площа кільця, утвореного двома концентричними колами  S = π(R1² − R2²).
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

AUTHOR = "Виконав(ла): ПІБ студента, група ___"
TOPIC = "Побудова математичних моделей задач"
R_EARTH = 6400.0   # радіус Землі, км


def horizon(h, R=R_EARTH):
    """Відстань до горизонту l (км) для висоти h (км)."""
    h = np.asarray(h, dtype=float)
    if np.any(h <= 0):
        raise ValueError("Висота h має бути додатною (h > 0)")
    return np.sqrt((2 * R + h) * h)


def ring_area(R1, R2):
    """Площа кільця між колами радіусів R1 > R2 > 0."""
    if not (0 < R2 < R1):
        raise ValueError("Має виконуватися умова 0 < R2 < R1")
    return np.pi * R1 ** 2 - np.pi * R2 ** 2


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Математичні моделі: горизонт з літака, площа кільця")
        self.geometry("760x560")
        hdr = tk.Frame(self, bg="#1f4e79"); hdr.pack(fill="x")
        tk.Label(hdr, text=AUTHOR, fg="white", bg="#1f4e79", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        tk.Label(hdr, text=TOPIC, fg="white", bg="#1f4e79", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(0, 6))
        nb = ttk.Notebook(self); nb.pack(fill="both", expand=True, padx=8, pady=8)

        t1 = tk.Frame(nb); nb.add(t1, text="Задача 1. Горизонт")
        tk.Label(t1, text="l = √((2R + h)·h),  R = 6400 км. Введіть висоту польоту h (км):").pack(anchor="w", pady=4)
        row = tk.Frame(t1); row.pack(anchor="w")
        self.h = tk.Entry(row, width=10); self.h.insert(0, "10"); self.h.pack(side="left")
        ttk.Button(row, text="Обчислити", command=self.run1).pack(side="left", padx=6)
        self.out1 = tk.Text(t1, font=("Courier New", 10), height=18); self.out1.pack(fill="both", expand=True, pady=4)

        t2 = tk.Frame(nb); nb.add(t2, text="Задача 2. Площа кільця")
        tk.Label(t2, text="S = πR1² − πR2²,  0 < R2 < R1. Введіть радіуси:").pack(anchor="w", pady=4)
        row = tk.Frame(t2); row.pack(anchor="w")
        tk.Label(row, text="R1 =").pack(side="left"); self.r1 = tk.Entry(row, width=8); self.r1.insert(0, "5"); self.r1.pack(side="left")
        tk.Label(row, text="R2 =").pack(side="left"); self.r2 = tk.Entry(row, width=8); self.r2.insert(0, "3"); self.r2.pack(side="left")
        ttk.Button(row, text="Обчислити", command=self.run2).pack(side="left", padx=6)
        self.out2 = tk.Text(t2, font=("Courier New", 10), height=18); self.out2.pack(fill="both", expand=True, pady=4)
        self.nb = nb

    def run1(self):
        try:
            h = float(self.h.get().replace(",", ".")); l = horizon(h)
        except Exception as ex:
            messagebox.showerror("Помилка", str(ex)); return
        self.out1.insert("end", "h = %g км  ->  l = %.2f км\n\nТаблиця l(h):\n%10s %12s\n" % (h, l, "h, км", "l, км"))
        for hh in (0.002, 0.1, 1, 3, 5, 10, 12):
            self.out1.insert("end", "%10g %12.2f\n" % (hh, horizon(hh)))
        self.out1.insert("end", "\n")

    def run2(self):
        try:
            R1 = float(self.r1.get().replace(",", ".")); R2 = float(self.r2.get().replace(",", "."))
            S = ring_area(R1, R2)
        except Exception as ex:
            messagebox.showerror("Помилка", str(ex)); return
        self.out2.insert("end", "S1 = π·%g² = %.4f\nS2 = π·%g² = %.4f\nS = S1 − S2 = %.4f\n\n"
                         % (R1, np.pi * R1 ** 2, R2, np.pi * R2 ** 2, S))


if __name__ == "__main__":
    app = App()
    import os
    if os.environ.get("SNAP") == "1":
        app.after(300, app.run1)
    elif os.environ.get("SNAP") == "2":
        app.after(200, lambda: app.nb.select(1)); app.after(300, app.run2)
    app.mainloop()
