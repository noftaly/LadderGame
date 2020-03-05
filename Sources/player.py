from Sources.tile import Tile
from Sources.blocks import Blocks

JUMP_HEIGHT = 3


class Player(Tile):
    def __init__(self, player_type, canvas, coords, solid, jumpable):
        Tile.__init__(self, canvas, player_type, coords, solid, jumpable)

        if player_type == Blocks.SPAWN_KNIGHT:
            self.right_key = 'Right'
            self.left_key = 'Left'
            self.up_key = 'Up'
            self.down_key = 'Down'

        elif player_type == Blocks.SPAWN_SKELETON:
            self.right_key = 'd'
            self.left_key = 'q'
            self.up_key = 'z'
            self.down_key = 's'

    def move(self, cells, keys):
        x = self.x
        y = self.y

        if self.right_key in keys and cells[y][x+1].tile_type != Blocks.BRICK:
            self.x += 1
        elif self.left_key in keys and cells[y][x-1].tile_type != Blocks.BRICK:
            self.x -= 1
        elif self.up_key in keys and cells[y-1][x].tile_type != Blocks.BRICK and cells[y][x].tile_type == Blocks.LADDER:
            self.y -= 1
        elif self.down_key in keys and cells[y+1][x].tile_type != Blocks.BRICK\
                and (cells[y][x].tile_type == Blocks.LADDER or cells[y+1][x].tile_type == Blocks.LADDER):
            self.y += 1

        elif self.up_key in keys and cells[y+1][x].jumpable:
            for i in range(JUMP_HEIGHT):
                if cells[y-i][x].solid:
                    return

            self.y -= JUMP_HEIGHT
