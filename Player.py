import pygame
import enum


class Direction(enum.Enum):
    RIGHT = 0
    UP    = 1
    LEFT  = 2
    DOWN  = 3


class Player:
    def __init__(self, game, x, y):
        self.SPRITE_SHEET_ROW = 0
        self.ANIMATION_FRAME_COUNT = 3
        self.game = game
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.x = x
        self.y = y
        self.speed = 3

    def eat(self):
        pass

    def move(self):
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

        self.direction = self.next_direction
        if   self.direction == Direction.RIGHT:
            self.x += self.speed
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
        elif self.direction == Direction.DOWN:
            self.y += self.speed
        elif self.direction == Direction.UP:
            self.y -= self.speed

    def draw(self):
        frame = self.game.tick // 5 % 4
        if frame == 3:
            frame = 2
        self.game.window.blit(
            pygame.transform.rotate(
                self.game.sprite_sheet.get_image_at(frame, 0), 90 * self.direction.value), (self.x, self.y))

    def clear(self):
        pygame.draw.rect(self.game.window, (0, 0, 0), (self.x, self.y, 48, 48))
