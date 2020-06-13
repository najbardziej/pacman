"""Module containing character classes - for player and all the ghosts"""
import random
import math
import pygame
from game_files import constants, game, drawhelper


def get_modified_position(coordinates, direction, delta):
    """Returns modified coortinates by given direction and value"""
    current_x, current_y = coordinates
    (new_x, new_y) = {
        0: lambda x, y: (x + delta, y),  # RIGHT
        1: lambda x, y: (x, y - delta),  # UP
        2: lambda x, y: (x - delta, y),  # LEFT
        3: lambda x, y: (x, y + delta),  # DOWN
    }[direction](current_x, current_y)
    return new_x, new_y


class Character:
    """Base class for Player and Ghost classes"""
    def __init__(self, tile_x, tile_y):
        self.direction = constants.RIGHT
        self.x = (tile_x + 1)   * constants.TILE_SIZE
        self.y = (tile_y + 0.5) * constants.TILE_SIZE

    def clear(self):
        """Clears character in game window"""
        pygame.draw.rect(game.Game.WINDOW,
                         constants.BACKGROUND_COLOR,
                         (self.x - constants.SPRITE_SIZE / 2,
                          self.y - constants.SPRITE_SIZE / 2,
                          constants.SPRITE_SIZE,
                          constants.SPRITE_SIZE))

    def get_distance_to_tile_center(self, next_tile=False):
        """Returns distance to the center of tile

        If next_tile parameter is given
        returns distance to tile in front of character"""
        if next_tile:
            tile_x, tile_y = get_modified_position(
                (self.get_tile_x(), self.get_tile_y()), self.direction, 1)
        else:
            tile_x, tile_y = self.get_tile_x(), self.get_tile_y()
        tile_x_center = (tile_x + 0.5) * constants.TILE_SIZE
        tile_y_center = (tile_y + 0.5) * constants.TILE_SIZE
        return abs(tile_x_center - self.x) + abs(tile_y_center - self.y)

    def get_tile_x(self):
        """Returns current tile_x of character"""
        return self.x // constants.TILE_SIZE

    def get_tile_y(self):
        """Returns current tile_y of character"""
        return self.y // constants.TILE_SIZE


