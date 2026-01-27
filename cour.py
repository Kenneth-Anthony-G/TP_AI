import tkinter as tk
import sys

UNIT = 80
MAZE_H = 6
MAZE_W = 6

HALF_UNIT = UNIT / 2
HALF_UNIT_MINUS10 = HALF_UNIT - 10
SIZE = int(3 * UNIT / 8)


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT,))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAZE_H * UNIT,
                                width=MAZE_W * UNIT,)
        self.canvas.pack()



if __name__ == "__main__":
    print(__name__)
    env = Maze()
    env.mainloop()