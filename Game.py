import os
import sys
import pygame
import time
import math
import random
import constants
import Map
import SpriteSheet
import Player
import Barrier
from Ghosts import Blinky
from Ghosts import Inky
from Ghosts import Pinky
from Ghosts import Clyde


class Game:
    def __init__(self):
        self.map = Map.Map()
        self.tick = 0
        self.level = 0
        self.score = 0
        self.barrier = None
        self.player = None
        self.fruit = 0
        self.lives = 1
        self.combo = 1
        self.wait = 0
        self.ghosts = []
        self.previous_ghosts_state = constants.GhostState.SCATTER
        os.environ['SDL_VIDEO_WINDOW_POS'] = "512, 32"
        pygame.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), constants.SPRITE_SHEET_SPRITE_SIZE)
        self.window = pygame.display.set_mode((
            self.get_screen_width(),
            self.get_screen_height()))
        self.sprite_sheet = SpriteSheet.SpriteSheet()
        self.initialize_level()

    def initialize_level(self):
        self.map.initialize_map()
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
        self.barrier = Barrier.Barrier(self)
        for b in self.map.get_barriers():
            self.barrier.add_tile(b[0], b[1])
        self.draw_walls()
        self.draw_pellets()
        self.level += 1
        self.fruit = 0
        self.update_caption()
        self.wait = 1

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def update_caption(self):
        pygame.display.set_caption("Pacman level: " + str(self.level) + \
                                   " score: " + str(self.score) + \
                                   " lives: " + str(self.lives))

    def display_text(self, string):
        text = self.font.render(string, True, constants.TEXT_COLOR, constants.BACKGROUND_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.map.get_width() // 2, self.map.get_height() // 2 + 2 * constants.TILE_SIZE)
        self.window.blit(text, text_rect)

    def clear_text(self):
        pygame.draw.rect(self.window, constants.BACKGROUND_COLOR,
                         (self.map.get_width() // 2 - 3 * constants.SPRITE_SHEET_SPRITE_SIZE,
                          self.map.get_height() // 2 + constants.SPRITE_SHEET_SPRITE_SIZE,
                          6 * constants.SPRITE_SHEET_SPRITE_SIZE, constants.TILE_SIZE))

    def step(self):
        start_time = time.time()
        if not self.wait:
            if self.player.eat():
                self.spawn_fruit()
                if self.next_level():
                    return (time.time() - start_time) * 1000
            else:
                self.player.move()
            self.change_ghost_states()
            if self.check_collisions():
                return (time.time() - start_time) * 1000
            for ghost in self.ghosts:
                ghost.move()
            self.draw_fruit()
            self.draw_pellets()
            self.draw_characters()
            pygame.display.update()  # room for improvement
            self.tick += 1
            self.clear_characters()
        else:
            self.clear_fruit()
            self.draw_pellets()
            self.draw_characters()
            self.display_text("R E A D Y !")
            pygame.display.update()

            events = pygame.event.get()
            keys = [pygame.K_RIGHT, 0, pygame.K_LEFT, 0]
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in keys:
                        self.player.direction = keys.index(event.key)
                        self.player.next_direction = keys.index(event.key)
                    self.wait = 0
                    self.clear_characters()
                    self.clear_text()
        return (time.time() - start_time) * 1000

    def check_collisions(self):
        for ghost in self.ghosts:
            if not ghost.dead:
                if ghost.get_tile_x() == self.player.get_tile_x():
                    if ghost.get_tile_y() == self.player.get_tile_y():
                        if ghost.state == constants.GhostState.FRIGHTENED:
                            self.score += 200 * self.combo
                            self.combo *= 2
                            self.update_caption()
                            ghost.dead = True
                            ghost.update_target()
                        else:
                            self.player.die()
                            return True
        return False

    def next_level(self):
        if sum(1 for i in self.map.get_pellets()) == 0:
            self.initialize_level()
            return True
        return False

    def change_ghost_states(self):
        if self.player.fright > 0:
            self.player.fright -= 1
        else:
            if any(g for g in self.ghosts if g.state == constants.GhostState.FRIGHTENED):
                for ghost in self.ghosts:
                    ghost.change_state(self.previous_ghosts_state)
            cycle_times = constants.get_level_based_constant(self.level, constants.GHOST_MODE_CYCLE)
            second = self.tick / constants.TICKRATE - self.player.power_pellets * constants.get_level_based_constant(self.level, constants.FRIGHT_TIME)
            if second in cycle_times:
                cycle = cycle_times.index(second)
                new_state = constants.GhostState.SCATTER if cycle % 2 else constants.GhostState.CHASE
                self.previous_ghosts_state = new_state
                for ghost in self.ghosts:
                    ghost.change_state(new_state)

    def get_screen_width(self):
        return self.map.get_width()

    def get_screen_height(self):
        return self.map.get_height()

    def delay(self, time):
        pygame.time.wait(int(time))

    def draw_walls(self):
        ts = constants.TILE_SIZE
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
        self.barrier.draw()
        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()

    def clear_characters(self):
        self.barrier.clear()
        self.player.clear()
        for ghost in self.ghosts:
            ghost.clear()

    def spawn_fruit(self):
        pellets = sum(1 for i in self.map.get_pellets())
        if (self.map.total_pellets - pellets) in constants.FRUIT_SPAWN:
            self.fruit = random.randint(9 * constants.TICKRATE, 10 * constants.TICKRATE)

    def draw_fruit(self):
        if self.fruit > 0:
            fruit_location = self.map.get_coordinates('f')
            fruit_image_col = constants.get_level_based_constant(self.level, constants.FRUITS)[0]
            offset = constants.TILE_SIZE / 2 - constants.SPRITE_SHEET_SPRITE_SIZE / 2
            self.window.blit(
                self.sprite_sheet.get_image_at(fruit_image_col, constants.FRUIT_IMAGE_ROW),
                ((fruit_location[0] + 0.5) * constants.TILE_SIZE + offset, fruit_location[1] * constants.TILE_SIZE + offset))
            self.fruit -= 1

    def clear_fruit(self):
        fruit_location = self.map.get_coordinates('f')
        offset = constants.TILE_SIZE / 2 - constants.SPRITE_SHEET_SPRITE_SIZE / 2
        if self.fruit == 0:
            sprite_size = self.sprite_sheet.sprite_size
            pygame.draw.rect(self.window, constants.BACKGROUND_COLOR,
                             ((fruit_location[0] + 0.5) * constants.TILE_SIZE + offset,
                              fruit_location[1] * constants.TILE_SIZE + offset, sprite_size, sprite_size))

    def draw_pellets(self):
        ts = constants.TILE_SIZE
        size = ts / 8
        offset = ts / 2 - size / 2

        for pellet in self.map.get_pellets():
            if pellet[2] == '.':
                pygame.draw.rect(self.window, constants.PELLET_COLOR,
                                 (pellet[0] * ts + offset, pellet[1] * ts + offset, size, size))
            elif pellet[2] == 'o':
                pygame.draw.circle(self.window, constants.PELLET_COLOR,
                                   (int((pellet[0] + 0.5) * ts), int((pellet[1] + 0.5) * ts)), int(size * 2))
