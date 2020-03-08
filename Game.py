import pygame

from Map import Map


class Game:
    def __init__(self, tickrate, tile_size, game_map_file, caption):
        with open(game_map_file) as file:
            game_map = [line.rstrip('\n') for line in file]
        self.map = Map(game_map=game_map,
                       tile_size=tile_size)
        self.__delay = 1000 / tickrate
        self.window = pygame.display.set_mode((
            self.get_screen_width(),
            self.get_screen_height()))
        pygame.init()
        pygame.display.set_caption(caption)

    def step(self):
        pygame.display.update()

    def get_base_delay(self):
        return self.__delay

    def get_screen_width(self):
        return self.map.get_width()

    def get_screen_height(self):
        return self.map.get_height() + 3 * self.map.tile_size

    def delay(self, time):
        pygame.time.delay(time)

    def draw_walls(self):
        for wall in self.map.get_walls():
            pygame.draw.rect(self.window, 
                             (17, 17, 193), 
                             (wall[0] * self.map.tile_size, (wall[1] + 3) * self.map.tile_size,
                              self.map.tile_size, self.map.tile_size))
        pygame.display.update()

