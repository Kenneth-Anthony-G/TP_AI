import numpy as np
import time
import pandas as pd
import random
import tkinter as tk

UNIT = 100
MAZE_H = 1
MAZE_W = 6
HALF_UNIT = UNIT/2
HALF_UNIT_MINOS_10 = UNIT/2 - 10
SIZE = int(3*UNIT/8)

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.title('Maze')
        self.action_space = ['gauche','droite']
        self.n_actions = len(self.action_space)
        self.q_table = pd.DataFrame(columns=self.action_space,dtype=np.float64)
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT,))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAZE_H * UNIT,
                                width=MAZE_W * UNIT,)
        self.canvas.pack()

        # Column
        for c in range(MAZE_W + 1):
            x0, y0 = c * UNIT, 0
            x1, y1 = x0, y0 + MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)

        # Row
        for r in range(MAZE_H + 1):
            x0, y0 = 0, r * UNIT
            x1, y1 = x0 + MAZE_W * UNIT, y0
            self.canvas.create_line(x0, y0, x1, y1)

        # creer le point de départ
        point_depart = [UNIT / 8, UNIT / 8]
        print(point_depart)

        # creer un carre a la premiere case
        x0, y0 = point_depart[0], point_depart[1]
        x1, y1 = x0 + 3 * UNIT/4, y0 + 3 * UNIT/4,
        self.rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill='red')

        #creer un rond a la sixieme case
        x0, y0 = point_depart[0] + (MAZE_W - 1) * UNIT, point_depart[1]
        x1, y1 = x0 + 3 * UNIT/4, y0 + 3 * UNIT/4
        self.oval = self.canvas.create_oval(x0, y0, x1, y1, fill='yellow')

        #pack all
        self.canvas.pack()

        return self.rect



if __name__ == "__main__":
    env = Maze()
    print('afficher la table',env.q_table)
    env.mainloop()

