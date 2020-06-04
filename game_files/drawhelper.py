import math
import pygame

from game_files import constants, Game

LINE_WIDTH = constants.TILE_SIZE // 8


def draw_arc(x0, y0, start_angle, stop_angle,
             color=constants.WALL_COLOR):
    x_compensation = LINE_WIDTH / 2 if start_angle in [0, 3/2] else 0
    y_compensation = LINE_WIDTH / 2 if stop_angle  in [0, 3/2] else 0
    pygame.draw.arc(Game.Game.window, color,
                    (x0 * constants.TILE_SIZE + x_compensation,
                     y0 * constants.TILE_SIZE + y_compensation,
                     constants.TILE_SIZE, constants.TILE_SIZE),
                    start_angle * math.pi, stop_angle * math.pi, LINE_WIDTH)


def draw_line(x0, y0, x1, y1, color=constants.WALL_COLOR):
    pygame.draw.line(Game.Game.window, color,
                     (x0 * constants.TILE_SIZE,
                      y0 * constants.TILE_SIZE),
                     (x1 * constants.TILE_SIZE,
                      y1 * constants.TILE_SIZE),
                     LINE_WIDTH)


def draw_rect(x0, y0, width, height=0, offset=0,
              color=constants.BACKGROUND_COLOR):
    if height == 0:
        height = width
    pygame.draw.rect(Game.Game.window, color,
                     (x0 * constants.TILE_SIZE + offset,
                      y0 * constants.TILE_SIZE + offset,
                      width, height))


def get_image_at(x, y):
    rectangle = pygame.Rect((
        x * (constants.SPRITE_SIZE + constants.SPRITE_SPACING * 2)
        + constants.SPRITE_SPACING,
        y * (constants.SPRITE_SIZE + constants.SPRITE_SPACING * 2)
        + constants.SPRITE_SPACING,
        constants.SPRITE_SIZE,
        constants.SPRITE_SIZE
    ))
    image = pygame.Surface(rectangle.size).convert()
    image.set_colorkey(constants.BACKGROUND_COLOR)
    image.blit(Game.Game.sprite_sheet, (0, 0), rectangle)
    return image


def draw_text(string):
    font = pygame.font.SysFont(pygame.font.get_default_font(),
                               constants.SPRITE_SIZE)
    text = font.render(string, True, constants.TEXT_COLOR,
                       constants.BACKGROUND_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (constants.GAMEMAP_WIDTH_PX // 2,
                        constants.GAMEMAP_HEIGHT_PX // 2 +
                        2 * constants.TILE_SIZE)
    Game.Game.window.blit(text, text_rect)


def clear_text():
    draw_rect(constants.GAMEMAP_WIDTH // 2 - 5,
              constants.GAMEMAP_HEIGHT // 2 + 2,
              width=10 * constants.TILE_SIZE,
              height=constants.TILE_SIZE)
