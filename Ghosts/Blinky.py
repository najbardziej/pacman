from Ghosts import Ghost
import constants


class Blinky(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_BLINKY_ROW)
        self.move = True
