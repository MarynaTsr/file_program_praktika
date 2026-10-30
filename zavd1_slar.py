# -*- coding: utf-8 -*-
"""
Обчислювальна практика. Змістовий модуль 1.
Розв'язування систем лінійних алгебраїчних рівнянь (СЛАР). Варіант 9.
Методи: метод Крамера, метод Зейделя.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

AUTHOR = "Виконав(ла): ПІБ студента, група ___"   # впишіть свої дані
TOPIC = "Змістовий модуль 1. Розв'язування СЛАР. Варіант 9"

# Матриця коефіцієнтів і вектор вільних членів (варіант 9)
A0 = np.array([[0.45, 0.03, -0.01, 0.02, -0.111],
               [0.02, 0.375, -0.01, 0.01, 0.0],
               [0.0, 0.7, 0.44, 0.0, 0.113],
               [-0.03, 0.015, -0.02, 0.41, -0.084],
               [0.02, 0.01, 0.0, 0.0, 0.29]])
B0 = np.array([0.75, -1.738, 1.75, -2.138, -1.45])


def cramer(A, b):
    """Метод Крамера: x_i = det(A_i) / det(A)."""
    n = len(b)
    d = np.linalg.det(A)
    if abs(d) < 1e-12:
        raise ValueError("Визначник системи дорівнює нулю — метод Крамера не застосовний")
    dets = []
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b          # замінюємо i-й стовпець на стовпець вільних членів
        dets.append(np.linalg.det(Ai))
    x = np.array(dets) / d
    return x, d, dets


def seidel(A, b, eps=1e-4, max_iter=500):
    """Метод Зейделя: нові значення x_j використовуються одразу після обчислення."""
    n = len(b)
    if np.any(np.abs(np.diag(A)) < 1e-12):
        raise ValueError("На головній діагоналі є нульовий елемент")
    x = np.zeros(n)
    history = [x.copy()]
    for k in range(1, max_iter + 1):
        x_old = x.copy()
        for i in range(n):
            s1 = A[i, :i] @ x[:i]          # вже уточнені компоненти (k+1)
            s2 = A[i, i + 1:] @ x_old[i + 1:]  # компоненти з попередньої ітерації
            x[i] = (b[i] - s1 - s2) / A[i, i]
        history.append(x.copy())
        if np.max(np.abs(x - x_old)) < eps:
            return x, k, history
    raise RuntimeError("Ітераційний процес не збігся за %d ітерацій" % max_iter)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Завдання 1. СЛАР — методи Крамера та Зейделя")
        self.geometry("900x640")
        hdr = tk.Frame(self, bg="#1f4e79")
        hdr.pack(fill="x")
        tk.Label(hdr, text=AUTHOR, fg="white", bg="#1f4e79", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        tk.Label(hdr, text=TOPIC, fg="white", bg="#1f4e79", font=("Arial", 10)).pack(anchor="w", padx=10)
        tk.Label(hdr, text="Задача: розв'язати систему 5 лінійних рівнянь A·x = b. Коефіцієнти можна змінити в таблиці.",
                 fg="#dfe9f5", bg="#1f4e79", font=("Arial", 9)).pack(anchor="w", padx=10, pady=(0, 6))

        body = tk.Frame(self)
        body.pack(fill="both", expand=True, padx=10, pady=8)
        grid = tk.LabelFrame(body, text="Матриця A та стовпець b")
        grid.pack(fill="x")
        self.cells = []
        for j, name in enumerate(["x1", "x2", "x3", "x4", "x5", "", "b"]):
            tk.Label(grid, text=name, font=("Arial", 9, "bold")).grid(row=0, column=j, padx=2)
        for i in range(5):
            row = []
            for j in range(5):
                e = tk.Entry(grid, width=9, justify="right")
                e.insert(0, str(A0[i, j]))
                e.grid(row=i + 1, column=j, padx=2, pady=2)
                row.append(e)
            tk.Label(grid, text="=").grid(row=i + 1, column=5)
            e = tk.Entry(grid, width=9, justify="right")
            e.insert(0, str(B0[i]))
            e.grid(row=i + 1, column=6, padx=2)
            row.append(e)
            self.cells.append(row)

        ctl = tk.Frame(body)
        ctl.pack(fill="x", pady=6)
        tk.Label(ctl, text="Точність ε (для Зейделя):").pack(side="left")
        self.eps = tk.Entry(ctl, width=10)
        self.eps.insert(0, "0.0001")
        self.eps.pack(side="left", padx=4)
        ttk.Button(ctl, text="Метод Крамера", command=self.run_cramer).pack(side="left", padx=4)
        ttk.Button(ctl, text="Метод Зейделя", command=self.run_seidel).pack(side="left", padx=4)
        ttk.Button(ctl, text="Очистити", command=lambda: self.out.delete("1.0", "end")).pack(side="left", padx=4)

        self.out = tk.Text(body, font=("Courier New", 10), height=20)
        self.out.pack(fill="both", expand=True)

    def read(self):
        A = np.array([[float(self.cells[i][j].get().replace(",", ".")) for j in range(5)] for i in range(5)])
        b = np.array([float(self.cells[i][5].get().replace(",", ".")) for i in range(5)])
        return A, b

    def run_cramer(self):
        try:
            A, b = self.read()
            x, d, dets = cramer(A, b)
        except Exception as ex:
            messagebox.showerror("Помилка", str(ex)); return
        self.out.insert("end", "=== Метод Крамера ===\n")
        self.out.insert("end", "det(A) = %.8f\n" % d)
        for i, di in enumerate(dets):
            self.out.insert("end", "det(A%d) = %+.8f   x%d = %+.6f\n" % (i + 1, di, i + 1, x[i]))
        self.out.insert("end", "Нев'язка ||A·x - b|| = %.2e\n\n" % np.linalg.norm(A @ x - b))

    def run_seidel(self):
        try:
            A, b = self.read()
            eps = float(self.eps.get().replace(",", "."))
            x, k, hist = seidel(A, b, eps)
        except Exception as ex:
            messagebox.showerror("Помилка", str(ex)); return
        self.out.insert("end", "=== Метод Зейделя (ε = %g) ===\n" % eps)
        self.out.insert("end", " k " + "".join("%12s" % ("x%d" % (i + 1)) for i in range(5)) + "\n")
        for it, v in enumerate(hist):
            self.out.insert("end", "%2d " % it + "".join("%12.6f" % t for t in v) + "\n")
        self.out.insert("end", "Кількість ітерацій: %d; нев'язка = %.2e\n\n" % (k, np.linalg.norm(A @ x - b)))


if __name__ == "__main__":
    app = App()
    import os
    if os.environ.get("SNAP"):
        app.after(300, app.run_cramer); app.after(400, app.run_seidel)
    app.mainloop()
