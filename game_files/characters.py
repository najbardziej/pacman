# pylint: disable=bad-whitespace
import random
import math
import pygame
from game_files import constants, game, drawhelper


def get_modified_position(coordinates, direction, delta):
    current_x, current_y = coordinates
    (new_x, new_y) = {
        0: lambda x, y: (x + delta, y),  # RIGHT
        1: lambda x, y: (x, y - delta),  # UP
        2: lambda x, y: (x - delta, y),  # LEFT
        3: lambda x, y: (x, y + delta),  # DOWN
    }[direction](current_x, current_y)
    return new_x, new_y


class Character:
    def __init__(self, game, tile_x, tile_y):
        self.game = game
        self.x = (tile_x + 1) * constants.TILE_SIZE
        self.y = (tile_y + 0.5) * constants.TILE_SIZE

    def clear(self):
        pygame.draw.rect(game.Game.window,
                         constants.BACKGROUND_COLOR,
                         (self.x - constants.SPRITE_SIZE / 2,
                          self.y - constants.SPRITE_SIZE / 2,
                          constants.SPRITE_SIZE,
                          constants.SPRITE_SIZE))

    def get_tile_x(self):
        return self.x // constants.TILE_SIZE

    def get_tile_y(self):
        return self.y // constants.TILE_SIZE


