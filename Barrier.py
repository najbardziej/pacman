import pygame
import constants


class Barrier:
    def __init__(self, game):
        self.game = game
        self.tiles = []

    def add_tile(self, tile_x, tile_y):
        self.tiles.append((tile_x, tile_y))

    def draw(self):
        ts = self.game.map.tile_size
        lw = int(ts / 8)
        offset = 0
        for tile in self.tiles:
            pygame.draw.line(self.game.window, constants.BARRIER_COLOR,
                             ((tile[0] - 0.25) * ts, (tile[1] + offset + 0.5) * ts),
                             ((tile[0] + 1.25) * ts, (tile[1] + offset + 0.5) * ts), lw)

    def clear(self):
        ts = self.game.map.tile_size
        lw = int(ts / 8)
        offset = 0
        for tile in self.tiles:
            pygame.draw.line(self.game.window, constants.BACKGROUND_COLOR,
                             ((tile[0] - 0.25) * ts, (tile[1] + offset + 0.5) * ts),
                             ((tile[0] + 1.25) * ts, (tile[1] + offset + 0.5) * ts), lw)
