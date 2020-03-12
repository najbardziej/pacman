import pygame
import time
import math
import Map

WALL_COLOR = (17, 17, 193)

class Game:
    def __init__(self, tickrate, tile_size, game_map_file, caption):
        with open(game_map_file) as file:
            game_map = [line.rstrip('\n') for line in file]
        self.map = Map.Map(game_map=game_map,
                           tile_size=tile_size)
        self.__delay = 1000 / tickrate
        self.window = pygame.display.set_mode((
            self.get_screen_width(),
            self.get_screen_height()))
        pygame.init()
        pygame.display.set_caption(caption)

    def step(self):
        start_time_ms = time.time()
        pygame.display.update()
        return time.time() - start_time_ms

    def get_base_delay(self):
        return self.__delay

    def get_screen_width(self):
        return self.map.get_width()

    def get_screen_height(self):
        return self.map.get_height() + 3 * self.map.tile_size

    def delay(self, time):
        pygame.time.delay(int(time))

    def draw_walls(self):
        for wall in self.map.get_walls():
            if wall[2] == 0:
                pygame.draw.rect(self.window, WALL_COLOR,
                                 (wall[0] * self.map.tile_size, (wall[1] + 3) * self.map.tile_size, self.map.tile_size, self.map.tile_size))
            elif wall[2] == 1:
                pygame.draw.arc(self.window, (255, 0, 0),
                                ((wall[0] + 0.5) * self.map.tile_size, (wall[1] + 3.5) * self.map.tile_size, self.map.tile_size, self.map.tile_size), math.pi/2, math.pi, int(self.map.tile_size / 8))
            elif wall[2] == 2:
                pygame.draw.arc(self.window, (255, 0, 0),
                                ((wall[0] - 0.5) * self.map.tile_size, (wall[1] + 3.5) * self.map.tile_size, self.map.tile_size, self.map.tile_size), 0, math.pi/2, int(self.map.tile_size / 8))
            elif wall[2] == 3:
                pygame.draw.arc(self.window, (255, 0, 0),
                                ((wall[0] - 0.5) * self.map.tile_size, (wall[1] + 2.5) * self.map.tile_size, self.map.tile_size, self.map.tile_size), math.pi*3/2, 0, int(self.map.tile_size / 8))
            elif wall[2] == 4:
                pygame.draw.arc(self.window, (255, 0, 0),
                                ((wall[0] + 0.5) * self.map.tile_size, (wall[1] + 2.5) * self.map.tile_size, self.map.tile_size, self.map.tile_size), math.pi, math.pi*3/2, int(self.map.tile_size / 8))
            elif wall[2] == 5:
                pygame.draw.line(self.window, (255, 0, 0),
                                ((wall[0]) * self.map.tile_size, (wall[1] + 3.5) * self.map.tile_size), ((wall[0] + 1) * self.map.tile_size, (wall[1] + 3.5) * self.map.tile_size), int(self.map.tile_size / 8))
            elif wall[2] == 6:
                pygame.draw.line(self.window, (255, 0, 0),
                                ((wall[0] + 0.5) * self.map.tile_size, (wall[1] + 3) * self.map.tile_size), ((wall[0] + 0.5) * self.map.tile_size, (wall[1] + 4) * self.map.tile_size), int(self.map.tile_size / 8))
        pygame.display.update()
