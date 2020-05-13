from Ghosts import Ghost
import constants


class Pinky(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_PINKY_ROW)
        self.direction = constants.Direction.UP
        self.freeze = False
        self.home_corner = (3, -3)

    def get_chase_target(self):
        player_tile_x = self.game.player.x // constants.TILE_SIZE
        player_tile_y = self.game.player.y // constants.TILE_SIZE
        dx = 0
        dy = 0
        if self.game.player.direction == constants.Direction.LEFT:
            dx = -4
        elif self.game.player.direction == constants.Direction.RIGHT:
            dx = 4
        elif self.game.player.direction == constants.Direction.UP:
            dy = -4
        elif self.game.player.direction == constants.Direction.DOWN:
            dy = 4
        return player_tile_x + dx, player_tile_y + dy