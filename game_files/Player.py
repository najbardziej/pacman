import pygame
from game_files import constants, Character


class Player(Character.Character):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y)
        self.fright = 0
        self.power_pellets = 0
        self.direction = constants.RIGHT
        self.next_direction = constants.RIGHT
        self.speed = 0

    def eat(self):
        if 0 < self.x < self.game.map.get_width():
            if abs((self.x % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                if abs((self.y % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:

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
                        fruit_location = self.game.map.get_coordinates('f')
                        if self.get_tile_x() in [fruit_location[0], fruit_location[0] + 1]:
                            if self.get_tile_y() == fruit_location[1]:
                                self.game.score += constants.get_level_based_constant(
                                    self.game.level, constants.FRUITS)[2]
                                self.game.fruit = 0
                                self.game.clear_fruit()
                                self.game.update_caption()
        return False

    def move(self):
        events = pygame.event.get()
        keys = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in keys:
                    self.next_direction = keys.index(event.key)

        self.update_speed()

        if 0 < self.x < self.game.map.get_width():
            if abs((self.x % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                if abs((self.y % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                    if self.direction != self.next_direction:
                        (tile_x, tile_y) = {
                            0: lambda x, y: (x + 1, y),  # RIGHT
                            1: lambda x, y: (x, y - 1),  # UP
                            2: lambda x, y: (x - 1, y),  # LEFT
                            3: lambda x, y: (x, y + 1)   # DOWN
                        }[self.next_direction](self.get_tile_x(), self.get_tile_y())
                        if self.game.map.get_tile(tile_x, tile_y) not in\
                                [constants.WALL, constants.BARRIER]:
                            self.x = (self.get_tile_x() + 0.5) * constants.TILE_SIZE
                            self.y = (self.get_tile_y() + 0.5) * constants.TILE_SIZE
                            self.direction = self.next_direction

                    (tile_x, tile_y) = {
                        0: lambda x, y: (x + 1, y),  # RIGHT
                        1: lambda x, y: (x, y - 1),  # UP
                        2: lambda x, y: (x - 1, y),  # LEFT
                        3: lambda x, y: (x, y + 1)   # DOWN
                    }[self.direction](self.get_tile_x(), self.get_tile_y())
                    if self.game.map.get_tile(tile_x, tile_y) == constants.WALL:
                        self.speed = 0

        (self.x, self.y) = {
            0: lambda x, y: (x + self.speed, y),  # RIGHT
            1: lambda x, y: (x, y - self.speed),  # UP
            2: lambda x, y: (x - self.speed, y),  # LEFT
            3: lambda x, y: (x, y + self.speed)   # DOWN
        }[self.direction](self.x, self.y)

        if self.x <= -1 * constants.TILE_SIZE / 2:
            self.x = self.game.map.get_width() + constants.TILE_SIZE / 2
        elif self.x >= self.game.map.get_width() + constants.TILE_SIZE / 2:
            self.x = -1 * constants.TILE_SIZE / 2

    def draw(self):
        frame = int(self.game.tick * constants.ANIMATION_SPEED) % 4
        if frame == 3:
            frame = 2
        self.game.window.blit(
            pygame.transform.rotate(
                self.game.get_image_at(frame, constants.PLAYER_ROW),
                90 * self.direction),
            (self.x - constants.SPRITE_SIZE / 2, self.y - constants.SPRITE_SIZE / 2))

    def update_speed(self):
        index = 1 if self.fright == 0 else 0
        multiplier = constants.get_level_based_constant(self.game.level, constants.PACMAN_SPEED_MULTIPLIER)[index]
        self.speed = constants.BASE_SPEED * multiplier
