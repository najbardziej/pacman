"""Module containing barrier class - used for letting the ghosts out"""
from game_files import constants, drawhelper


class Barrier:
    """Class used for letting the ghosts out"""
    def __init__(self, tiles):
        self.tiles = tiles
        self.visible = False

    def get_entrance(self):
        """Returns coordinates of the barrier entrance"""
        avg_x = sum(t[0] for t in self.tiles) / len(self.tiles)
        avg_y = sum(t[1] for t in self.tiles) / len(self.tiles)
        return avg_x, avg_y - 1

    def get_spawn(self):
        """Returns coordinates of the ghost spawn"""
        entrance_x, entrance_y = self.get_entrance()
        return entrance_x, entrance_y + 3

    def draw_barrier(self, color):
        """Draws barrier with a given color"""
        if self.visible:
            for tile_x, tile_y in self.tiles:
                drawhelper.draw_line(tile_x - 0.25, tile_y + 0.5,
                                     tile_x + 1.25, tile_y + 0.5,
                                     color=color)

    def draw(self):
        """Draws barrier"""
        self.draw_barrier(constants.BARRIER_COLOR)

    def clear(self):
        """Clears barrier"""
        self.draw_barrier(constants.BACKGROUND_COLOR)
