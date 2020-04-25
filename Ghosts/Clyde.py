from Ghosts import Ghost
import constants


class Clyde(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_CLYDE_ROW)
        self.direction = constants.Direction.LEFT
        self.home_corner = (0, 33)
        self.pellets_to_leave = 60

