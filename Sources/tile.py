from typing import Optional
from tkinter import PhotoImage, Canvas
from Sources.blocks import Blocks

images = {
    Blocks.BRICK: PhotoImage(file='../Resources/Brick.gif'),
    Blocks.LADDER: PhotoImage(file='../Resources/Ladder.gif'),
    Blocks.TREASURE: PhotoImage(file='../Resources/Treasure.gif'),
    Blocks.SPAWN_KNIGHT: PhotoImage(file='../Resources/Knight.gif'),
    Blocks.SPAWN_SKELETON: PhotoImage(file='../Resources/Skeleton.gif'),
}


class Tile:
    def __init__(self, canvas: Canvas, tile_type: Blocks, coords: (int, int), solid: bool, jumpable: bool):
        self._x: int = coords[0]
        self._y: int = coords[1]
        self._coords = coords
        self._tile_type = tile_type
        self._solid = solid
        self._jumpable = jumpable
        self._id: Optional[int] = None
        if tile_type != Blocks.VOID:
            self._id = canvas.create_image(self.canvas_x(), self.canvas_y(), image=images[tile_type])

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def coords(self) -> (int, int):
        return self._coords

    @property
    def tile_type(self) -> Blocks:
        return self._tile_type

    @property
    def solid(self) -> bool:
        return self._solid

    @property
    def jumpable(self) -> bool:
        return self._jumpable

    @property
    def id(self) -> Optional[int]:
        return self._id

    @x.setter
    def x(self, x) -> None:
        self._x = x
        self._coords = (self._x, self._y)

    @y.setter
    def y(self, y) -> None:
        self._y = y
        self._coords = (self._x, self._y)

    def canvas_x(self) -> int:
        return self._x * 32 + 16

    def canvas_y(self) -> int:
        return self._y * 32 + 16

    def is_type(self, block) -> bool:
        return self._tile_type is block
