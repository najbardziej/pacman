import pygame
import constants


class SpriteSheet:
    def __init__(self):
        self.__sheet        = pygame.image.load(constants.SPRITE_SHEET_FILE).convert()
        self.sprite_size    = constants.SPRITE_SHEET_SPRITE_SIZE
        self.sprite_spacing = constants.SPRITE_SHEET_SPRITE_SPACING

    def get_image_at(self, x, y):
        rectangle = \
            pygame.Rect((
                x * (self.sprite_size + self.sprite_spacing * 2) + self.sprite_spacing,
                y * (self.sprite_size + self.sprite_spacing * 2) + self.sprite_spacing,
                self.sprite_size,
                self.sprite_size
            ))
        image = pygame.Surface(rectangle.size).convert()
        image.blit(self.__sheet, (0, 0), rectangle)
        return image
