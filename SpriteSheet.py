import pygame


class SpriteSheet:
    def __init__(self, file, sprite_size, sprite_spacing):
        self.__sheet          = pygame.image.load(file).convert()
        self.__sprite_size    = sprite_size
        self.__sprite_spacing = sprite_spacing

    def get_image_at(self, x, y):
        rectangle = \
            pygame.Rect((
                x * (self.__sprite_size + self.__sprite_spacing * 2) + self.__sprite_spacing,
                y * (self.__sprite_size + self.__sprite_spacing * 2) + self.__sprite_spacing,
                self.__sprite_size,
                self.__sprite_size
            ))
        image = pygame.Surface(rectangle.size).convert()
        image.blit(self.__sheet, (0, 0), rectangle)
        return image
