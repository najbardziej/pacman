import pygame
from game_files import constants


class Character:
    def __init__(self, game, tile_x, tile_y):
        self.game = game
        self.x = (tile_x + 1) * self.game.map.tile_size
        self.y = (tile_y + 0.5) * self.game.map.tile_size

    def clear(self):
        pygame.draw.rect(self.game.window,
                         constants.BACKGROUND_COLOR,
                         (self.x - constants.SPRITE_SIZE / 2,
                          self.y - constants.SPRITE_SIZE / 2,
                          constants.SPRITE_SIZE,
                          constants.SPRITE_SIZE))

    def get_tile_x(self):
        return self.x // constants.TILE_SIZE

    def get_tile_y(self):
        return self.y // constants.TILE_SIZE
