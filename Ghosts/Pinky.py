from Ghosts import Ghost
import constants


class Pinky(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_PINKY_ROW)
        self.direction = constants.Direction.UP
        self.freeze = False
        self.home_corner = (3, -3)

