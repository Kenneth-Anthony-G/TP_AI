import numpy as np
import time
import pandas as pd
import random
import tkinter as tk

UNIT = 100
MAZE_H = 3
MAZE_W = 3
SIZE = int(3*UNIT/8)

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.title('Maze')
        self.action_space = list(range(9))
        self.available_actions = self.action_space.copy()
        self.n_actions = len(self.action_space)
        self.cases = {}
        self.etat = [0] * self.n_actions
        self.q_table = pd.DataFrame(columns=self.action_space,dtype=np.float64)
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT,))
        self.isCroix = True
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAZE_H * UNIT,
                                width=MAZE_W * UNIT)
        self.canvas.pack()
        self._build_maze()

    def _build_maze(self):
        self.canvas.delete("all")

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

        num = 0

        for r in range(MAZE_H):
            for c in range(MAZE_W):
                self.cases[num] = (r,c)
                num += 1

        self.canvas.pack()

    def check_end(self):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # lignes
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colonnes
            (0, 4, 8), (2, 4, 6)  # diagonales
        ]

        for a, b, c in wins:
            if self.etat[a] != 0 and self.etat[a] == self.etat[b] == self.etat[c]:
                # victoire
                return 1, True

        # match nul
        if 0 not in self.etat:
            return 0, True

        # partie continue
        return 0, False

    def step(self, action):
        row, col = self.cases[action]
        x0 = col * UNIT + UNIT / 8
        y0 = row * UNIT + UNIT / 8
        x1, y1 = x0 + 3 * UNIT / 4, y0 + 3 * UNIT / 4

        if self.isCroix:
            self.canvas.create_oval(x0, y0, x1, y1, fill='yellow')
            self.etat[action] = 1
        else:
            self.canvas.create_oval(x0, y0, x1, y1, fill='black')
            self.etat[action] = 2
        self.isCroix = not self.isCroix


    def choisir_action(self):
        choice = random.choice(self.available_actions)
        self.available_actions.remove(choice)

        return choice

def update():
    reward, done =  env.check_end()
    if done:
        if reward == 1:
            print("Win")
        else:
            print("Nul")
        env.etat = [0] * env.n_actions
        env.available_actions = env.action_space.copy()
        env._build_maze()
    else:
        choice = env.choisir_action()
        print(env.etat)
        env.step(choice)
    env.after(1000, update)  # rappel après 1 seconde


if __name__ == "__main__":
    env = Maze()
    update()
    env.mainloop()
