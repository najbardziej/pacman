# pylint: disable=no-member
import pygame
from game_files import constants, Character, Game, drawhelper


def modify_position(coordinates, direction, delta):
    current_x, current_y = coordinates
    (new_x, new_y) = {
        0: lambda x, y: (x + delta, y),  # RIGHT
        1: lambda x, y: (x, y - delta),  # UP
        2: lambda x, y: (x - delta, y),  # LEFT
        3: lambda x, y: (x, y + delta),  # DOWN
    }[direction](current_x, current_y)
    return new_x, new_y


class Player(Character.Character):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y)
        self.fright = 0
        self.power_pellets = 0
        self.direction = constants.RIGHT
        self.next_direction = constants.RIGHT
        self.speed = 0

    def eat(self):
        if 0 < self.x < constants.GAMEMAP_WIDTH_PX:
            if self.get_distance_to_tile_center() <= self.speed:
                points = self.game.map.remove_pellet(self.get_tile_x(), self.get_tile_y())
                if points == 50:
                    self.power_pellets += 1
                    self.game.combo = 1
                    fright_time_s = constants.get_level_based_constant(self.game.level, constants.FRIGHT_TIME)
                    self.fright = fright_time_s * constants.TICKRATE
                    for ghost in self.game.ghosts.values():
                        ghost.change_state(constants.FRIGHTENED)
                if points:
                    self.game.score += points
                    self.game.update_caption()
                    pellets = sum(1 for i in self.game.map.get_pellets())
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
            if distance_to_center <= self.speed:
                self.x, self.y = modify_position((self.x, self.y),
                                                 self.direction,
                                                 distance_to_center)
                self.speed -= distance_to_center
                if self.direction != self.next_direction:
                    tile_x, tile_y = modify_position((self.get_tile_x(),
                                                      self.get_tile_y()),
                                                     self.next_direction,
                                                     1)
                    if self.game.map.get_tile(tile_x, tile_y) not in\
                            [constants.WALL, constants.BARRIER]:
                        self.direction = self.next_direction

                tile_x, tile_y = modify_position((self.get_tile_x(),
                                                  self.get_tile_y()),
                                                 self.direction,
                                                 1)
                if self.game.map.get_tile(tile_x, tile_y) == constants.WALL:
                    self.speed = 0

        self.x, self.y = modify_position((self.x, self.y),
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
        Game.Game.window.blit(
            pygame.transform.rotate(
                drawhelper.get_image_at(frame, constants.PLAYER_ROW),
                90 * self.direction),
            (self.x - constants.SPRITE_SIZE / 2,
             self.y - constants.SPRITE_SIZE / 2))

    def update_speed(self):
        index = 1 if self.fright == 0 else 0
        multiplier = constants.get_level_based_constant(self.game.level, constants.PACMAN_SPEED_MULTIPLIER)[index]
        self.speed = constants.BASE_SPEED * multiplier
