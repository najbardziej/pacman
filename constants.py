import enum

TICKRATE  = 60
DELAY = 1000 / TICKRATE
TILE_SIZE = 32
BASE_SPEED = TILE_SIZE / 6 * 0.75
GAME_MAP_FILE = "gamemap.txt"

WALL    = ' '
PELLET  = '.'
POWER_PELLET = 'o'
NOTHING = '#'
BARRIER = 'e'
INTERSECTION = 'x'
PELLET2 = INTERSECTION2 = 'X'

SPRITE_SHEET_FILE = "sprite-sheet.png"
SPRITE_SHEET_SPRITE_SIZE = 48
SPRITE_SHEET_SPRITE_SPACING = 8
SPRITE_SHEET_BLINKY_ROW = 1
SPRITE_SHEET_INKY_ROW   = 2
SPRITE_SHEET_PINKY_ROW  = 4
SPRITE_SHEET_CLYDE_ROW  = 3

ANIMATION_SPEED = 0.20

BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR    = (25, 25, 166)
PELLET_COLOR  = (222, 161, 133)
BARRIER_COLOR = (250, 142, 225)

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
    (0,  (0.8,  0.9)),
    (2,  (0.9, 0.95)),
    (5,  (1.0,  1.0)),
    (21, (0.9,  1.0))
]

GHOST_SPEED_MULTIPLIER = [
    # min level, tuple with: speed, fright speed, tunnel speed
    (1,  (0.75, 0.50, 0.40)),
    (2,  (0.85, 0.55, 0.45)),
    (5,  (0.95, 0.60, 0.50))
]

ELROY_SPEED_MULTIPLIER = [
    # min level, tuple with: tuples with elroy dots left and speed
    (1,  ((20,  0.80), (10, 0.85))),
    (2,  ((30,  0.90), (15, 0.95))),
    (3,  ((40,  0.90), (20, 0.95))),
    (5,  ((40,  1.00), (20, 1.05))),
    (6,  ((50,  1.00), (25, 1.05))),
    (9,  ((60,  1.00), (30, 1.05))),
    (12, ((80,  1.00), (40, 1.05))),
    (15, ((100, 1.00), (50, 1.05))),
    (19, ((120, 1.00), (60, 1.05)))
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
    (13, (7, "key",       5000))
]


def get_level_based_constant(level, constant):
    return list(filter(lambda x: x[0] <= level, constant))[-1][1]


class Direction(enum.IntEnum):
    RIGHT = 0
    UP    = 1
    LEFT  = 2
    DOWN  = 3


class GhostState(enum.IntEnum):
    SCATTER    = 0
    CHASE      = 1
    FRIGHTENED = 2
