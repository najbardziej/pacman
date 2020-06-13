"""Module with constants needed for entire application"""
import bisect

TICKRATE = 60
DELAY = 1000 / TICKRATE
TILE_SIZE = 32
BASE_SPEED = TILE_SIZE / 8

GAMEMAP_FILE = "game_files/gamemap.txt"
GAMEMAP_WIDTH  = 28
GAMEMAP_WIDTH_PX = GAMEMAP_WIDTH * TILE_SIZE
GAMEMAP_HEIGHT = 31
GAMEMAP_HEIGHT_PX = GAMEMAP_HEIGHT * TILE_SIZE

WALL    = ' '
PELLET  = '.'
POWER_PELLET = 'o'
NOTHING = '#'
TUNNEL  = 't'
BARRIER = 'e'
INTERSECTION = 'x'
PELLET2 = INTERSECTION2 = 'X'

SPRITE_SHEET = "game_files/sprite-sheet.png"
SPRITE_SIZE = 48
SPRITE_SPACING = 8
PLAYER_ROW = 0
BLINKY_ROW = 1
INKY_ROW   = 2
PINKY_ROW  = 4
CLYDE_ROW  = 3

ANIMATION_SPEED = 0.20

BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR    = (25,  25, 166)
PELLET_COLOR  = (222, 161, 133)
BARRIER_COLOR = (250, 142, 225)
TEXT_COLOR    = (250, 242, 0)

FRUIT_SPAWN = [70, 170]
FRUIT_IMAGE_ROW = 6

GHOST_MODE_CYCLE = [
    # level, tuple with cycle times
    (1, (7, 27, 34, 54, 59,   79,   84)),
    (2, (7, 27, 34, 54, 59, 1092, 1097)),
    (5, (5, 25, 30, 50, 55, 1092, 1097))
]

FRIGHT_TIME = [
    # min level, fright time
    (1,  6),
    (2,  5),
    (3,  4),
    (4,  3),
    (5,  2),
    (6,  5),
    (7,  2),
    (9,  1),
    (10, 5),
    (11, 2),
    (12, 1),
    (14, 3),
    (15, 1),
    (17, 0),
    (18, 1),
    (19, 0)
]

PACMAN_SPEED_MULTIPLIER = [
    # min level, tuple with: speed, fright speed
    (1,  (0.8,  0.9)),
    (2,  (0.9, 0.95)),
    (5,  (1.0,  1.0)),
    (21, (0.9,  1.0))
]

GHOST_SPEED_MULTIPLIER = [
    # min level, tuple with: speed, fright speed, tunnel speed
    (1,  (.75, .50, .40)),
    (2,  (.85, .55, .45)),
    (5,  (.95, .60, .50))
]

ELROY_SPEED_MULTIPLIER = [
    # min level, tuple with: tuples with elroy dots left and speed
    (1,  ((20,   .80), (10,  .85))),
    (2,  ((30,   .90), (15,  .95))),
    (3,  ((40,   .90), (20,  .95))),
    (5,  ((40,  1.00), (20, 1.05))),
    (6,  ((50,  1.00), (25, 1.05))),
    (9,  ((60,  1.00), (30, 1.05))),
    (12, ((80,  1.00), (40, 1.05))),
    (15, ((100, 1.00), (50, 1.05))),
    (19, ((120, 1.00), (60, 1.05))),
]

FRUITS = [
    # min level, tuple with: name, image_column and points
    (1,  (0, "cherries",   100)),
    (2,  (1, "strawberry", 300)),
    (3,  (2, "peach",      500)),
    (5,  (3, "apple",      700)),
    (7,  (4, "grapes",    1000)),
    (9,  (5, "galaxian",  2000)),
    (11, (6, "bell",      3000)),
    (13, (7, "key",       5000)),
]


def get_level_based_constant(level, constant):
    """Function returning last tuple from list meeting the level requirement"""
    return constant[bisect.bisect_right([r[0] for r in constant], level) - 1][1]


RIGHT, UP, LEFT, DOWN = range(4)
SCATTER, CHASE, FRIGHTENED = range(3)
