import enum
import os
from typing import List, Optional, Final

from tkinter import Canvas, Tk

from Sources.player import Player
from Sources.tile import Tile
from Sources.blocks import Blocks


keys: List[str] = []


def key_pressed(evt):
    if evt.keysym not in keys:
        keys.append(evt.keysym)


def key_released(evt):
    if evt.keysym in keys:
        keys.remove(evt.keysym)


class FinishCodes(enum.Enum):
    NOT_FINISHED = 0
    KNIGHT_WINS = 1
    SKELETON_WINS = 2
    GAME_ENDED = 3


# Main
class Game:
    def __init__(self, window: Tk, canvas: Canvas):
        self.canvas: Final[Canvas] = canvas
        self.window: Final[Tk] = window
        self.finished = False
        self.paused = True
        self.cells: List[List[Tile]] = []
        self.chests: List[Tile] = []
        self.level = 0

        self.knight: Optional[Player] = None
        self.skeleton: Optional[Player] = None

        self.canvas.bind('<KeyPress>', key_pressed)
        self.canvas.bind('<KeyRelease>', key_released)
        self.canvas.delete('all')

        self.next_level()

        # Start ticking
        self.next_tick()

    def next_level(self, finish_code: FinishCodes = FinishCodes.NOT_FINISHED) -> None:
        # We pause the ticks (movement and gravity loops)
        self.paused = True

        exists = os.path.isfile(f'../Levels/level_{str(self.level + 1)}.txt')
        # If there is a file and the skeleton did not won, then we load the next level
        if exists and finish_code is not FinishCodes.SKELETON_WINS:
            self.load_level()
        else:
            self.game_end(finish_code)

    def load_level(self) -> None:
        self.level += 1

        file = open(f'../Levels/level_{str(self.level)}.txt')
        lines = file.readlines()
        file.close()

        file_cells: List[List[str]] = []
        self.cells = []
        self.canvas.delete('all')

        for line in lines:
            cell_line: List[str] = []
            for char in line:
                if char == '\n' or char == '\r' or char == '\r\n':
                    continue
                cell_line.append(str(char))
            file_cells.append(cell_line)

        # Display images
        for i in range(21):
            self.cells.append([])
            for j in range(21):
                if file_cells[i][j] is Blocks.BRICK.value:
                    self.cells[i].append(Tile(self.canvas, Blocks.BRICK, (j, i), True, True))

                elif file_cells[i][j] is Blocks.LADDER.value:
                    self.cells[i].append(Tile(self.canvas, Blocks.LADDER, (j, i), False, True))

                elif file_cells[i][j] is Blocks.TREASURE.value:
                    self.cells[i].append(Tile(self.canvas, Blocks.TREASURE, (j, i), False, True))
                    self.chests.append(self.cells[i][j])

                elif file_cells[i][j] is Blocks.SPAWN_KNIGHT.value:
                    self.cells[i].append(Tile(self.canvas, Blocks.VOID, (j, i), False, False))
                    self.knight = Player(Blocks.SPAWN_KNIGHT, self.canvas, (j, i), False, False)

                elif file_cells[i][j] is Blocks.SPAWN_SKELETON.value:
                    self.cells[i].append(Tile(self.canvas, Blocks.VOID, (j, i), False, False))
                    self.skeleton = Player(Blocks.SPAWN_SKELETON, self.canvas, (j, i), False, False)

                else:
                    self.cells[i].append(Tile(self.canvas, Blocks.VOID, (j, i), False, False))

        self.paused = False

    def next_tick(self) -> None:
        print(keys)
        if not self.paused:
            self.movement()
            self.gravity()

        if not self.finished:
            self.window.after(115, self.next_tick)

    def redraw(self) -> None:
        self.canvas.coords(self.knight.id, self.knight.canvas_x(), self.knight.canvas_y())
        self.canvas.coords(self.skeleton.id, self.skeleton.canvas_x(), self.skeleton.canvas_y())

    def gravity(self) -> None:
        if not self.cells[self.knight.y+1][self.knight.x].solid \
                and not self.cells[self.knight.y+1][self.knight.x].is_type(Blocks.LADDER):
            self.knight.y += 1
        if not self.cells[self.skeleton.y+1][self.skeleton.x].solid                             \
                and not self.cells[self.skeleton.y+1][self.skeleton.x].is_type(Blocks.TREASURE) \
                and not self.cells[self.skeleton.y+1][self.skeleton.x].is_type(Blocks.LADDER):
            self.skeleton.y += 1

        self.redraw()

    def movement(self) -> None:
        self.knight.move(self.cells, keys)
        self.skeleton.move(self.cells, keys)

        # Check chests
        for chest in self.chests:
            if (self.knight.coords == chest.coords) or (self.knight.x == chest.x and (self.knight.y+1) == chest.y):
                self.canvas.delete(chest.id)
                self.chests.remove(chest)

                if len(self.chests) == 0:
                    self.next_level(FinishCodes.KNIGHT_WINS)
                    return

        # Check collisions between skeleton and knight
        if self.knight.x == self.skeleton.x and self.knight.y == self.skeleton.y and not self.finished:
            self.next_level(FinishCodes.SKELETON_WINS)
            return

        self.redraw()

    def game_end(self, finish_code: FinishCodes) -> None:
        self.finished = True
        if finish_code is FinishCodes.KNIGHT_WINS:
            self.canvas.create_rectangle(0, 0, 672, 672, fill='white')
            self.canvas.create_text(350, 300, text='Le chevalier a gagné !', fill='#66BB66', font=('Arial', 70))
            self.window.after(2000, lambda: exit(0))
        elif finish_code is FinishCodes.SKELETON_WINS:
            self.canvas.create_rectangle(0, 0, 672, 672, fill='white')
            self.canvas.create_text(325, 300, text='Oh non :(', fill='#CC6666', font=('Arial', 70))
            self.canvas.create_text(330, 500, text='Le squellette a gagné !', fill='#CC6666', font=('Arial', 40))
            self.window.after(2000, lambda: exit(0))
        elif finish_code is FinishCodes.GAME_ENDED:
            self.canvas.create_rectangle(0, 0, 672, 672, fill='white')
            self.canvas.create_text(350, 285, text='Le jeu est fini :)', fill='#66BB66', font=('Arial', 70))
        else:
            self.canvas.create_rectangle(0, 0, 672, 672, fill='white')
            self.canvas.create_text(353, 285, text='Argh, impossible :(', fill='#66BB66', font=('Arial', 65))
