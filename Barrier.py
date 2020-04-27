import pygame
import constants


class Barrier:
    def __init__(self, game):
        self.game = game
        self.tiles = []
        self.visible = False

    def get_entrance(self):
        avg_x = 0
        avg_y = 0
        for tile in self.tiles:
            avg_x += tile[0]
            avg_y += tile[1]
        avg_x /= len(self.tiles)
        avg_y /= len(self.tiles)
        return avg_x, avg_y

    def add_tile(self, tile_x, tile_y):
        self.tiles.append((tile_x, tile_y))

    def draw(self):
        if self.visible:
            ts = constants.TILE_SIZE
            lw = int(ts / 8)
            offset = 0
            for tile in self.tiles:
                pygame.draw.line(self.game.window, constants.BARRIER_COLOR,
                                 ((tile[0] - 0.25) * ts, (tile[1] + offset + 0.5) * ts),
                                 ((tile[0] + 1.25) * ts, (tile[1] + offset + 0.5) * ts), lw)

    def clear(self):
        if self.visible:
            ts = constants.TILE_SIZE
            lw = int(ts / 8)
            offset = 0
            for tile in self.tiles:
                pygame.draw.line(self.game.window, constants.BACKGROUND_COLOR,
                                 ((tile[0] - 0.25) * ts, (tile[1] + offset + 0.5) * ts),
                                 ((tile[0] + 1.25) * ts, (tile[1] + offset + 0.5) * ts), lw)
