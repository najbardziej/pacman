""""""
from game_files import constants, drawhelper


class Barrier:
    def __init__(self, tiles):
        self.tiles = tiles
        self.visible = False

    def get_entrance(self):
        avg_x = sum(t[0] for t in self.tiles) / len(self.tiles)
        avg_y = sum(t[1] for t in self.tiles) / len(self.tiles)
        return avg_x, avg_y - 1

    def get_spawn(self):
        entrance_x, entrance_y = self.get_entrance()
        return entrance_x, entrance_y + 3

    def draw_barrier(self, color):
        if self.visible:
            for tile_x, tile_y in self.tiles:
                drawhelper.draw_line(tile_x - 0.25, tile_y + 0.5,
                                     tile_x + 1.25, tile_y + 0.5,
                                     color=color)

    def draw(self):
        self.draw_barrier(constants.BARRIER_COLOR)

    def clear(self):
        self.draw_barrier(constants.BACKGROUND_COLOR)
