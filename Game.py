import os
import pygame
import time
import math
import constants
import Map
import SpriteSheet
import Player
from Ghosts import Blinky
from Ghosts import Inky
from Ghosts import Pinky
from Ghosts import Clyde

class Game:
    def __init__(self):
        self.map = Map.Map()
        self.__delay = 1000 / constants.TICKRATE
        self.tick = 0
        self.level = 0
        self.score = 0
        self.player = None
        self.ghosts = []
        os.environ['SDL_VIDEO_WINDOW_POS'] = "512, 32"
        self.window = pygame.display.set_mode((
            self.get_screen_width(),
            self.get_screen_height()))
        self.sprite_sheet = SpriteSheet.SpriteSheet()
        self.initialize_level()

    def initialize_level(self):
        self.map.initialize_map()
        self.draw_walls()
        self.draw_pellets()
        player_pos = self.map.get_coordinates('s')
        blinky_pos = self.map.get_coordinates('b')
        pinky_pos  = self.map.get_coordinates('p')
        inky_pos   = self.map.get_coordinates('i')
        clyde_pos  = self.map.get_coordinates('c')
        self.player = Player.Player(self, player_pos[0], player_pos[1])
        self.ghosts = []
        self.ghosts.append(Blinky.Blinky(self, blinky_pos[0], blinky_pos[1]))
        self.ghosts.append(Pinky.Pinky(self, pinky_pos[0], pinky_pos[1]))
        self.ghosts.append(Inky.Inky(self, inky_pos[0], inky_pos[1]))
        self.ghosts.append(Clyde.Clyde(self, clyde_pos[0], clyde_pos[1]))
        self.level += 1
        self.update_caption()

    def update_caption(self):
        pygame.display.set_caption("Pacman level: " + str(self.level) + " score: " + str(self.score))

    def step(self):
        start_time_ms = time.time()
        if not self.player.eat():
            self.player.move()
        self.draw_characters()
        self.draw_pellets()
        pygame.display.update()  # room for improvement
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
                pygame.draw.arc(self.window, constants.WALL_COLOR,
                                ((wall[0] + 0.5) * ts, (wall[1] + offset + 0.5) * ts, ts, ts),
                                math.pi / 2, math.pi, lw)
            elif wall[2] == 1:
                pygame.draw.arc(self.window, constants.WALL_COLOR,
                                ((wall[0] - 0.5) * ts + lw / 2, (wall[1] + offset + 0.5) * ts, ts, ts),
                                0, math.pi / 2, lw)
            elif wall[2] == 2:
                pygame.draw.arc(self.window, constants.WALL_COLOR,
                                ((wall[0] - 0.5) * ts + lw / 2, (wall[1] + offset - 0.5) * ts + lw / 2, ts, ts),
                                math.pi * 3 / 2, 0, lw)
            elif wall[2] == 3:
                pygame.draw.arc(self.window, constants.WALL_COLOR,
                                ((wall[0] + 0.5) * ts, (wall[1] + offset - 0.5) * ts + lw / 2, ts, ts),
                                math.pi, math.pi * 3 / 2, lw)
            elif wall[2] == 4:
                pygame.draw.line(self.window, constants.WALL_COLOR,
                                 ((wall[0] + 0.5) * ts, (wall[1] + offset) * ts),
                                 ((wall[0] + 0.5) * ts, (wall[1] + offset + 1) * ts), lw)
            elif wall[2] == 5:
                pygame.draw.line(self.window, constants.WALL_COLOR,
                                 ((wall[0])     * ts, (wall[1] + offset + 0.5) * ts),
                                 ((wall[0] + 1) * ts, (wall[1] + offset + 0.5) * ts), lw)

        pygame.display.update()

    def draw_characters(self):
        for ghost in self.ghosts:
            ghost.draw()
        self.player.draw()

    def clear_characters(self):
        for ghost in self.ghosts:
            ghost.clear()
        self.player.clear()

    def draw_pellets(self):
        ts = self.map.tile_size
        size = ts / 8
        offset = ts / 2 - size / 2

        for pellet in self.map.get_pellets():
            if pellet[2] == '.':
                pygame.draw.rect(self.window, constants.PELLET_COLOR,
                                 (pellet[0] * ts + offset, pellet[1] * ts + offset, size, size))
            elif pellet[2] == 'o':
                pygame.draw.circle(self.window, constants.PELLET_COLOR,
                                   (int((pellet[0] + 0.5) * ts), int((pellet[1] + 0.5) * ts)), int(size * 2))
