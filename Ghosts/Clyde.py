from Ghosts import Ghost
import constants


class Clyde(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_CLYDE_ROW)
        self.direction = constants.Direction.LEFT
        self.home_corner = (0, 33)
        self.pellets_to_leave = 60

    def get_chase_target(self):
        player = self.game.player
        distance = ((self.get_tile_x() - player.get_tile_x()) ** 2 + (self.get_tile_y()  - player.get_tile_y()) ** 2) ** (1 / 2)
        if distance < 8:
            return self.home_corner
        else:
            return player.get_tile_x(), player.get_tile_y()
