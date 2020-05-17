from Ghosts import Ghost
import constants


class Blinky(Ghost.Ghost):
    def __init__(self, game, tile_x, tile_y):
        super().__init__(game, tile_x, tile_y, constants.SPRITE_SHEET_BLINKY_ROW)
        self.freeze = False
        self.in_base = False
        self.home_corner = (24, -3)
        self.target = (24, -3)
        self.elroy = 0

    def get_chase_target(self):
        player_tile_x = self.game.player.x // constants.TILE_SIZE
        player_tile_y = self.game.player.y // constants.TILE_SIZE
        return player_tile_x, player_tile_y

    def update_speed(self):
        if self.game.map.get_tile(self.get_tile_x(), self.get_tile_y()) == constants.TUNNEL:
            multiplier = constants.get_level_based_constant(self.game.level, constants.GHOST_SPEED_MULTIPLIER)[2]
        elif not self.dead and self.state == constants.GhostState.FRIGHTENED:
            multiplier = constants.get_level_based_constant(self.game.level, constants.GHOST_SPEED_MULTIPLIER)[1]
        elif self.elroy == 1:
            multiplier = constants.get_level_based_constant(self.game.level, constants.ELROY_SPEED_MULTIPLIER)[0][1]
        elif self.elroy == 2:
            multiplier = constants.get_level_based_constant(self.game.level, constants.ELROY_SPEED_MULTIPLIER)[1][1]
        else:
            multiplier = constants.get_level_based_constant(self.game.level, constants.GHOST_SPEED_MULTIPLIER)[0]
        self.speed = constants.BASE_SPEED * multiplier