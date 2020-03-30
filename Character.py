import pygame
import enum

COLOR_BLACK = (0, 0, 0)


class Direction(enum.IntEnum):
    RIGHT = 0
    UP    = 1
    LEFT  = 2
    DOWN  = 3


class Character:
    def __init__(self, game):
        self.game = game

    def clear(self):
        sprite_size = self.game.sprite_sheet.sprite_size
        pygame.draw.rect(self.game.window, COLOR_BLACK,
                         (self.x - sprite_size / 2, self.y - sprite_size / 2, sprite_size, sprite_size))
