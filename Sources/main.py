# coding: utf8

import tkinter
window = tkinter.Tk()

from Sources.game import Game

"""
TODO:
    - Ideas :
    - [x] Jump
    - [ ] Teleport tiles
    - [ ] Starting screen
    - [ ] When on the edge of the map, make us appear on the other side
    - [ ] Broken ladders
"""

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
