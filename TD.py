from tabnanny import check

import numpy as np
import time
import pandas as pd
import random
import tkinter as tk

UNIT = 100
MAZE_H = 6
MAZE_W = 6
HALF_UNIT = UNIT/2
HALF_UNIT_MINOS_10 = UNIT/2 - 10
SIZE = int(3*UNIT/8)

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.title('Maze')
        self.action_space = ['gauche','droite','haut','bas']
        self.n_actions = len(self.action_space)
        self.q_table = pd.DataFrame(columns=self.action_space,dtype=np.float64)
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT,))
        self.start_state = (1, 1)
        self.hell_states = [(2, 3), (3, 2)]
        self.goal_state = (6, 6)
        self.epsilon = 0.1
        self.gamma = 0.9
        self.alpha = 0.01

        self._build_maze()

    def grid_to_canvas(self, i, j):
        x0 = (j - 1) * UNIT + UNIT / 8
        y0 = (i - 1) * UNIT + UNIT / 8
        x1 = x0 + 3 * UNIT / 4
        y1 = y0 + 3 * UNIT / 4
        return x0, y0, x1, y1

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
        # enfers
        for (i, j) in self.hell_states:
            self.canvas.create_rectangle(
                *self.grid_to_canvas(i, j),
                fill='brown'
            )

        # paradis
        self.oval = self.canvas.create_oval(
            *self.grid_to_canvas(*self.goal_state),
            fill='yellow'
        )

        # agent (départ)
        self.rect = self.canvas.create_rectangle(
            *self.grid_to_canvas(*self.start_state),
            fill='red'
        )

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
        if action == 'droite' and s[0] < (MAZE_W - 1) * UNIT:
            base_action[0] += UNIT
        elif action == 'gauche' and s[0] > 0:
            base_action[0] -= UNIT
        elif action == 'haut' and s[1] > 0:
            base_action[1] -= UNIT
        elif action == 'bas' and s[1] < (MAZE_H - 1) * UNIT:
            base_action[1] += UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])
        next_state = self.canvas.coords(self.rect)

        # paradis
        if next_state == self.canvas.coords(self.oval):
            return next_state, 1, True

        # enfer
        for hell in self.hell_states:
            if next_state == list(self.grid_to_canvas(*hell)):
                return next_state, -1, True

        # état normal
        return next_state, 0, False

    def choisir_action(self):
        env.check_state_exist()
        if np.random.rand() < 0.1:
            action = np.random.choice(self.action_space)
        else:
            s = str(self.canvas.coords(self.rect))
            action_scores = self.q_table.loc[s, :]
            action = np.random.choice(action_scores[action_scores == np.max(action_scores)].index)
        return action

    def apprendre(self, s, a, r, s_):
        self.check_state_exist()
        q_predict = self.q_table.loc[str(s), a]

        if r != 0:
            q_target = r
        else:
            q_target = r + self.gamma * self.q_table.loc[str(s_)].max()

        self.q_table.loc[str(s), a] += self.alpha * (q_target - q_predict)


def update():
    state = env.canvas.coords(env.rect)

    action = env.choisir_action()
    next_state, reward, done = env.step(action)

    env.apprendre(state, action, reward, next_state)

    if done:
        print(env.q_table)
        # retour à l'état initial (1,1)
        x0, y0, x1, y1 = env.grid_to_canvas(*env.start_state)
        env.canvas.coords(env.rect, x0, y0, x1, y1)

        env.after(200, update)
    else:
        env.after(50, update)



if __name__ == "__main__":
    env = Maze()
    env.check_state_exist()
    update()
    env.mainloop()