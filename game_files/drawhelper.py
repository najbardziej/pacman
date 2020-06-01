import math
import pygame

from game_files import constants, Game


def draw_arc(start_x, start_y, start_angle, stop_angle,
             color=constants.WALL_COLOR):
    line_width = int(constants.TILE_SIZE / 8)
    x_compensation = line_width / 2 if start_angle in [0, 3/2] else 0
    y_compensation = line_width / 2 if stop_angle  in [0, 3/2] else 0
    pygame.draw.arc(Game.Game.window, color,
                    (start_x * constants.TILE_SIZE + x_compensation,
                     start_y * constants.TILE_SIZE + y_compensation,
                     constants.TILE_SIZE, constants.TILE_SIZE),
                    start_angle * math.pi, stop_angle * math.pi, line_width)


def draw_line(x0, y0, x1, y1, color=constants.WALL_COLOR):
    line_width = int(constants.TILE_SIZE / 8)
    pygame.draw.line(Game.Game.window, color,
                     (x0 * constants.TILE_SIZE,
                      y0 * constants.TILE_SIZE),
                     (x1 * constants.TILE_SIZE,
                      y1 * constants.TILE_SIZE),
                     line_width)


def draw_rect(x0, y0, width, height=0, offset=0,
              color=constants.BACKGROUND_COLOR):
    if height == 0:
        height = width
    pygame.draw.rect(Game.Game.window, color,
                     (x0 * constants.TILE_SIZE + offset,
                      y0 * constants.TILE_SIZE + offset,
                      width, height))
