# coding: utf8

import tkinter
window = tkinter.Tk()

from Sources.game import Game

window.title('LadderGame')

canvas = tkinter.Canvas(window, width=21*32, height=21*32)
canvas.focus_set()

game = Game(window, canvas)
canvas.pack()

window.mainloop()
