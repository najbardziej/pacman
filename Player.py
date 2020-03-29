import pygame
import enum
import Character


class Direction(enum.Enum):
    RIGHT = 0
    UP    = 1
    LEFT  = 2
    DOWN  = 3


class Player(Character.Character):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game)
        self.SPRITE_SHEET_ROW = 0
        self.ANIMATION_FRAME_COUNT = 3
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.x = (tile_x + 1)   * self.game.map.tile_size
        self.y = (tile_y + 0.5) * self.game.map.tile_size
        self.speed = self.game.map.tile_size / 6 * 0.8

    def eat(self):
        pass

    def move(self):
        print(self.x, self.y)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.next_direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.next_direction = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.next_direction = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.next_direction = Direction.DOWN

        if abs((self.x % self.game.map.tile_size) - self.game.map.tile_size / 2) <= self.speed / 2:
            if abs((self.y % self.game.map.tile_size) - self.game.map.tile_size / 2) <= self.speed / 2:
                if self.direction != self.next_direction:
                    tile_x = self.x // self.game.map.tile_size
                    tile_y = self.y // self.game.map.tile_size
                    self.x = (tile_x + 0.5) * self.game.map.tile_size
                    self.y = (tile_y + 0.5) * self.game.map.tile_size
                    self.direction = self.next_direction

        if self.direction == Direction.RIGHT:
            self.x += self.speed
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
        elif self.direction == Direction.DOWN:
            self.y += self.speed
        elif self.direction == Direction.UP:
            self.y -= self.speed




    def draw(self):
        sprite_size = self.game.sprite_sheet.sprite_size
        frame = self.game.tick // 5 % 4
        if frame == 3:
            frame = 2
        self.game.window.blit(
            pygame.transform.rotate(
                self.game.sprite_sheet.get_image_at(frame, 0),
                90 * self.direction.value),
            (self.x - sprite_size / 2, self.y - sprite_size / 2))
