# Créé par Elliot, le 02/07/2018 en Python 3.2
import tkinter
import os
from typing import List, Any

from player import Player
from tile import Tile

"""
TODO:
    - Idées :
    - [ ] Jump
    - [ ] Téléporteur
    - [ ] Ecran de départ
    - [ ] Quand on arrive sur un bord de la map, on arrive de l'autre côté
    - [ ] Echelles cassées, murs traversables
"""

# JUMP_HEIGHT = 3
VOID = ' '
BRICK = 'X'
LADDER = 'H'
TREASURE = 'T'
SPAWN_KNIGHT = 'K'
SPAWN_SKELETON = 'S'

level = 1
finished = False
cells = []
keys: List[Any] = []
chests = []

window = tkinter.Tk()
window.title('LadderGame')

canvas = tkinter.Canvas(window, width=672, height=672)
knight_image = tkinter.PhotoImage(file='Ressources/Knight.gif')
brick_image = tkinter.PhotoImage(file='Ressources/Brick.gif')
ladder_image = tkinter.PhotoImage(file='Ressources/Ladder.gif')
skeleton_image = tkinter.PhotoImage(file='Ressources/Skeleton.gif')
treasure_image = tkinter.PhotoImage(file='Ressources/Treasure.gif')

knight = None
skeleton = None


# Functions
def game_end(end_type):
    if end_type == 0:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(350, 300, text='Le chavalier à gagné !', fill='#66BB66', font=('Arial', 70))
        window.after(2000, create_level)
    elif end_type == 1:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(325, 300, text='Oh non :(', fill='#CC6666', font=('Arial', 70))
        canvas.create_text(330, 500, text='Le squellette à gagné !', fill='#CC6666', font=('Arial', 40))
        window.after(2000, lambda: exit(0))
    elif end_type == 2:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(350, 285, text='Le jeu est fini :)', fill='#66BB66', font=('Arial', 70))
        window.after(2000, lambda: exit(0))


def movement():
    global knight, skeleton, cells, finished

    knight.move(cells, keys, BRICK, LADDER)
    skeleton.move(cells, keys, BRICK, LADDER)

    # Check chests
    for chest in chests:
        if (knight.x == chest.x and knight.y == chest.y) or (knight.x == chest.x and (knight.y+1) == chest.y):
            canvas.delete(chest.id)

            # Set the chest position to VOID
            s = list(cells[knight.y])
            s[knight.x] = VOID
            cells[knight.y] = ''.join(s)

            chests.remove(chest)
            if len(chests) == 0:
                game_end(0)
                finished = True

    # Check collisions between skeleton and knight
    if knight.x == skeleton.x and knight.y == skeleton.y and not finished:
        game_end(1)
        finished = True

    if finished:
        return

    canvas.coords(knight.id, knight.canvas_x(), knight.canvas_y())
    canvas.coords(skeleton.id, skeleton.canvas_x(), skeleton.canvas_y())

    window.after(115, movement)


def gravity():
    global knight, skeleton

    if cells[knight.y+1][knight.x] in [VOID, SPAWN_SKELETON, TREASURE, SPAWN_KNIGHT]:
        knight.y += 1
    if cells[skeleton.y+1][skeleton.x] in [VOID, SPAWN_SKELETON, SPAWN_KNIGHT]:
        skeleton.y += 1

    if finished:
        return

    canvas.coords(knight.id, knight.canvas_x(), knight.canvas_y())
    canvas.coords(skeleton.id, skeleton.canvas_x(), skeleton.canvas_y())
    window.after(115, gravity)


def create_level():
    global cells, canvas, chests, knight, skeleton, level, finished

    cells = []
    chests = []

    canvas.delete('all')

    exists = os.path.isfile('Levels/level_' + str(level) + '.txt')
    if exists:
        file = open('Levels/level_' + str(level) + '.txt')
        level += 1
        for char in file:
            cells.append(str(char))
        file.close()

        # Display images
        for i in range(21):
            for j in range(21):
                if cells[i][j] == BRICK:
                    Tile(canvas, brick_image, j, i)

                elif cells[i][j] == LADDER:
                    Tile(canvas, ladder_image, j, i)

                elif cells[i][j] == TREASURE:
                    chest = Tile(canvas, treasure_image, j, i)
                    chests.append(chest)

                elif cells[i][j] == SPAWN_KNIGHT:
                    knight = Player('knight', canvas, knight_image, j, i)

                elif cells[i][j] == SPAWN_SKELETON:
                    skeleton = Player('skeleton', canvas, skeleton_image, j, i)

        # Start movement loop
        finished = False
        movement()
        gravity()
    else:
        game_end(2)
        finished = True


def key_pressed(evt):
    if evt.keysym not in keys:
        keys.append(evt.keysym)


def key_released(evt):
    if evt.keysym in keys:
        keys.remove(evt.keysym)


# Main
canvas.bind('<KeyPress>', key_pressed)
canvas.bind('<KeyRelease>', key_released)
canvas.focus_set()

create_level()
canvas.pack()

window.mainloop()
