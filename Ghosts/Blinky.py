from Ghosts import Ghost
import constants


class Blinky(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_BLINKY_ROW)
        self.freeze = False
        self.in_base = False
        self.home_corner = (24, -3)
        self.target = (24, -3)

    def get_chase_target(self):
        player_tile_x = self.game.player.x // constants.TILE_SIZE
        player_tile_y = self.game.player.y // constants.TILE_SIZE
        return player_tile_x, player_tile_y
