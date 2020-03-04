class Tile:
    def __init__(self, canvas, image, x, y):
        self._x = x
        self._y = y
        self._id = canvas.create_image(self.canvas_x(), self.canvas_y(), image=image)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def id(self):
        return self._id

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    def canvas_x(self):
        return self._x * 32 + 16

    def canvas_y(self):
        return self._y * 32 + 16
