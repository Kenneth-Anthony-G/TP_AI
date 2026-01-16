import tkinter as tk
import numpy as np



n = 6
size = 50

grid = np.zeros((n, n))
grid[5, 5] = 1  # première case rouge

root = tk.Tk()
canvas = tk.Canvas(root, width=n*size, height=n*size)


for i in range(n):
    for j in range(n):
        match i:
            case 0 | 2 | 4:
                color = "red"
                canvas.create_rectangle(
                    j*size, i*size,
                    (j+1)*size, (i+1)*size,
                    fill=color, outline="black"
                )
                continue
            case 1 | 3 | 5:
                color = "yellow"
                canvas.create_oval(
                    j*size, i*size,
                    (j+1)*size, (i+1)*size,
                    fill=color, outline="black"
                )
                continue
            case _:
                color = "white"
canvas.pack()
root.mainloop()