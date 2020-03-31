import pygame
import constants


class Character:
    def __init__(self, game):
        self.game = game

    def clear(self):
        sprite_size = self.game.sprite_sheet.sprite_size
        pygame.draw.rect(self.game.window, constants.BACKGROUND_COLOR,
                         (self.x - sprite_size / 2, self.y - sprite_size / 2, sprite_size, sprite_size))
