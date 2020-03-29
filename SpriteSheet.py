import pygame


class SpriteSheet:
    def __init__(self, file, sprite_size, sprite_spacing):
        self.__sheet        = pygame.image.load(file).convert()
        self.sprite_size    = sprite_size
        self.sprite_spacing = sprite_spacing

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
