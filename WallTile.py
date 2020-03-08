from Tile import Tile


class WallTile(Tile):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):

