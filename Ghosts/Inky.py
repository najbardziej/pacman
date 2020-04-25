from Ghosts import Ghost
import constants


class Inky(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_INKY_ROW)
        self.home_corner = (27, 33)
        self.pellets_to_leave = 30
