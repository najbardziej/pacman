from Ghosts import Ghost
import constants


class Clyde(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_CLYDE_ROW)
        self.direction = constants.Direction.LEFT
        self.home_corner = (0, 33)
        self.pellets_to_leave = 60

    def get_chase_target(self):
        player_tile_x = self.game.player.x // constants.TILE_SIZE
        player_tile_y = self.game.player.y // constants.TILE_SIZE
        clyde_tile_x = self.x // constants.TILE_SIZE
        clyde_tile_y = self.y // constants.TILE_SIZE
        distance = ((clyde_tile_x - player_tile_x) ** 2 + (clyde_tile_y - player_tile_y) ** 2) ** (1 / 2)
        if distance < 8:
            return self.home_corner
        else:
            return player_tile_x, player_tile_y
