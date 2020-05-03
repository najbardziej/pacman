import pygame
import Character
import constants


class Player(Character.Character):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y)
        self.SPRITE_SHEET_ROW = 0
        self.ANIMATION_FRAME_COUNT = 3
        self.fright = 0
        self.direction = constants.Direction.RIGHT
        self.next_direction = constants.Direction.RIGHT
        self.speed = self.get_speed()

    def eat(self):
        if 0 < self.x < self.game.map.get_width():
            if abs((self.x % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                if abs((self.y % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                    tile_x = self.x // constants.TILE_SIZE
                    tile_y = self.y // constants.TILE_SIZE
                    points = self.game.map.remove_pellet(tile_x, tile_y)
                    if points:
                        self.game.score += points
                        self.game.update_caption()
                        return True
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

        self.speed = self.get_speed()

        if 0 < self.x < self.game.map.get_width():
            if abs((self.x % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                if abs((self.y % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                    tile_x = self.x // constants.TILE_SIZE
                    tile_y = self.y // constants.TILE_SIZE

                    if self.direction != self.next_direction:
                        if self.next_direction == constants.Direction.RIGHT and \
                                self.game.map.get_tile(tile_x + 1, tile_y) != constants.WALL or \
                                self.next_direction == constants.Direction.LEFT and \
                                self.game.map.get_tile(tile_x - 1, tile_y) != constants.WALL or \
                                self.next_direction == constants.Direction.UP and \
                                self.game.map.get_tile(tile_x, tile_y - 1) != constants.WALL or \
                                self.next_direction == constants.Direction.DOWN and \
                                self.game.map.get_tile(tile_x, tile_y + 1) != constants.WALL and \
                                self.game.map.get_tile(tile_x, tile_y + 1) != constants.BARRIER:
                            self.x = (tile_x + 0.5) * constants.TILE_SIZE
                            self.y = (tile_y + 0.5) * constants.TILE_SIZE
                            self.direction = self.next_direction

                    if self.direction == constants.Direction.RIGHT and \
                            self.game.map.get_tile(tile_x + 1, tile_y) == constants.WALL or \
                            self.direction == constants.Direction.LEFT and \
                            self.game.map.get_tile(tile_x - 1, tile_y) == constants.WALL or \
                            self.direction == constants.Direction.UP and \
                            self.game.map.get_tile(tile_x, tile_y - 1) == constants.WALL or \
                            self.direction == constants.Direction.DOWN and \
                            self.game.map.get_tile(tile_x, tile_y + 1) == constants.WALL:
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

    def get_speed(self):
        if self.fright > 0:
            return constants.BASE_SPEED * 0.9
        return constants.BASE_SPEED * 0.8
