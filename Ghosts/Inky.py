from Ghosts import Ghost
import constants


class Inky(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_INKY_ROW)
        self.home_corner = (27, 33)
        self.pellets_to_leave = 30

    def get_chase_target(self):
        dx = 0
        dy = 0
        if self.game.player.direction == constants.Direction.LEFT:
            dx = -2
        elif self.game.player.direction == constants.Direction.RIGHT:
            dx = 2
        elif self.game.player.direction == constants.Direction.UP:
            dy = -2
        elif self.game.player.direction == constants.Direction.DOWN:
            dy = 2
        player = self.game.player
        blinky = self.game.ghosts[0]
        dx = 2 * (player.get_tile_x() + dx - blinky.get_tile_x())
        dy = 2 * (player.get_tile_y() + dy - blinky.get_tile_y())

        return blinky.get_tile_x() + dx, blinky.get_tile_y() + dy