class Ghost(Character):
    """Base class for all the ghosts"""
    def __init__(self, tile_x, tile_y, image_row):
        super().__init__(tile_x, tile_y)
        self.image_row = image_row
        self.freeze = True
        self.in_base = True
        self.dead = False
        self.speed = 0
        self.home_corner = (0, 0)
        self.target = (0, 0)
        self.pellets_to_leave = 0
        self.state = constants.SCATTER

    def get_chase_target(self, player, ghosts):
        """Abstract method - implementations should return target coordinates"""
        raise NotImplementedError

    def update_target(self, player, ghosts):
        """Updates the target which ghost will follow"""
        if self.dead:
            self.target = game.Game.barrier.get_entrance()
        elif self.state == constants.CHASE:
            self.target = self.get_chase_target(player, ghosts)
        elif self.state == constants.SCATTER:
            self.target = self.home_corner

    def reverse_direction(self):
        """Reverse movement direction of ghost"""
        if not self.dead and not self.in_base:
            self.direction = (self.direction + 2) % 4

    def change_state(self, new_state):
        """Change ghost state to one passed with argument"""
        if self.state != constants.FRIGHTENED:
            self.reverse_direction()
        self.state = new_state

    def get_possible_directions(self):
        """Returns all possible directions at intersection with ratings"""
        possible_directions = []
        tile_x, tile_y = self.get_tile_x(), self.get_tile_y()
        tiles = [
            game.Game.MAP.get_tile(tile_x, tile_y - 1),
            game.Game.MAP.get_tile(tile_x - 1, tile_y),
            game.Game.MAP.get_tile(tile_x, tile_y + 1),
            game.Game.MAP.get_tile(tile_x + 1, tile_y),
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
            if game.Game.MAP.get_tile(tile_x, tile_y) in \
                    [constants.INTERSECTION, constants.INTERSECTION2]:
                if not self.dead:
                    del possible_directions[0]

        return possible_directions

    def get_distance_to_target(self, tile_x, tile_y):
        """Calculates and returns distance from given tile to the target"""
        return ((tile_x - self.target[0]) ** 2 +
                (tile_y - self.target[1]) ** 2) ** (1 / 2)

    def choose_direction(self, possible_directions):
        """Returns next direction based on ratings and current state"""
        if len(possible_directions) >= 2 or \
                (len(possible_directions) == 1 and
                 possible_directions[0] != self.direction):
            self.x = (self.get_tile_x() + 0.5) * constants.TILE_SIZE
            self.y = (self.get_tile_y() + 0.5) * constants.TILE_SIZE
            if self.state == constants.FRIGHTENED and not self.dead:
                return sorted(possible_directions,
                              key=lambda x: random.random())[0][0]
            return sorted(possible_directions,
                          key=lambda x: x[1])[0][0]
        return self.direction

    def leave_base(self):
        """Leads the ghosts out of the base"""
        self.target = game.Game.barrier.get_entrance()
        tile_size = constants.TILE_SIZE
        entrance_dx = abs(self.x - (self.target[0] + 0.5) * tile_size)
        entrance_dy = abs(self.y - (self.target[1] + 0.5) * tile_size)
        if entrance_dx <= self.speed / 2:
            if entrance_dy <= self.speed / 2:
                self.in_base = False
                self.target = self.home_corner
                self.direction = constants.LEFT
                game.Game.barrier.visible = True
            else:
                self.x = (self.target[0] + 0.5) * tile_size
                self.direction = constants.UP

    def move(self, player, ghosts, pellet_count, previous_ghosts_state, level):
        """Ghost movement mechanism"""
        self.update_speed(level)
        tile_size = constants.TILE_SIZE
        if not self.freeze:
            if self.in_base:
                self.leave_base()
            else:
                distance_to_center = self.get_distance_to_tile_center()
                distance_to_next_tile = self.get_distance_to_tile_center(
                    next_tile=True)

                if 0 < self.x < constants.GAMEMAP_WIDTH_PX:
                    if distance_to_center <= self.speed and \
                       distance_to_next_tile >= tile_size:
                        # Move to tile center
                        self.update_target(player, ghosts)
                        previous_direction = self.direction
                        self.direction = self.choose_direction(
                            self.get_possible_directions())
                        self.x, self.y = \
                            get_modified_position((self.x, self.y),
                                                  self.direction,
                                                  distance_to_center)
                        self.speed -= distance_to_center
                        if self.direction != previous_direction:
                            self.speed = 0

                    elif abs(distance_to_center - tile_size / 2) <= self.speed \
                            and self.dead:
                        # Move to base if dead
                        tile_x, tile_y = self.get_tile_x(), self.get_tile_y()
                        entrance  = game.Game.barrier.get_entrance()
                        spawn     = game.Game.barrier.get_spawn()
                        sign = math.copysign(
                            1, self.x % tile_size - tile_size / 2)
                        if (tile_x + sign * 0.5, tile_y) == entrance:
                            self.direction = constants.DOWN
                            game.Game.barrier.visible = False
                        if (tile_x + sign * 0.5, tile_y) == spawn:
                            self.dead = False
                            self.in_base = True
                            self.state = previous_ghosts_state

            self.x, self.y = get_modified_position((self.x, self.y),
                                                   self.direction,
                                                   self.speed)

            if self.x <= -1 * constants.TILE_SIZE / 2:
                self.x = constants.GAMEMAP_WIDTH_PX + constants.TILE_SIZE / 2
            elif self.x >= constants.GAMEMAP_WIDTH_PX + constants.TILE_SIZE / 2:
                self.x = -1 * constants.TILE_SIZE / 2
        else:
            self.unfreeze(pellet_count)

    def unfreeze(self, pellet_count):
        """Allow the ghost to move if enough pellets are eaten"""
        if pellet_count <= game.Game.MAP.total_pellets - self.pellets_to_leave:
            game.Game.barrier.visible = False
            self.freeze = False

    def draw(self, tick, player_fright):
        """Draw ghost animation"""
        sprite_size = constants.SPRITE_SIZE
        frame = 0 if self.freeze else int(tick * constants.ANIMATION_SPEED) % 2

        if self.dead:
            game.Game.WINDOW.blit(
                drawhelper.get_image_at(4 + self.direction, 5),
                (self.x - sprite_size / 2, self.y - sprite_size / 2))
        elif self.state == constants.FRIGHTENED:
            if player_fright <= 100:
                frame += int(tick * constants.ANIMATION_SPEED / 2) % 2 * 2
            game.Game.WINDOW.blit(
                drawhelper.get_image_at(frame, 5),
                (self.x - sprite_size / 2, self.y - sprite_size / 2))
        else:
            game.Game.WINDOW.blit(
                drawhelper.get_image_at(frame + self.direction * 2,
                                        self.image_row),
                (self.x - sprite_size / 2, self.y - sprite_size / 2))

    def update_speed(self, level):
        """Update speed of the ghost"""
        if game.Game.MAP.get_tile(self.get_tile_x(),
                                  self.get_tile_y()) == constants.TUNNEL:
            multiplier = constants.get_level_based_constant(
                level, constants.GHOST_SPEED_MULTIPLIER)[2]
        elif not self.dead and self.state == constants.FRIGHTENED:
            multiplier = constants.get_level_based_constant(
                level, constants.GHOST_SPEED_MULTIPLIER)[1]
        else:
            multiplier = constants.get_level_based_constant(
                level, constants.GHOST_SPEED_MULTIPLIER)[0]
        self.speed = constants.BASE_SPEED * multiplier


class Blinky(Ghost):
    """Blinky - The red ghost

    Blinky has an Elroy mode
    - moves faster when certain amount of pellets are eaten

    Targeting: Blinky follows the pacman directly.
    """
    def __init__(self, tile_x, tile_y):
        super().__init__(tile_x, tile_y, constants.BLINKY_ROW)
        self.freeze = False
        self.in_base = False
        self.home_corner = (24, -3)
        self.target = (24, -3)
        self.elroy = 0

    def get_chase_target(self, player, ghosts):
        return player.get_tile_x(), player.get_tile_y()

    def update_speed(self, level):
        tile_x, tile_y = self.get_tile_x(), self.get_tile_y()
        if game.Game.MAP.get_tile(tile_x, tile_y) == constants.TUNNEL:
            multiplier = constants.get_level_based_constant(
                level, constants.GHOST_SPEED_MULTIPLIER)[2]
        elif not self.dead and self.state == constants.FRIGHTENED:
            multiplier = constants.get_level_based_constant(
                level, constants.GHOST_SPEED_MULTIPLIER)[1]
        elif self.elroy == 1:
            multiplier = constants.get_level_based_constant(
                level, constants.ELROY_SPEED_MULTIPLIER)[0][1]
        elif self.elroy == 2:
            multiplier = constants.get_level_based_constant(
                level, constants.ELROY_SPEED_MULTIPLIER)[1][1]
        else:
            multiplier = constants.get_level_based_constant(
                level, constants.GHOST_SPEED_MULTIPLIER)[0]
        self.speed = constants.BASE_SPEED * multiplier


class Inky(Ghost):
    """Inky - The blue ghost

    Inky leaves spawn if 30 pellets are eaten

    Targeting: Inky follows the tile pointed by doubled vector
        drawn from Blinky to Pacman
    """
    def __init__(self, tile_x, tile_y):
        super().__init__(tile_x, tile_y, constants.INKY_ROW)
        self.home_corner = (27, 33)
        self.pellets_to_leave = 30

    def get_chase_target(self, player, ghosts):
        dx, dy = get_modified_position((0, 0), player.direction, 2)
        blinky = ghosts["blinky"]
        dx = 2 * (player.get_tile_x() + dx - blinky.get_tile_x())
        dy = 2 * (player.get_tile_y() + dy - blinky.get_tile_y())

        return blinky.get_tile_x() + dx, blinky.get_tile_y() + dy


class Pinky(Ghost):
    """Pinky - The pink ghost

    Targeting: Pinky follows location 4 tiles ahead of the Pacman.
    """
    def __init__(self, tile_x, tile_y):
        super().__init__(tile_x, tile_y, constants.PINKY_ROW)
        self.direction = constants.UP
        self.freeze = False
        self.home_corner = (3, -3)

    def get_chase_target(self, player, ghosts):
        tile_x = player.get_tile_x()
        tile_y = player.get_tile_y()

        return get_modified_position((tile_x, tile_y), player.direction, 4)


class Clyde(Ghost):
    """Clyde - The orange ghost

        Clyde leaves spawn if 60 pellets are eaten

        Targeting: Clyde follows the Pacman directly
            if distance to Pacman is greater than 8 tiles.
            If else - he follows his home corner.
    """
    def __init__(self, tile_x, tile_y):
        super().__init__(tile_x, tile_y, constants.CLYDE_ROW)
        self.direction = constants.LEFT
        self.home_corner = (0, 33)
        self.pellets_to_leave = 60

    def get_chase_target(self, player, ghosts):
        self.target = (player.get_tile_x(), player.get_tile_y())
        tile_x, tile_y = self.get_tile_x(), self.get_tile_y()
        if self.get_distance_to_target(tile_x, tile_y) < 8:
            return self.home_corner
        return self.target


class Player(Character):
    """Player - the Pacman"""
    def __init__(self, tile_x, tile_y):
        super().__init__(tile_x, tile_y)
        self.fright = 0
        self.power_pellets = 0
        self.next_direction = constants.RIGHT
        self.speed = 0

    def eat(self, game_obj, points):
        """Mechanics for eating pellets and fruits"""
        if points == 50:
            self.power_pellets += 1
            game.combo = 1
            fright_time_s = constants.get_level_based_constant(
                game_obj.level, constants.FRIGHT_TIME)
            self.fright = fright_time_s * constants.TICKRATE
            for ghost in game_obj.ghosts.values():
                ghost.change_state(constants.FRIGHTENED)
        if points:
            game_obj.score += points
            game_obj.update_caption()
            pellets = len(game_obj.pellets)
            pellets_to_elroy2 = constants.get_level_based_constant(
                game_obj.level, constants.ELROY_SPEED_MULTIPLIER)[1][0]
            pellets_to_elroy1 = constants.get_level_based_constant(
                game_obj.level, constants.ELROY_SPEED_MULTIPLIER)[0][0]
            if pellets <= pellets_to_elroy2:
                game_obj.ghosts["blinky"].elroy = 2
            elif pellets <= pellets_to_elroy1:
                game_obj.ghosts["blinky"].elroy = 1
            return True
        if game_obj.fruit > 0:
            fruit_x, fruit_y = game.Game.MAP.get_coordinates('f')
            if self.get_tile_x() in [fruit_x, fruit_x + 1]:
                if self.get_tile_y() == fruit_y:
                    game_obj.score += \
                        constants.get_level_based_constant(
                            game_obj.level, constants.FRUITS)[2]
                    game_obj.fruit = 0
                    game_obj.clear_fruit()
                    game_obj.update_caption()
        return False

    def move(self, level):
        """Player movement mechanism"""
        events = pygame.event.get()
        keys = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in keys:
                    self.next_direction = keys.index(event.key)

        self.update_speed(level)
        distance_to_center = self.get_distance_to_tile_center()
        distance_to_next_tile = self.get_distance_to_tile_center(next_tile=True)

        if 0 < self.x < constants.GAMEMAP_WIDTH_PX:
            if distance_to_center <= self.speed and \
               distance_to_next_tile >= constants.TILE_SIZE:
                self.x, self.y = get_modified_position((self.x, self.y),
                                                       self.direction,
                                                       distance_to_center)
                self.speed -= distance_to_center
                if self.direction != self.next_direction:
                    tile_x, tile_y = get_modified_position((self.get_tile_x(),
                                                            self.get_tile_y()),
                                                           self.next_direction,
                                                           1)
                    if game.Game.MAP.get_tile(tile_x, tile_y) not in\
                            [constants.WALL, constants.BARRIER]:
                        self.direction = self.next_direction

                tile_x, tile_y = get_modified_position((self.get_tile_x(),
                                                        self.get_tile_y()),
                                                       self.direction,
                                                       1)
                if game.Game.MAP.get_tile(tile_x, tile_y) == constants.WALL:
                    self.speed = 0

        self.x, self.y = get_modified_position((self.x, self.y),
                                               self.direction,
                                               self.speed)

        if self.x <= -constants.TILE_SIZE / 2:
            self.x = constants.GAMEMAP_WIDTH_PX + constants.TILE_SIZE / 2
        elif self.x >= constants.GAMEMAP_WIDTH_PX + constants.TILE_SIZE / 2:
            self.x = -constants.TILE_SIZE / 2

    def draw(self, tick):
        """Draws player animation"""
        frame = int(tick * constants.ANIMATION_SPEED) % 4
        if frame == 3:
            frame = 2
        game.Game.WINDOW.blit(
            pygame.transform.rotate(
                drawhelper.get_image_at(frame, constants.PLAYER_ROW),
                90 * self.direction),
            (self.x - constants.SPRITE_SIZE / 2,
             self.y - constants.SPRITE_SIZE / 2))

    def update_speed(self, level):
        """Updates player speed"""
        index = 1 if self.fright == 0 else 0
        multiplier = constants.get_level_based_constant(
            level, constants.PACMAN_SPEED_MULTIPLIER)[index]
        self.speed = constants.BASE_SPEED * multiplier
