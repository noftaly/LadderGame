# Créé par Elliot, le 02/07/2018 en Python 3.2
"""
TODO LIST:
    [V] Plusieurs niveaux
    [ ] Jump
    [V] Bug quand on atterit sur l'emplacement d'un coffre qui a déjà été pris : on est en l'air
    [V] Bug "index out of range" avec les coffres
    [ ] Téléporteur
    [ ] Ecran de départ
    [ ] Quand on arrive sur un bord de la map, on arrive de l'autre côté
    [ ] Echelles cassées, murs traversables
"""

import tkinter, os

# VARIABLES
from typing import List, Any

JUMP_HEIGHT = 3

niveau = 1
fenetre = tkinter.Tk()  # ==> Met la réf. de la fenêtre dans "fenetre"
canvas = tkinter.Canvas(fenetre, width=672, height=672)              # ==> Met la réf. du canvas dans "canvas"
personnage = tkinter.PhotoImage(file='Ressources/Personnage.gif')  # ==> Stocke l'image du perso dans "personnage"
brique = tkinter.PhotoImage(file='Ressources/Brique.gif')          # ==> Stocke l'image de la brique dans "brique"
echelle = tkinter.PhotoImage(file='Ressources/Echelle.gif')        # ==> Stocke l'image des échelles dans "echelle"
squelette = tkinter.PhotoImage(file='Ressources/Squelette.gif')    # ==> Stocke l'image du squelette dans "squelette"
tresor = tkinter.PhotoImage(file='Ressources/Tresor.gif')          # ==> Stocke l'image des tresors dans "tresor"

cases = []
touches: List[Any] = []
coffres = []
coffresX = []
coffresY = []


# CODE

# Fonctions
def movement():  # ==> Déplacement du personnage
    global xJoueur1, yJoueur1, joueur, xJoueur2, yJoueur2, joueur2

    # Guerrier
    if 'Right' in touches and cases[yJoueur1][xJoueur1+1] != 'X':
        xJoueur1 += 1
    elif 'Left' in touches and cases[yJoueur1][xJoueur1-1] != 'X':
        xJoueur1 -= 1
    elif 'Up' in touches and cases[yJoueur1-1][xJoueur1] != 'X' and cases[yJoueur1][xJoueur1] == 'H':
        yJoueur1 -= 1
    #elif 'Up' in touches and (cases[yJoueur1+JUMP_HEIGHT][xJoueur1] == ' ' or 'T') and cases[yJoueur1-1][xJoueur1] != ' ':
    #    yJoueur1 -= JUMP_HEIGHT
    elif 'Down' in touches and cases[yJoueur1+1][xJoueur1] != 'X' and (cases[yJoueur1][xJoueur1] == 'H' or cases[yJoueur1+1][xJoueur1] == 'H'):
        yJoueur1 += 1

    # Squelette
    if 'd' in touches and cases[yJoueur2][xJoueur2+1] != 'X':
        xJoueur2 += 1
    elif 'q' in touches and cases[yJoueur2][xJoueur2-1] != 'X':
        xJoueur2 -= 1
    elif 'z' in touches and cases[yJoueur2-1][xJoueur2] != 'X' and cases[yJoueur2][xJoueur2] == 'H':
        yJoueur2 -= 1
    elif 's' in touches and cases[yJoueur2+1][xJoueur2] != 'X' and (cases[yJoueur2][xJoueur2] == 'H' or cases[yJoueur2+1][xJoueur2] == 'H'):
        yJoueur2 += 1

    # Vérification des coffres
    for i in range(len(coffres)):
        if (xJoueur1 == coffresX[i] and yJoueur1 == coffresY[i]) or (xJoueur1 == coffresX[i] and (yJoueur1+1) == coffresY[i]):
            canvas.delete(coffres[i])
            del(coffres[i])
            del(coffresX[i])
            del(coffresY[i])
            if len(coffres) == 0:
                canvas.create_rectangle(0, 0, 672, 672, fill='white')
                canvas.create_text(350, 300, text='Victoire', fill='#444fff444', font=('Arial', 70))
                fenetre.after(3000, creerNiveau)
            break

    # Vérification des collisions entre squelette/guerrier
    if xJoueur1 == xJoueur2 and yJoueur1 == yJoueur2:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(325, 300, text='Game Over', fill='red', font=('Arial', 70))
        return

    canvas.coords(joueur, xJoueur1*32+16, yJoueur1*32+16)
    canvas.coords(joueur2, xJoueur2*32+16, yJoueur2*32+16)

    fenetre.after(115, movement)


def gravite():
    global xJoueur1, yJoueur1, joueur, xJoueur2, yJoueur2, joueur2

    if cases[yJoueur1+1][xJoueur1] in [' ', 'S', 'T', 'M']:
        yJoueur1 += 1
    if cases[yJoueur2+1][xJoueur2] in [' ', 'S', 'M']:
        yJoueur2 += 1

    canvas.coords(joueur, xJoueur1*32+16, yJoueur1*32+16)
    canvas.coords(joueur2, xJoueur2*32+16, yJoueur2*32+16)
    fenetre.after(115, gravite)


def creerNiveau():
    global cases, canvas, coffres, coffresX, coffresY, xJoueur1, yJoueur1, xJoueur2, yJoueur2, joueur, joueur2, fichier2, niveau
    while len(cases) > 0:
        del(cases[0])
    while len(coffres) > 0:
        del(coffres[0])
    while len(coffresX) > 0:
        del(coffresX[0])
    while len(coffresY) > 0:
        del(coffresY[0])

    canvas.delete('all')

    exists = os.path.isfile('Niveau ' + str(niveau) + '.txt')
    if exists:
        fichier = open('Niveau ' + str(niveau) + '.txt')
        niveau += 1
        for i in fichier:
            cases.append(i)
        fichier.close()

        for i in range(21):
            for j in range(21):
                if cases[i][j] == 'X':
                    canvas.create_image(j*32+16, i*32+16, image=brique) # ==> Affichage des briques
                elif cases[i][j] == 'H':
                    canvas.create_image(j*32+16, i*32+16, image=echelle) # ==> Affichage des échelles
                elif cases[i][j] == 'T':
                    coffres.append(canvas.create_image(j*32+16, i*32+16, image=tresor)) # ==> Affichage des tresors
                    coffresX.append(j)
                    coffresY.append(i)

        for i in range(21):
            for j in range(21):
                if cases[i][j] == 'M':
                    xJoueur1 = j
                    yJoueur1 = i
                    joueur = canvas.create_image(xJoueur1*32+16, yJoueur1*32+16, image=personnage) # ==> Ajoute l'image au canvas
                elif cases[i][j] == 'S':
                    xJoueur2 = j
                    yJoueur2 = i
                    joueur2 = canvas.create_image(xJoueur2*32+16, xJoueur2*32+16, image=squelette) # ==> Affichage des squelettes
    else:
        canvas.create_rectangle(0, 0, 672, 672, fill='white')
        canvas.create_text(350, 300, text='Le jeu est fini :)', fill='#444fff444', font=('Arial', 70))


def enfoncee(evt):
    if evt.keysym not in touches:
        touches.append(evt.keysym)


def relachee(evt):
    if evt.keysym in touches:
        touches.remove(evt.keysym)


# Main
canvas.bind('<KeyPress>', enfoncee)
canvas.bind('<KeyRelease>', relachee)
canvas.focus_set()

creerNiveau()
canvas.pack()
movement()
gravite()
fenetre.mainloop()
