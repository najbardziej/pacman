"""Main module - controlling application and other objects"""
import dataclasses

import time
import random
import os
import pygame

from game_files import constants
from game_files import map as gamemap
from game_files import barrier
from game_files import drawhelper
from game_files import characters

os.environ['SDL_VIDEO_WINDOW_POS'] = "512, 32"


class Game:
    """Main class controlling the game"""
    WINDOW = pygame.display.set_mode((
        constants.GAMEMAP_WIDTH_PX, constants.GAMEMAP_HEIGHT_PX))
    SPRITE_SHEET = pygame.image.load(constants.SPRITE_SHEET).convert()
    MAP = gamemap.Map()
    barrier = barrier.Barrier(list(MAP.get_barriers()))

    def __init__(self):
        self.tick = 0
        self.level = 0
        self.score = 0
        self.player = None
        self.pellets = list(self.MAP.get_pellets())
        self.fruit = 0
        self.lives = 4
        self.combo = 1
        self.wait = 0
        self.ghosts = {}
        self.previous_ghosts_state = constants.SCATTER

    def initialize_level(self, next_level):
        """Initializing level after player death or to advance to new level"""
        player_x, player_y = self.MAP.get_coordinates('s')
        blinky_x, blinky_y = self.MAP.get_coordinates('b')
        pinky_x,  pinky_y  = self.MAP.get_coordinates('p')
        inky_x,   inky_y   = self.MAP.get_coordinates('i')
        clyde_x,  clyde_y  = self.MAP.get_coordinates('c')
        self.player = characters.Player(player_x, player_y)
        self.ghosts = {
            "blinky": characters.Blinky(blinky_x, blinky_y),
            "pinky":  characters.Pinky(pinky_x, pinky_y),
            "inky":   characters.Inky(inky_x, inky_y),
            "clyde":  characters.Clyde(clyde_x, clyde_y),
        }
        for ghost in self.ghosts.values():
            ghost.state = self.previous_ghosts_state
        self.combo = 1
        self.fruit = 0
        self.update_caption()
        self.wait = 1
        if next_level:
            self.pellets = list(self.MAP.get_pellets())
            self.draw_walls()
            self.draw_pellets()
            self.level += 1
            self.tick = 0
        else:
            self.lives -= 1
            if self.lives == 0:
                drawhelper.draw_text("GAME OVER!")
                pygame.display.update()
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            return

    def update_caption(self):
        """Updates caption shown on Application bar"""
        pygame.display.set_caption(f"Pacman level: {self.level} "
                                   f"score: {self.score} "
                                   f"lives: {self.lives}")

    def remove_pellet(self, tile_x, tile_y):
        """Removes the pellet from given location and returns the value of it"""
        try:
            tile = next(t for t in self.pellets
                        if t.x == tile_x and t.y == tile_y)
            if tile.cell in [constants.PELLET, constants.PELLET2]:
                del self.pellets[self.pellets.index(tile)]
                return 10
            if tile.cell == constants.POWER_PELLET:
                del self.pellets[self.pellets.index(tile)]
                return 50
            return False
        except StopIteration:
            return False

    def step(self):
        """Step method - executed once every frame"""
        start_time = time.time()
        if not self.wait:
            if self.player.eat(
                    self,
                    self.remove_pellet(self.player.get_tile_x(),
                                       self.player.get_tile_y())):

                self.spawn_fruit()
                if self.next_level():
                    return (time.time() - start_time) * 1000
            else:
                self.player.move(self.level)
            self.change_ghost_states()
            if self.check_collisions():
                return (time.time() - start_time) * 1000
            for ghost in self.ghosts.values():
                ghost.move(self.player,
                           self.ghosts,
                           len(self.pellets),
                           self.previous_ghosts_state,
                           self.level)
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
            drawhelper.draw_text("R E A D Y !")
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
                    drawhelper.clear_text()
        return (time.time() - start_time) * 1000

    def check_collisions(self):
        """Check for collisions of player with any of the ghosts"""
        for ghost in self.ghosts.values():
            if not ghost.dead:
                if ghost.get_tile_x() == self.player.get_tile_x():
                    if ghost.get_tile_y() == self.player.get_tile_y():
                        if ghost.state == constants.FRIGHTENED:
                            self.score += 200 * self.combo
                            self.combo *= 2
                            self.update_caption()
                            ghost.dead = True
                            ghost.update_target(self.player, self.ghosts)
                        else:
                            self.initialize_level(False)
                            return True
        return False

    def next_level(self):
        """Checks if no pellets are left and moves to next level"""
        if len(self.pellets) == 0:
            self.initialize_level(True)
            return True
        return False

    def change_ghost_states(self):
        """Operates the ghost state cycle rotation"""
        if self.player.fright > 0:
            self.player.fright -= 1
        else:
            if any(g for g in self.ghosts.values()
                   if g.state == constants.FRIGHTENED):
                for ghost in self.ghosts.values():
                    ghost.change_state(self.previous_ghosts_state)
            cycle_times = constants.get_level_based_constant(
                self.level, constants.GHOST_MODE_CYCLE)
            second = self.tick / constants.TICKRATE - \
                     self.player.power_pellets * \
                     constants.get_level_based_constant(self.level,
                                                        constants.FRIGHT_TIME)
            if second in cycle_times:
                cycle = cycle_times.index(second)
                new_state = constants.SCATTER if cycle % 2 else constants.CHASE
                self.previous_ghosts_state = new_state
                for ghost in self.ghosts.values():
                    ghost.change_state(new_state)

    def draw_walls(self):
        """Draws all the map walls depending on wall types"""
        for wall_x, wall_y, wall_type in self.MAP.get_walls():
            {
                0: lambda x, y: drawhelper.draw_arc(x + .5, y + .5, 1 / 2, 1),
                1: lambda x, y: drawhelper.draw_arc(x - .5, y + .5, 0, 1 / 2),
                2: lambda x, y: drawhelper.draw_arc(x - .5, y - .5, 3 / 2, 0),
                3: lambda x, y: drawhelper.draw_arc(x + .5, y - .5, 1, 3 / 2),
                4: lambda x, y: drawhelper.draw_line(x + .5, y, x + .5, y + 1),
                5: lambda x, y: drawhelper.draw_line(x, y + .5, x + 1, y + .5),
            }[wall_type](wall_x, wall_y)
        pygame.display.update()

    def draw_characters(self):
        """Draws barrier, player and all the ghosts"""
        self.barrier.draw()
        self.player.draw(self.tick)
        for ghost in self.ghosts.values():
            ghost.draw(self.tick, self.player.fright)

    def clear_characters(self):
        """Clears barrier, player and all the ghosts"""
        self.barrier.clear()
        self.player.clear()
        for ghost in self.ghosts.values():
            ghost.clear()

    def spawn_fruit(self):
        """Spawn fruits when enough pellets are eaten"""
        pellets = len(self.pellets)
        if self.MAP.total_pellets - pellets in constants.FRUIT_SPAWN:
            self.fruit = random.randint(
                9 * constants.TICKRATE, 10 * constants.TICKRATE)

    def draw_fruit(self):
        """Draws fruit on game window"""
        if self.fruit > 0:
            fruit_x, fruit_y = self.MAP.get_coordinates('f')
            fruit_image_col = constants.get_level_based_constant(
                self.level, constants.FRUITS)[0]
            offset = constants.TILE_SIZE / 2 - constants.SPRITE_SIZE / 2
            self.WINDOW.blit(
                drawhelper.get_image_at(fruit_image_col,
                                        constants.FRUIT_IMAGE_ROW),
                ((fruit_x + 0.5) * constants.TILE_SIZE + offset,
                 fruit_y * constants.TILE_SIZE + offset))
            self.fruit -= 1
            if self.fruit == 0:
                self.clear_fruit()

    def clear_fruit(self):
        """Clears fruit"""
        fruit_x, fruit_y = self.MAP.get_coordinates('f')
        offset = (constants.TILE_SIZE - constants.SPRITE_SIZE) / 2
        if self.fruit == 0:
            drawhelper.draw_rect(fruit_x + 0.5, fruit_y, constants.SPRITE_SIZE,
                                 offset=offset)

    def draw_pellets(self):
        """Draws all pellets"""
        tile_size = constants.TILE_SIZE
        size = tile_size / 8
        offset = tile_size / 2 - size / 2
        for pellet in self.pellets:
            pellet_x, pellet_y, pellet_type = dataclasses.astuple(pellet)
            if pellet_type in [constants.PELLET, constants.PELLET2]:
                drawhelper.draw_rect(pellet_x, pellet_y, size,
                                     offset=offset,
                                     color=constants.PELLET_COLOR)
            elif pellet_type == constants.POWER_PELLET:
                pygame.draw.circle(self.WINDOW, constants.PELLET_COLOR,
                                   (int((pellet_x + 0.5) * tile_size),
                                    int((pellet_y + 0.5) * tile_size)),
                                   int(size * 2))
