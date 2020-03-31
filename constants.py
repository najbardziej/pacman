import enum

TICKRATE = 150
TILE_SIZE = 32
GAME_MAP_FILE = "gamemap.txt"

SPRITE_SHEET_FILE = "sprite-sheet.png"
SPRITE_SHEET_SPRITE_SIZE = 48
SPRITE_SHEET_SPRITE_SPACING = 8

BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR   = (25, 25, 166)
PELLET_COLOR = (222, 161, 133)

WALL   = ' '
PELLET = '.'
POWER_PELLET = 'o'
NOTHING = '#'


class Direction(enum.IntEnum):
    RIGHT = 0
    UP    = 1
    LEFT  = 2
    DOWN  = 3
