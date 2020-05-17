import pygame
import Character
import constants


class Player(Character.Character):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y)
        self.SPRITE_SHEET_ROW = 0
        self.ANIMATION_FRAME_COUNT = 3
        self.fright = 0
        self.power_pellets = 0
        self.direction = constants.Direction.RIGHT
        self.next_direction = constants.Direction.RIGHT
        self.speed = 0

    def eat(self):
        if 0 < self.x < self.game.map.get_width():
            if abs((self.x % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                if abs((self.y % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:

                    points = self.game.map.remove_pellet(self.get_tile_x(), self.get_tile_y())
                    if points == 50:
                        self.power_pellets += 1
                        self.game.combo = 0
                        fright_time_s = constants.get_level_based_constant(self.game.level, constants.FRIGHT_TIME)
                        self.fright = fright_time_s * constants.TICKRATE
                        for ghost in self.game.ghosts:
                            ghost.change_state(constants.GhostState.FRIGHTENED)
                    if points:
                        self.game.score += points
                        self.game.update_caption()
                        pellets = sum(1 for i in self.game.map.get_pellets())
                        pellets_to_elroy2 = constants.get_level_based_constant(self.game.level, constants.ELROY_SPEED_MULTIPLIER)[1][0]
                        pellets_to_elroy1 = constants.get_level_based_constant(self.game.level, constants.ELROY_SPEED_MULTIPLIER)[0][0]
                        if pellets <= pellets_to_elroy2:
                            self.game.ghosts[0].elroy = 2
                        elif pellets <= pellets_to_elroy1:
                            self.game.ghosts[1].elroy = 1
                        return True
                    if self.game.fruit > 0:
                        fruit_location = self.game.map.get_coordinates('f')
                        if self.get_tile_x() in [fruit_location[0], fruit_location[0] + 1]:
                            if self.get_tile_y() == fruit_location[1]:
                                self.game.score += constants.get_level_based_constant(self.game.level, constants.FRUITS)[2]
                                self.game.fruit = 0
                                self.game.clear_fruit()
                                self.game.update_caption()
        return False

    def move(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.next_direction = constants.Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.next_direction = constants.Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.next_direction = constants.Direction.UP
                if event.key == pygame.K_DOWN:
                    self.next_direction = constants.Direction.DOWN

        self.update_speed()

        if 0 < self.x < self.game.map.get_width():
            if abs((self.x % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                if abs((self.y % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                    if self.direction != self.next_direction:
                        if self.next_direction == constants.Direction.RIGHT and \
                                self.game.map.get_tile(self.get_tile_x() + 1, self.get_tile_y()) != constants.WALL or \
                                self.next_direction == constants.Direction.LEFT and \
                                self.game.map.get_tile(self.get_tile_x() - 1, self.get_tile_y()) != constants.WALL or \
                                self.next_direction == constants.Direction.UP and \
                                self.game.map.get_tile(self.get_tile_x(), self.get_tile_y() - 1) != constants.WALL or \
                                self.next_direction == constants.Direction.DOWN and \
                                self.game.map.get_tile(self.get_tile_x(), self.get_tile_y() + 1) != constants.WALL and \
                                self.game.map.get_tile(self.get_tile_x(), self.get_tile_y() + 1) != constants.BARRIER:
                            self.x = (self.get_tile_x() + 0.5) * constants.TILE_SIZE
                            self.y = (self.get_tile_y() + 0.5) * constants.TILE_SIZE
                            self.direction = self.next_direction

                    if self.direction == constants.Direction.RIGHT and \
                            self.game.map.get_tile(self.get_tile_x() + 1, self.get_tile_y()) == constants.WALL or \
                            self.direction == constants.Direction.LEFT and \
                            self.game.map.get_tile(self.get_tile_x() - 1, self.get_tile_y()) == constants.WALL or \
                            self.direction == constants.Direction.UP and \
                            self.game.map.get_tile(self.get_tile_x(), self.get_tile_y() - 1) == constants.WALL or \
                            self.direction == constants.Direction.DOWN and \
                            self.game.map.get_tile(self.get_tile_x(), self.get_tile_y() + 1) == constants.WALL:
                        self.speed = 0

        if self.direction == constants.Direction.RIGHT:
            self.x += self.speed
        elif self.direction == constants.Direction.LEFT:
            self.x -= self.speed
        elif self.direction == constants.Direction.DOWN:
            self.y += self.speed
        elif self.direction == constants.Direction.UP:
            self.y -= self.speed

        if self.x <= -1 * constants.TILE_SIZE / 2:
            self.x = self.game.map.get_width() + constants.TILE_SIZE / 2
        elif self.x >= self.game.map.get_width() + constants.TILE_SIZE / 2:
            self.x = -1 * constants.TILE_SIZE / 2

    def draw(self):
        sprite_size = self.game.sprite_sheet.sprite_size
        frame = int(self.game.tick * constants.ANIMATION_SPEED) % 4
        if frame == 3:
            frame = 2
        self.game.window.blit(
            pygame.transform.rotate(
                self.game.sprite_sheet.get_image_at(frame, 0),
                90 * self.direction),
            (self.x - sprite_size / 2, self.y - sprite_size / 2))

    def update_speed(self):
        if self.fright > 0:
            multiplier = constants.get_level_based_constant(self.game.level, constants.PACMAN_SPEED_MULTIPLIER)[1]
        else:
            multiplier = constants.get_level_based_constant(self.game.level, constants.PACMAN_SPEED_MULTIPLIER)[0]
        self.speed = constants.BASE_SPEED * multiplier
