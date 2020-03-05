# Créé par Elliot, le 02/07/2018 en Python 3.2
import tkinter
import os
from typing import List, Any

window = tkinter.Tk()

from Sources.player import Player
from Sources.tile import Tile
from Sources.blocks import Blocks

"""
TODO:
    - Idées :
    - [x] Jump
    - [ ] Téléporteur
    - [ ] Ecran de départ
    - [ ] Quand on arrive sur un bord de la map, on arrive de l'autre côté
    - [ ] Echelles cassées, murs traversables
"""

level = 1
finished = False
cells = []
keys: List[Any] = []
chests = []

window.title('LadderGame')

canvas = tkinter.Canvas(window, width=21*32, height=21*32)

knight = None
skeleton = None


# Functions
def game_end(end_type):
    if end_type == 0:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(350, 300, text='Le chevalier a gagné !', fill='#66BB66', font=('Arial', 70))
        window.after(2000, create_level)
    elif end_type == 1:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(325, 300, text='Oh non :(', fill='#CC6666', font=('Arial', 70))
        canvas.create_text(330, 500, text='Le squellette a gagné !', fill='#CC6666', font=('Arial', 40))
        window.after(2000, lambda: exit(0))
    elif end_type == 2:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(350, 285, text='Le jeu est fini :)', fill='#66BB66', font=('Arial', 70))


def movement():
    global knight, skeleton, cells, finished

    knight.move(cells, keys)
    skeleton.move(cells, keys)

    # Check chests
    for chest in chests:
        if (knight.coords == chest.coords) or (knight.x == chest.x and (knight.y+1) == chest.y):
            canvas.delete(chest.id)
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

    if not cells[knight.y+1][knight.x].solid and not cells[knight.y+1][knight.x].is_type(Blocks.LADDER):
        knight.y += 1
    if not cells[skeleton.y+1][skeleton.x].solid                             \
            and not cells[skeleton.y+1][skeleton.x].is_type(Blocks.TREASURE)  \
            and not cells[skeleton.y+1][skeleton.x].is_type(Blocks.LADDER):
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

        for line in file:
            cell_line = []
            for char in line:
                if char == '\n' or char == '\r' or char == '\r\n':
                    continue
                cell_line.append(str(char))
            cells.append(cell_line)

        file.close()

        # Display images
        for i in range(21):
            for j in range(21):
                if cells[i][j] == Blocks.BRICK.value:
                    cells[i][j] = Tile(canvas, Blocks.BRICK, (j, i), True, True)

                elif cells[i][j] == Blocks.LADDER.value:
                    cells[i][j] = Tile(canvas, Blocks.LADDER, (j, i), False, True)

                elif cells[i][j] == Blocks.TREASURE.value:
                    cells[i][j] = Tile(canvas, Blocks.TREASURE, (j, i), False, True)
                    chests.append(cells[i][j])

                elif cells[i][j] == Blocks.VOID.value:
                    cells[i][j] = Tile(canvas, Blocks.VOID, (j, i), False, False)

                elif cells[i][j] == Blocks.SPAWN_KNIGHT.value:
                    cells[i][j] = Tile(canvas, Blocks.VOID, (j, i), False, False)
                    knight = Player(Blocks.SPAWN_KNIGHT, canvas, (j, i), False, False)

                elif cells[i][j] == Blocks.SPAWN_SKELETON.value:
                    cells[i][j] = Tile(canvas, Blocks.VOID, (j, i), False, False)
                    skeleton = Player(Blocks.SPAWN_SKELETON, canvas, (j, i), False, False)

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
