from game_files import constants


class Barrier:
    def __init__(self, game):
        self.game = game
        self.tiles = []
        self.visible = False

    def get_entrance(self):
        avg_x = sum(t[0] for t in self.tiles) / len(self.tiles)
        avg_y = sum(t[1] for t in self.tiles) / len(self.tiles)
        return avg_x, avg_y - 1

    def get_spawn(self):
        entrance_x, entrance_y = self.get_entrance()
        return entrance_x, entrance_y + 3

    def add_tile(self, tile_x, tile_y):
        self.tiles.append((tile_x, tile_y))

    def draw(self):
        if self.visible:
            for tile in self.tiles:
                self.game.draw_line(tile[0] - 0.25, tile[1] + 0.5,
                                    tile[0] + 1.25, tile[1] + 0.5,
                                    color=constants.BARRIER_COLOR)

    def clear(self):
        if self.visible:
            for tile in self.tiles:
                self.game.draw_line(tile[0] - 0.25, tile[1] + 0.5,
                                    tile[0] + 1.25, tile[1] + 0.5,
                                    color=constants.BACKGROUND_COLOR)
