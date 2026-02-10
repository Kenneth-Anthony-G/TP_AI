from tkinter import *
import random
import time
import pandas as pd
import numpy as np

NB_LIGNES = 4
NB_COLONNES = 4
CELL = 100
MARGE = 20
HAUTEUR = NB_LIGNES * CELL
LARGEUR = NB_COLONNES * CELL

EPSILON = 0.1
GAMMA = 0.9
TA_INITIAL = 0.1

NB_PERIODES = 200
SLEEP_STEP = 0.02

root = Tk()
root.title("Exercice 3 : Paradis (3,3) et Enfers")

canvas = Canvas(root, bg="white", height=HAUTEUR, width=LARGEUR)
canvas.pack()

agent_id = None
q_table = pd.DataFrame(columns=["haut", "bas", "gauche", "droite"], dtype=np.float64)


def coords_to_pixel(row, col):
    x0, y0 = col * CELL + MARGE, row * CELL + MARGE
    x1, y1 = (col + 1) * CELL - MARGE, (row + 1) * CELL - MARGE
    return x0, y0, x1, y1


def ajouter_etat_si_absent(E):
    global q_table
    if E not in q_table.index:
        q_table.loc[E] = [0.0, 0.0, 0.0, 0.0]


def init():
    global agent_id
    canvas.delete("all")
    for i in range(5):
        canvas.create_line(i * CELL, 0, i * CELL, HAUTEUR)
        canvas.create_line(0, i * CELL, LARGEUR, i * CELL)

    enfers = [(1, 2), (2, 1)]
    for r, c in enfers:
        x0, y0, x1, y1 = coords_to_pixel(r, c)
        canvas.create_rectangle(x0, y0, x1, y1, fill="black")

    px0, py0, px1, py1 = coords_to_pixel(2, 2)
    canvas.create_oval(px0, py0, px1, py1, fill="gold")

    ax0, ay0, ax1, ay1 = coords_to_pixel(0, 0)
    agent_id = canvas.create_rectangle(ax0, ay0, ax1, ay1, fill="red")

    return 0, 0


def choisir_action(E, epsilon):
    ajouter_etat_si_absent(E)
    if random.random() < epsilon:
        return random.choice(["haut", "bas", "gauche", "droite"])
    else:
        scores = q_table.loc[E, :]
        return random.choice(scores[scores == scores.max()].index.tolist())


def apprendre(E, a, E_suivant, row_suiv, col_suiv, ta):
    global q_table
    ajouter_etat_si_absent(E_suivant)

    # Récompenses
    if (row_suiv, col_suiv) == (2, 2):  # Paradis
        r = 1
        q_cible = r
    elif (row_suiv, col_suiv) in [(1, 2), (2, 1)]:  # Enfers
        r = -1
        q_cible = r
    else:  # Case normale
        r = 0
        q_cible = r + GAMMA * q_table.loc[E_suivant].max()

    q_table.loc[E, a] += ta * (q_cible - q_table.loc[E, a])


def entrainer_agent():
    current_ta = TA_INITIAL

    for periode in range(NB_PERIODES):
        row, col = init()
        E = str((row, col))
        termine = False
        nb_pas = 0

        while not termine:
            action = choisir_action(E, EPSILON)
            n_row, n_col = row, col
            if action == "haut" and row > 0:
                n_row -= 1
            elif action == "bas" and row < NB_LIGNES - 1:
                n_row += 1
            elif action == "gauche" and col > 0:
                n_col -= 1
            elif action == "droite" and col < NB_COLONNES - 1:
                n_col += 1

            row, col = n_row, n_col
            canvas.coords(agent_id, *coords_to_pixel(row, col))
            root.update()
            time.sleep(SLEEP_STEP)

            E_suiv = str((row, col))
            apprendre(E, action, E_suiv, row, col, current_ta)

            E = E_suiv
            nb_pas += 1

            if (row, col) in [(3, 3), (1, 2), (2, 1)]:
                termine = True

        resultat = "GAGNÉ" if (row, col) == (3, 3) else "PERDU (Enfer)"
        print(f"Période {periode + 1}/{NB_PERIODES} | Pas: {nb_pas} | Résultat: {resultat} | TA: {current_ta:.4f}")

        if current_ta > 0.01:
            current_ta -= 0.0005

    print("\n--- Entraînement terminé ---")


root.after(100, entrainer_agent)
root.mainloop()