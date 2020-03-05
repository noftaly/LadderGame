from tkinter import PhotoImage
from Sources.blocks import Blocks

images = {
    Blocks.BRICK: PhotoImage(file='Ressources/BRICK.gif'),
    Blocks.LADDER: PhotoImage(file='Ressources/LADDER.gif'),
    Blocks.TREASURE: PhotoImage(file='Ressources/TREASURE.gif'),
    Blocks.SPAWN_KNIGHT: PhotoImage(file='Ressources/Knight.gif'),
    Blocks.SPAWN_SKELETON: PhotoImage(file='Ressources/Skeleton.gif'),
}


class Tile:
    def __init__(self, canvas, tile_type, coords, solid, jumpable):
        self._x = coords[0]
        self._y = coords[1]
        self._coords = coords
        self._tile_type = tile_type
        self._solid = solid
        self._jumpable = jumpable
        if tile_type != Blocks.VOID:
            self._id = canvas.create_image(self.canvas_x(), self.canvas_y(), image=images[tile_type])
        else:
            self._id = None

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def coords(self):
        return self._coords

    @property
    def tile_type(self):
        return self._tile_type

    @property
    def solid(self):
        return self._solid

    @property
    def jumpable(self):
        return self._jumpable

    @property
    def id(self):
        return self._id

    @x.setter
    def x(self, x):
        self._x = x
        self._coords = (self._x, self._y)

    @y.setter
    def y(self, y):
        self._y = y
        self._coords = (self._x, self._y)

    def canvas_x(self):
        return self._x * 32 + 16

    def canvas_y(self):
        return self._y * 32 + 16

    def is_type(self, block):
        return self._tile_type is block
