import os
from typing import List, Any

from Sources.player import Player
from Sources.tile import Tile
from Sources.blocks import Blocks


keys: List[Any] = []


def key_pressed(evt):
    if evt.keysym not in keys:
        keys.append(evt.keysym)


def key_released(evt):
    if evt.keysym in keys:
        keys.remove(evt.keysym)


# Main
class Game:
    def __init__(self, window, canvas):
        self.canvas = canvas
        self.window = window
        self.finished = False
        self.cells = []
        self.chests = []
        self.level = 1

        self.canvas.bind('<KeyPress>', key_pressed)
        self.canvas.bind('<KeyRelease>', key_released)
        self.canvas.delete('all')

        exists = os.path.isfile(f'../Levels/level_{str(self.level)}.txt')
        if exists:
            file = open('../Levels/level_' + str(self.level) + '.txt')
            self.level += 1

            for line in file:
                cell_line = []
                for char in line:
                    if char == '\n' or char == '\r' or char == '\r\n':
                        continue
                    cell_line.append(str(char))
                self.cells.append(cell_line)

            file.close()

            # Display images
            for i in range(21):
                for j in range(21):
                    if self.cells[i][j] == Blocks.BRICK.value:
                        self.cells[i][j] = Tile(self.canvas, Blocks.BRICK, (j, i), True, True)

                    elif self.cells[i][j] == Blocks.LADDER.value:
                        self.cells[i][j] = Tile(self.canvas, Blocks.LADDER, (j, i), False, True)

                    elif self.cells[i][j] == Blocks.TREASURE.value:
                        self.cells[i][j] = Tile(self.canvas, Blocks.TREASURE, (j, i), False, True)
                        self.chests.append(self.cells[i][j])

                    elif self.cells[i][j] == Blocks.VOID.value:
                        self.cells[i][j] = Tile(self.canvas, Blocks.VOID, (j, i), False, False)

                    elif self.cells[i][j] == Blocks.SPAWN_KNIGHT.value:
                        self.cells[i][j] = Tile(self.canvas, Blocks.VOID, (j, i), False, False)
                        self.knight = Player(Blocks.SPAWN_KNIGHT, self.canvas, (j, i), False, False)

                    elif self.cells[i][j] == Blocks.SPAWN_SKELETON.value:
                        self.cells[i][j] = Tile(self.canvas, Blocks.VOID, (j, i), False, False)
                        self.skeleton = Player(Blocks.SPAWN_SKELETON, self.canvas, (j, i), False, False)

            # Start movement loop
            self.movement()
            self.gravity()
        else:
            self.game_end(2)
            self.finished = True

    def gravity(self):
        if not self.cells[self.knight.y+1][self.knight.x].solid \
                and not self.cells[self.knight.y+1][self.knight.x].is_type(Blocks.LADDER):
            self.knight.y += 1
        if not self.cells[self.skeleton.y+1][self.skeleton.x].solid                             \
                and not self.cells[self.skeleton.y+1][self.skeleton.x].is_type(Blocks.TREASURE) \
                and not self.cells[self.skeleton.y+1][self.skeleton.x].is_type(Blocks.LADDER):
            self.skeleton.y += 1

        if self.finished:
            return

        self.canvas.coords(self.knight.id, self.knight.canvas_x(), self.knight.canvas_y())
        self.canvas.coords(self.skeleton.id, self.skeleton.canvas_x(), self.skeleton.canvas_y())
        self.window.after(115, self.gravity)

    def movement(self):
        self.knight.move(self.cells, keys)
        self.skeleton.move(self.cells, keys)

        # Check chests
        for chest in self.chests:
            if (self.knight.coords == chest.coords) or (self.knight.x == chest.x and (self.knight.y+1) == chest.y):
                self.canvas.delete(chest.id)
                self.chests.remove(chest)

                if len(self.chests) == 0:
                    self.game_end(0)
                    finished = True

        # Check collisions between skeleton and knight
        if self.knight.x == self.skeleton.x and self.knight.y == self.skeleton.y and not self.finished:
            self.game_end(1)
            finished = True

        if self.finished:
            return

        self.canvas.coords(self.knight.id, self.knight.canvas_x(), self.knight.canvas_y())
        self.canvas.coords(self.skeleton.id, self.skeleton.canvas_x(), self.skeleton.canvas_y())

        self.window.after(115, self.movement)

    # End the game with the provided exit code
    # 0: Knight wins
    # 1: Skeleton wins
    # 2: Game is finished
    def game_end(self, end_type):
        if end_type == 0:
            self.canvas.create_rectangle(0, 0, 672, 672, fill='white')
            self.canvas.create_text(350, 300, text='Le chevalier a gagné !', fill='#66BB66', font=('Arial', 70))
            self.window.after(2000, lambda: exit(0))
        elif end_type == 1:
            self.canvas.create_rectangle(0, 0, 672, 672, fill='white')
            self.canvas.create_text(325, 300, text='Oh non :(', fill='#CC6666', font=('Arial', 70))
            self.canvas.create_text(330, 500, text='Le squellette a gagné !', fill='#CC6666', font=('Arial', 40))
            self.window.after(2000, lambda: exit(0))
        elif end_type == 2:
            self.canvas.create_rectangle(0, 0, 672, 672, fill='white')
            self.canvas.create_text(350, 285, text='Le jeu est fini :)', fill='#66BB66', font=('Arial', 70))
