from tabnanny import check

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
        point_depart = np.array([UNIT / 8, UNIT / 8])

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

    def check_state_exist(self):
        s = str(self.canvas.coords(self.rect))
        if s not in self.q_table.index:
            self.q_table = self.q_table._append(
                pd.Series(
                    [0]*len(self.action_space),
                    index=self.q_table.columns,
                    name=s
                )
            )

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 'droite':
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 'gauche':
            if s[0] > UNIT:
                base_action[0] -= UNIT
        self.canvas.move(self.rect, base_action[0], base_action[1])
        if self.canvas.coords(self.rect) == self.canvas.coords(self.oval):
            return 0
        else:
            return 1

    def choisir_action(self):
        env.check_state_exist()
        if np.random.rand() < 0.1:
            action = np.random.choice(self.action_space)
        else:
            s = str(self.canvas.coords(self.rect))
            action_scores = self.q_table.loc[s, :]
            action = np.random.choice(action_scores[action_scores == np.max(action_scores)].index)


        return action

    def apprendre(self, action,etat_actuel, etat_suivant):
        self.check_state_exist()
        if etat_suivant == self.canvas.coords(self.oval):
            q_cible = 1
        else:
            action_scores = self.q_table.loc[str(etat_suivant), :]
            q_cible = 0.9 * np.max(action_scores)
        q_actuel = self.q_table.loc[str(etat_actuel), action]

        self.q_table.loc[str(etat_actuel),action] = 0.01 * (q_cible - q_actuel)

def update():
    etat_actuel = env.canvas.coords(env.rect)
    action = env.choisir_action()
    a = env.step(action)
    etat_suivant = env.canvas.coords(env.rect)
    env.apprendre(action,etat_actuel,etat_suivant)
    if a == 0:
        print(env.q_table)
        env.canvas.move(env.rect, -UNIT * (MAZE_W - 1)  , 0)
        env.after(200, update)
    else:
        env.after(200, update)

if __name__ == "__main__":
    env = Maze()
    env.check_state_exist()
    update()
    env.mainloop()