import os

import pygame
import time
import math
import Map
import SpriteSheet
import Player

WALL_COLOR = (17, 17, 193)


class Game:
    def __init__(self, tickrate, tile_size, game_map_file,
                 sprite_sheet_file, sprite_sheet_sprite_size, sprite_sheet_sprite_spacing):
        with open(game_map_file) as file:
            game_map = [line.rstrip('\n') for line in file]
        self.map = Map.Map(game_map=game_map,
                           tile_size=tile_size)
        self.__delay = 1000 / tickrate
        self.tick = 0
        os.environ['SDL_VIDEO_WINDOW_POS'] = "512, 32"
        self.window = pygame.display.set_mode((
            self.get_screen_width(),
            self.get_screen_height()))
        self.sprite_sheet = \
            SpriteSheet.SpriteSheet(
                file=sprite_sheet_file,
                sprite_size=sprite_sheet_sprite_size,
                sprite_spacing=sprite_sheet_sprite_spacing
            )
        self.player = Player.Player(self, 1, 1)
        pygame.init()
        pygame.display.set_caption("Pacman")

    def step(self):
        start_time_ms = time.time()
        self.player.move()
        self.draw_characters()
        pygame.display.update()
        self.tick += 1
        self.clear_characters()
        return time.time() - start_time_ms

    def get_base_delay(self):
        return self.__delay

    def get_screen_width(self):
        return self.map.get_width()

    def get_screen_height(self):
        return self.map.get_height()
        #+ 3 * self.map.tile_size

    def delay(self, time):
        pygame.time.delay(int(time))

    def draw_walls(self):
        ts = self.map.tile_size
        lw = int(ts / 8)
        offset = 0
        for wall in self.map.get_walls():
            if wall[2] == 0:
                pygame.draw.arc(self.window, WALL_COLOR,
                                ((wall[0] + 0.5) * ts, (wall[1] + offset + 0.5) * ts, ts, ts),
                                math.pi / 2, math.pi, lw)
            elif wall[2] == 1:
                pygame.draw.arc(self.window, WALL_COLOR,
                                ((wall[0] - 0.5) * ts + lw / 2, (wall[1] + offset + 0.5) * ts, ts, ts),
                                0, math.pi / 2, lw)
            elif wall[2] == 2:
                pygame.draw.arc(self.window, WALL_COLOR,
                                ((wall[0] - 0.5) * ts + lw / 2, (wall[1] + offset - 0.5) * ts + lw / 2, ts, ts),
                                math.pi * 3 / 2, 0, lw)
            elif wall[2] == 3:
                pygame.draw.arc(self.window, WALL_COLOR,
                                ((wall[0] + 0.5) * ts, (wall[1] + offset - 0.5) * ts + lw / 2, ts, ts),
                                math.pi, math.pi * 3 / 2, lw)
            elif wall[2] == 4:
                pygame.draw.line(self.window, WALL_COLOR,
                                 ((wall[0] + 0.5) * ts, (wall[1] + offset) * ts),
                                 ((wall[0] + 0.5) * ts, (wall[1] + offset + 1) * ts), lw)
            elif wall[2] == 5:
                pygame.draw.line(self.window, WALL_COLOR,
                                 ((wall[0])     * ts, (wall[1] + offset + 0.5) * ts),
                                 ((wall[0] + 1) * ts, (wall[1] + offset + 0.5) * ts), lw)

        pygame.display.update()

    def draw_characters(self):
        # for character in self.character_list:
        #     character.draw()
        self.player.draw()

    def clear_characters(self):
        # for character in self.character_list:
        #     character.clear()
        self.player.clear()
