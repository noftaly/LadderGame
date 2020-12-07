# coding: utf8

import tkinter
window = tkinter.Tk()

from Sources.game import Game

level = 1
finished = False
cells = []
chests = []

window.title('LadderGame')

canvas = tkinter.Canvas(window, width=21*32, height=21*32)

knight = None
skeleton = None

canvas.focus_set()

game = Game(window, canvas)
canvas.pack()

window.mainloop()
