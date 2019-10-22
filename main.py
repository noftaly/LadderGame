# Créé par Elliot, le 02/07/2018 en Python 3.2
"""
TODO:
    - Idées :
    - [ ] Jump
    - [ ] Téléporteur
    - [ ] Ecran de départ
    - [ ] Quand on arrive sur un bord de la map, on arrive de l'autre côté
    - [ ] Echelles cassées, murs traversables
    
    - BugFixes :
    - [ ] Quand le jeu est finit (écran "Le jeu est finit") : Erreur "Index out of range"
    - [ ] Quand un squelette arrive sur (dessus) l'emplacement d'un ancien coffre, pris, il ne tombe pas
"""
"""
DOC:
    [ ] = Vide
    [X] = Briques
    [H] = Échelles
    [T] = Trésor
    [M] = Guerrier
    [S] = Squelette

"""

import tkinter, os
from typing import List, Any

# JUMP_HEIGHT = 3

level = 1
window = tkinter.Tk()
window.title('LadderGame')
canvas = tkinter.Canvas(window, width=672, height=672)
knight = tkinter.PhotoImage(file='Ressources/Knight.gif')
brick = tkinter.PhotoImage(file='Ressources/Brick.gif')
ladder = tkinter.PhotoImage(file='Ressources/Ladder.gif')
skeleton = tkinter.PhotoImage(file='Ressources/Skeleton.gif')
treasure = tkinter.PhotoImage(file='Ressources/Treasure.gif')

cells = []
keys: List[Any] = []
chests = []
chestsX = []
chestsY = []
xPlayer1 = 0
yPlayer1 = 0
xPlayer2 = 0
yPlayer2 = 0

# Functions
def movement():
    global xPlayer1, yPlayer1, player, xPlayer2, yPlayer2, player2

    # Knight
    if 'Right' in keys and cells[yPlayer1][xPlayer1+1] != 'X':
        xPlayer1 += 1
    elif 'Left' in keys and cells[yPlayer1][xPlayer1-1] != 'X':
        xPlayer1 -= 1
    elif 'Up' in keys and cells[yPlayer1-1][xPlayer1] != 'X' and cells[yPlayer1][xPlayer1] == 'H':
        yPlayer1 -= 1
    # elif 'Up' in keys and (cells[yPlayer1+JUMP_HEIGHT][xPlayer1] == ' ' or 'T') and cells[yPlayer1-1][xPlayer1] != ' ':
    #    yPlayer1 -= JUMP_HEIGHT
    elif 'Down' in keys and cells[yPlayer1+1][xPlayer1] != 'X' and (cells[yPlayer1][xPlayer1] == 'H' or cells[yPlayer1+1][xPlayer1] == 'H'):
        yPlayer1 += 1

    # Skeleton
    if 'd' in keys and cells[yPlayer2][xPlayer2+1] != 'X':
        xPlayer2 += 1
    elif 'q' in keys and cells[yPlayer2][xPlayer2-1] != 'X':
        xPlayer2 -= 1
    elif 'z' in keys and cells[yPlayer2-1][xPlayer2] != 'X' and cells[yPlayer2][xPlayer2] == 'H':
        yPlayer2 -= 1
    elif 's' in keys and cells[yPlayer2+1][xPlayer2] != 'X' and (cells[yPlayer2][xPlayer2] == 'H' or cells[yPlayer2+1][xPlayer2] == 'H'):
        yPlayer2 += 1

    # Check chests
    for i in range(len(chests)):
        if (xPlayer1 == chestsX[i] and yPlayer1 == chestsY[i]) or (xPlayer1 == chestsX[i] and (yPlayer1+1) == chestsY[i]):
            canvas.delete(chests[i])
            del(chests[i])
            del(chestsX[i])
            del(chestsY[i])
            if len(chests) == 0:
                canvas.create_rectangle(0, 0, 672, 672, fill='white')
                canvas.create_text(350, 300, text='Bravo !', fill='#66BB66', font=('Arial', 70))
                window.after(1000, create_level)
            break

    # Check collisions between skeleton and knight
    if xPlayer1 == xPlayer2 and yPlayer1 == yPlayer2:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(325, 300, text='Oh non :(', fill='#CC6666', font=('Arial', 70))
        canvas.create_text(330, 500, text='Le squellette à gagné !', fill='#CC6666', font=('Arial', 40))
        return

    canvas.coords(player, xPlayer1*32+16, yPlayer1*32+16)
    canvas.coords(player2, xPlayer2*32+16, yPlayer2*32+16)

    window.after(115, movement)


def gravity():
    global xPlayer1, yPlayer1, player, xPlayer2, yPlayer2, player2

    if cells[yPlayer1+1][xPlayer1] in [' ', 'S', 'T', 'K']:
        yPlayer1 += 1
    if cells[yPlayer2+1][xPlayer2] in [' ', 'S', 'K']:
        yPlayer2 += 1

    canvas.coords(player, xPlayer1*32+16, yPlayer1*32+16)
    canvas.coords(player2, xPlayer2*32+16, yPlayer2*32+16)
    window.after(115, gravity)


def create_level():
    global cells, canvas, chests, chestsX, chestsY, xPlayer1, yPlayer1, xPlayer2, yPlayer2, player, player2, level

    while len(cells) > 0:
        del(cells[0])
    while len(chests) > 0:
        del(chests[0])
        del(chestsX[0])
        del(chestsY[0])

    canvas.delete('all')

    exists = os.path.isfile('Niveau ' + str(level) + '.txt')
    if exists:
        file = open('Niveau ' + str(level) + '.txt')
        level += 1
        for i in file:
            cells.append(i)
        file.close()

        # Display images
        for i in range(21):
            for j in range(21):
                # Brick
                if cells[i][j] == 'X':
                    canvas.create_image(j*32+16, i*32+16, image=brick)
                # Ladder
                elif cells[i][j] == 'H':
                    canvas.create_image(j*32+16, i*32+16, image=ladder)
                # Treasure
                elif cells[i][j] == 'T':
                    chests.append(canvas.create_image(j*32+16, i*32+16, image=treasure))
                    chestsX.append(j)
                    chestsY.append(i)
                # Knight
                elif cells[i][j] == 'K':
                    xPlayer1 = j
                    yPlayer1 = i
                    player = canvas.create_image(xPlayer1*32+16, yPlayer1*32+16, image=knight)
                # Skeleton
                elif cells[i][j] == 'S':
                    xPlayer2 = j
                    yPlayer2 = i
                    player2 = canvas.create_image(xPlayer2*32+16, xPlayer2*32+16, image=skeleton)
    else:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(350, 285, text='Le jeu est fini :)', fill='#66BB66', font=('Arial', 70))


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
movement()
gravity()
window.mainloop()