class Ghost(Character):
    def __init__(self, game, tile_x, tile_y, image_row):
        super().__init__(game, tile_x, tile_y)
        self.image_row = image_row
        self.direction = constants.RIGHT
        self.freeze = True
        self.in_base = True
        self.dead = False
        self.speed = 0
        self.home_corner = (0, 0)
        self.target = (0, 0)
        self.pellets_to_leave = 0
        self.state = constants.SCATTER

    def get_chase_target(self):
        raise NotImplementedError

    def update_target(self):
        if self.dead:
            self.target = self.game.barrier.get_entrance()
        elif self.state == constants.CHASE:
            self.target = self.get_chase_target()
        elif self.state == constants.SCATTER:
            self.target = self.home_corner

    def reverse_direction(self):
        if not self.dead and not self.in_base:
            self.direction = (self.direction + 2) % 4

    def change_state(self, new_state):
        if self.state != constants.FRIGHTENED:
            self.reverse_direction()
        self.state = new_state

    def get_possible_directions(self):
        possible_directions = []
        tile_x, tile_y = self.get_tile_x(), self.get_tile_y()
        tiles = [
            self.game.map.get_tile(tile_x, tile_y - 1),
            self.game.map.get_tile(tile_x - 1, tile_y),
            self.game.map.get_tile(tile_x, tile_y + 1),
            self.game.map.get_tile(tile_x + 1, tile_y),
        ]
        distances = [
            self.get_distance_to_target(tile_x, tile_y - 1),
            self.get_distance_to_target(tile_x - 1, tile_y),
            self.get_distance_to_target(tile_x, tile_y + 1),
            self.get_distance_to_target(tile_x + 1, tile_y),
        ]
        directions = [1, 2, 3, 0]  # up, left, down, right - tiebreaker
        for tile, distance, direction in zip(tiles, distances, directions):
            if tile not in [constants.WALL, constants.BARRIER]:
                if self.direction != (direction + 2) % 4:
                    possible_directions.append((direction, distance))

        if possible_directions[0][0] == constants.UP:
            if self.game.map.get_tile(tile_x, tile_y) in \
                    [constants.INTERSECTION, constants.INTERSECTION2]:
                if not self.dead:
                    del possible_directions[0]

        return possible_directions

    def get_distance_to_target(self, tile_x, tile_y):
        return ((tile_x - self.target[0]) ** 2 +
                (tile_y - self.target[1]) ** 2) ** (1 / 2)

    def move(self):
        if not self.freeze:
            if self.in_base:
                self.target = self.game.barrier.get_entrance()
                if abs(self.x - self.target[0] * constants.TILE_SIZE - constants.TILE_SIZE / 2) <= self.speed / 2:
                    if abs(self.y - self.target[1] * constants.TILE_SIZE - constants.TILE_SIZE / 2) <= self.speed / 2:
                        self.in_base = False
                        self.target = self.home_corner
                        self.direction = constants.LEFT
                        self.game.barrier.visible = True
                    else:
                        self.x = self.target[0] * constants.TILE_SIZE + constants.TILE_SIZE / 2
                        self.direction = constants.UP
            else:
                if 0 < self.x < constants.GAMEMAP_WIDTH_PX:
                    if abs((self.y % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                        if abs((self.x % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                            self.update_target()
                            possible_directions = self.get_possible_directions()
                            if len(possible_directions) >= 2 or \
                                    (len(possible_directions) == 1 and possible_directions[0] != self.direction):
                                self.x = (self.get_tile_x() + 0.5) * constants.TILE_SIZE
                                self.y = (self.get_tile_y() + 0.5) * constants.TILE_SIZE
                                if self.state == constants.FRIGHTENED and not self.dead:
                                    self.direction = sorted(possible_directions, key=lambda x: random.random())[0][0]
                                else:
                                    self.direction = sorted(possible_directions, key=lambda x: x[1])[0][0]
                        if self.dead and abs((self.x + self.speed / 2) % constants.TILE_SIZE) <= self.speed:
                            sign = math.copysign(1, (self.x % constants.TILE_SIZE - constants.TILE_SIZE / 2))
                            if self.game.barrier.get_entrance() == (self.get_tile_x() + sign * 0.5, self.get_tile_y()):
                                self.direction = constants.DOWN
                                self.game.barrier.visible = False
                            if self.game.barrier.get_spawn() == (self.get_tile_x() + sign * 0.5, self.get_tile_y()):
                                self.dead = False
                                self.in_base = True
                                self.state = self.game.previous_ghosts_state

            self.update_speed()
            (self.x, self.y) = {
                0: lambda x, y: (x + self.speed, y),  # RIGHT
                1: lambda x, y: (x, y - self.speed),  # UP
                2: lambda x, y: (x - self.speed, y),  # LEFT
                3: lambda x, y: (x, y + self.speed)   # DOWN
            }[self.direction](self.x, self.y)

            if self.x <= -1 * constants.TILE_SIZE / 2:
                self.x = constants.GAMEMAP_WIDTH_PX + constants.TILE_SIZE / 2
            elif self.x >= constants.GAMEMAP_WIDTH_PX + constants.TILE_SIZE / 2:
                self.x = -1 * constants.TILE_SIZE / 2
        else:
            self.unfreeze()

    def unfreeze(self):
        pellets = sum(1 for i in self.game.pellets)
        if pellets <= self.game.map.total_pellets - self.pellets_to_leave:
            self.game.barrier.visible = False
            self.freeze = False

    def draw(self):
        sprite_size = constants.SPRITE_SIZE
        if not self.freeze:
            frame = int(self.game.tick * constants.ANIMATION_SPEED) % 2
        else:
            frame = 0

        if self.dead:
            game.Game.window.blit(
                drawhelper.get_image_at(4 + self.direction, 5),
                (self.x - sprite_size / 2, self.y - sprite_size / 2))
        elif self.state == constants.FRIGHTENED:
            if self.game.player.fright <= 100:
                frame += int(self.game.tick * constants.ANIMATION_SPEED / 2) % 2 * 2
            game.Game.window.blit(
                drawhelper.get_image_at(frame, 5),
                (self.x - sprite_size / 2, self.y - sprite_size / 2))
        else:
            game.Game.window.blit(
                drawhelper.get_image_at(frame + self.direction * 2, self.image_row),
                (self.x - sprite_size / 2, self.y - sprite_size / 2))

    def update_speed(self):
        if self.game.map.get_tile(self.get_tile_x(), self.get_tile_y()) == constants.TUNNEL:
            multiplier = constants.get_level_based_constant(self.game.level, constants.GHOST_SPEED_MULTIPLIER)[2]
        elif not self.dead and self.state == constants.FRIGHTENED:
            multiplier = constants.get_level_based_constant(self.game.level, constants.GHOST_SPEED_MULTIPLIER)[1]
        else:
            multiplier = constants.get_level_based_constant(self.game.level, constants.GHOST_SPEED_MULTIPLIER)[0]
        self.speed = constants.BASE_SPEED * multiplier


class Blinky(Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.BLINKY_ROW)
        self.freeze = False
        self.in_base = False
        self.home_corner = (24, -3)
        self.target = (24, -3)
        self.elroy = 0

    def get_chase_target(self):
        return self.game.player.get_tile_x(), self.game.player.get_tile_y()

    def update_speed(self):
        if self.game.map.get_tile(self.get_tile_x(), self.get_tile_y()) == constants.TUNNEL:
            multiplier = constants.get_level_based_constant(
                self.game.level, constants.GHOST_SPEED_MULTIPLIER)[2]
        elif not self.dead and self.state == constants.FRIGHTENED:
            multiplier = constants.get_level_based_constant(
                self.game.level, constants.GHOST_SPEED_MULTIPLIER)[1]
        elif self.elroy == 1:
            multiplier = constants.get_level_based_constant(
                self.game.level, constants.ELROY_SPEED_MULTIPLIER)[0][1]
        elif self.elroy == 2:
            multiplier = constants.get_level_based_constant(
                self.game.level, constants.ELROY_SPEED_MULTIPLIER)[1][1]
        else:
            multiplier = constants.get_level_based_constant(
                self.game.level, constants.GHOST_SPEED_MULTIPLIER)[0]
        self.speed = constants.BASE_SPEED * multiplier


class Inky(Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.INKY_ROW)
        self.home_corner = (27, 33)
        self.pellets_to_leave = 30

    def get_chase_target(self):
        (dx, dy) = {
            0: lambda: (2,  0),  # RIGHT
            1: lambda: (0, -2),  # UP
            2: lambda: (-2, 0),  # LEFT
            3: lambda: (0,  2),  # DOWN
        }[self.game.player.direction]()

        player = self.game.player
        blinky = self.game.ghosts["blinky"]
        dx = 2 * (player.get_tile_x() + dx - blinky.get_tile_x())
        dy = 2 * (player.get_tile_y() + dy - blinky.get_tile_y())

        return blinky.get_tile_x() + dx, blinky.get_tile_y() + dy


class Pinky(Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.PINKY_ROW)
        self.direction = constants.UP
        self.freeze = False
        self.home_corner = (3, -3)

    def get_chase_target(self):
        tile_x = self.game.player.get_tile_x()
        tile_y = self.game.player.get_tile_y()

        return {
            0: lambda x, y: (x + 4, y),  # RIGHT
            1: lambda x, y: (x, y - 4),  # UP
            2: lambda x, y: (x - 4, y),  # LEFT
            3: lambda x, y: (x, y + 4),  # DOWN
        }[self.game.player.direction](tile_x, tile_y)


class Clyde(Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.CLYDE_ROW)
        self.direction = constants.LEFT
        self.home_corner = (0, 33)
        self.pellets_to_leave = 60

    def get_chase_target(self):
        player = self.game.player
        self.target = (player.get_tile_x(), player.get_tile_y())
        if self.get_distance_to_target(self.get_tile_x(), self.get_tile_y()) < 8:
            return self.home_corner
        return self.target


class Player(Character):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y)
        self.fright = 0
        self.power_pellets = 0
        self.direction = constants.RIGHT
        self.next_direction = constants.RIGHT
        self.speed = 0

    def eat(self, points):
        if points == 50:
            self.power_pellets += 1
            self.game.combo = 1
            fright_time_s = constants.get_level_based_constant(
                self.game.level, constants.FRIGHT_TIME)
            self.fright = fright_time_s * constants.TICKRATE
            for ghost in self.game.ghosts.values():
                ghost.change_state(constants.FRIGHTENED)
        if points:
            self.game.score += points
            self.game.update_caption()
            pellets = sum(1 for i in self.game.pellets)
            pellets_to_elroy2 = constants.get_level_based_constant(
                self.game.level, constants.ELROY_SPEED_MULTIPLIER)[1][0]
            pellets_to_elroy1 = constants.get_level_based_constant(
                self.game.level, constants.ELROY_SPEED_MULTIPLIER)[0][0]
            if pellets <= pellets_to_elroy2:
                self.game.ghosts["blinky"].elroy = 2
            elif pellets <= pellets_to_elroy1:
                self.game.ghosts["blinky"].elroy = 1
            return True
        if self.game.fruit > 0:
            fruit_x, fruit_y = self.game.map.get_coordinates('f')
            if self.get_tile_x() in [fruit_x, fruit_x + 1]:
                if self.get_tile_y() == fruit_y:
                    self.game.score += \
                        constants.get_level_based_constant(
                            self.game.level, constants.FRUITS)[2]
                    self.game.fruit = 0
                    self.game.clear_fruit()
                    self.game.update_caption()
        return False

    def get_distance_to_tile_center(self):
        tile_x_center = (self.get_tile_x() + 1/2) * constants.TILE_SIZE
        tile_y_center = (self.get_tile_y() + 1/2) * constants.TILE_SIZE
        return abs(tile_x_center - self.x) + abs(tile_y_center - self.y)

    def move(self):
        events = pygame.event.get()
        keys = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in keys:
                    self.next_direction = keys.index(event.key)

        self.update_speed()
        distance_to_center = self.get_distance_to_tile_center()

        if 0 < self.x < constants.GAMEMAP_WIDTH_PX:
            if distance_to_center < self.speed:
                self.x, self.y = get_modified_position((self.x, self.y),
                                                       self.direction,
                                                       distance_to_center)
                self.speed -= distance_to_center
                if self.direction != self.next_direction:
                    tile_x, tile_y = get_modified_position((self.get_tile_x(),
                                                            self.get_tile_y()),
                                                           self.next_direction,
                                                           1)
                    if self.game.map.get_tile(tile_x, tile_y) not in\
                            [constants.WALL, constants.BARRIER]:
                        self.direction = self.next_direction

                tile_x, tile_y = get_modified_position((self.get_tile_x(),
                                                        self.get_tile_y()),
                                                       self.direction,
                                                       1)
                if self.game.map.get_tile(tile_x, tile_y) == constants.WALL:
                    self.speed = 0

        self.x, self.y = get_modified_position((self.x, self.y),
                                               self.direction,
                                               self.speed)

        if self.x <= -constants.TILE_SIZE / 2:
            self.x = constants.GAMEMAP_WIDTH_PX + constants.TILE_SIZE / 2
        elif self.x >= constants.GAMEMAP_WIDTH_PX + constants.TILE_SIZE / 2:
            self.x = -constants.TILE_SIZE / 2

    def draw(self):
        frame = int(self.game.tick * constants.ANIMATION_SPEED) % 4
        if frame == 3:
            frame = 2
        game.Game.window.blit(
            pygame.transform.rotate(
                drawhelper.get_image_at(frame, constants.PLAYER_ROW),
                90 * self.direction),
            (self.x - constants.SPRITE_SIZE / 2,
             self.y - constants.SPRITE_SIZE / 2))

    def update_speed(self):
        index = 1 if self.fright == 0 else 0
        multiplier = constants.get_level_based_constant(
            self.game.level, constants.PACMAN_SPEED_MULTIPLIER)[index]
        self.speed = constants.BASE_SPEED * multiplier
