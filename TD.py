import tkinter as tk
import numpy as np

n = 6
size = 50

grid = np.zeros((n, n))
grid[5, 5] = 1  # première case rouge

root = tk.Tk()
canvas = tk.Canvas(root, width=n*size, height=n*size)

isRect = True

for i in range(n):
    isRect = not isRect
    for j in range(n):
        if(isRect):
            canvas.create_rectangle(
                    j*size, i*size,
                    (j+1)*size, (i+1)*size,
                    fill='red', outline="black"
                )
        else :
            canvas.create_oval(
                    j*size, i*size,
                    (j+1)*size, (i+1)*size,
                    fill='yellow', outline="black"
                )
        isRect = not isRect
canvas.pack()
root.mainloop()