from Sources.tile import Tile

JUMP_HEIGHT = 3
VOID = ' '
BRICK = 'X'
LADDER = 'H'
TREASURE = 'T'
SPAWN_KNIGHT = 'K'
SPAWN_SKELETON = 'S'


class Player (Tile):
    def __init__(self, player_type, canvas, image, x, y):
        Tile.__init__(self, canvas, image, x, y)
        if player_type == 'knight':
            self.right_key = 'Right'
            self.left_key = 'Left'
            self.up_key = 'Up'
            self.down_key = 'Down'
        elif player_type == 'skeleton':
            self.right_key = 'd'
            self.left_key = 'q'
            self.up_key = 'z'
            self.down_key = 's'

    def move(self, cells, keys):
        if self.right_key in keys and cells[self.y][self.x + 1] != BRICK:
            self.x += 1
        elif self.left_key in keys and cells[self.y][self.x - 1] != BRICK:
            self.x -= 1
        elif self.up_key in keys and cells[self.y - 1][self.x] != BRICK and cells[self.y][self.x] == LADDER:
            self.y -= 1
        elif self.down_key in keys and cells[self.y + 1][self.x] != BRICK and (cells[self.y][self.x] == LADDER or cells[self.y + 1][self.x] == LADDER):
            self.y += 1

        elif self.up_key in keys and cells[self.y + 1][self.x] != VOID:
            for i in range(JUMP_HEIGHT):
                if cells[self.y - i][self.x] != VOID:
                    return
            self.y -= JUMP_HEIGHT
