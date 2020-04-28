import Character
import constants


class Ghost(Character.Character):
    def __init__(self, game, tile_x, tile_y, image_row):
        super().__init__(game, tile_x, tile_y)
        self.image_row = image_row
        self.direction = constants.Direction.RIGHT
        self.freeze = True
        self.in_base = True
        self.speed = constants.BASE_SPEED * 0.75
        self.home_corner = (0, 0)
        self.target = (0, 0)
        self.pellets_to_leave = 0

    def get_distance_to_target(self, x, y):
        return ((x - self.target[0]) ** 2 + (y - self.target[1]) ** 2) ** (1/2)

    def move(self):
        if not self.freeze:
            if self.in_base:
                self.target = self.game.barrier.get_entrance()
                if abs(self.x - self.target[0] * constants.TILE_SIZE - constants.TILE_SIZE / 2) <= self.speed / 2:
                    if abs(self.y - self.target[1] * constants.TILE_SIZE + constants.TILE_SIZE / 2) <= self.speed / 2:
                        self.in_base = False
                        self.target = self.home_corner
                        self.direction = constants.Direction.LEFT
                        self.game.barrier.visible = True
                    else:
                        self.x = self.target[0] * constants.TILE_SIZE + constants.TILE_SIZE / 2
                        self.direction = constants.Direction.UP
            else:
                if 0 < self.x < self.game.map.get_width():
                    if abs((self.x % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                        if abs((self.y % constants.TILE_SIZE) - constants.TILE_SIZE / 2) <= self.speed / 2:
                            tile_x = self.x // constants.TILE_SIZE
                            tile_y = self.y // constants.TILE_SIZE

                            possible_directions = []    # up, left, down, right - tiebreaker
                            if self.game.map.get_tile(tile_x, tile_y - 1) != constants.WALL and \
                                    self.direction != constants.Direction.DOWN:
                                possible_directions.append(
                                    (constants.Direction.UP, self.get_distance_to_target(tile_x, tile_y - 1)))
                            if self.game.map.get_tile(tile_x - 1, tile_y) != constants.WALL and \
                                    self.direction != constants.Direction.RIGHT:
                                possible_directions.append(
                                    (constants.Direction.LEFT, self.get_distance_to_target(tile_x - 1, tile_y)))
                            if self.game.map.get_tile(tile_x, tile_y + 1) != constants.WALL and \
                                    self.game.map.get_tile(tile_x, tile_y + 1) != constants.BARRIER and \
                                    self.direction != constants.Direction.UP:
                                possible_directions.append(
                                    (constants.Direction.DOWN, self.get_distance_to_target(tile_x, tile_y + 1)))
                            if self.game.map.get_tile(tile_x + 1, tile_y) != constants.WALL and \
                                    self.direction != constants.Direction.LEFT:
                                possible_directions.append(
                                    (constants.Direction.RIGHT, self.get_distance_to_target(tile_x + 1, tile_y)))

                            if len(possible_directions) >= 2 or \
                                    (len(possible_directions) == 1 and possible_directions[0] != self.direction):
                                self.x = (tile_x + 0.5) * constants.TILE_SIZE
                                self.y = (tile_y + 0.5) * constants.TILE_SIZE
                                self.direction = sorted(possible_directions, key=lambda x: x[1])[0][0]

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
        else:
            self.unfreeze()

    def unfreeze(self):
        pellets = sum(1 for i in self.game.map.get_pellets())
        if pellets <= self.game.map.total_pellets - self.pellets_to_leave:
            self.game.barrier.visible = False
            self.freeze = False

    def draw(self):
        sprite_size = constants.SPRITE_SHEET_SPRITE_SIZE
        if not self.freeze:
            frame = int(self.game.tick * constants.ANIMATION_SPEED) % 2
        else:
            frame = 0

        self.game.window.blit(
            self.game.sprite_sheet.get_image_at(frame + self.direction * 2, self.image_row),
            (self.x - sprite_size / 2, self.y - sprite_size / 2))