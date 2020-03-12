import Tile

WALL = ' '

class Map:
    __tiles = []

    def __init__(self, game_map, tile_size):
        for y, line_str in enumerate(game_map):
            for x, cell in enumerate(line_str):
                self.__tiles.append(Tile.Tile(x, y, cell))
        self.tile_size = tile_size

    def get_width(self):
        return (self.__tiles[-1].x + 1) * self.tile_size

    def get_height(self):
        return (self.__tiles[-1].y + 1) * self.tile_size

    def get_tile(self, x, y):
        if x < 0 or x > self.__tiles[-1].x:
            return False
        if y < 0 or y > self.__tiles[-1].y:
            return False
        return next(t for t in self.__tiles if t.x == x and t.y == y).cell

    def get_walls(self):
        for tile in self.__tiles:
            if tile.cell == WALL:
                wall_type = 0
                left = self.get_tile(tile.x - 1, tile.y)
                right = self.get_tile(tile.x + 1, tile.y)
                right2 = self.get_tile(tile.x + 2, tile.y)
                right3 = self.get_tile(tile.x + 3, tile.y)
                lower = self.get_tile(tile.x, tile.y + 1)
                upper = self.get_tile(tile.x, tile.y - 1)
                if right == WALL and lower == WALL and left != WALL and upper != WALL:
                    wall_type = 1
                elif left == WALL and lower == WALL and right != WALL and upper != WALL:
                    wall_type = 2
                elif left == WALL and upper == WALL and right != WALL and lower != WALL:
                    wall_type = 3
                elif right == WALL and upper == WALL and left != WALL and lower != WALL:
                    wall_type = 4
                elif left == WALL and right == WALL and upper != WALL and lower != WALL:
                    wall_type = 5
                elif left == WALL and right == WALL and upper != WALL and lower == WALL and upper is not False:
                    if right2 != WALL:
                        wall_type = 5
                    elif right2 == WALL and right3 == WALL:
                        wall_type = 5
                elif left == WALL and right == WALL and upper == WALL and lower != WALL and lower is not False and self.get_tile(tile.x, tile.y - 2) != WALL:
                    wall_type = 5
                elif left == WALL and right == WALL and upper == WALL and lower != WALL and lower is not False and self.get_tile(tile.x, tile.y - 2) == WALL and self.get_tile(tile.x, tile.y - 3) == WALL:
                    wall_type = 5
                elif upper == WALL and lower == WALL and left != WALL and right != WALL:
                    wall_type = 6
                elif upper == WALL and lower == WALL and left != WALL and right == WALL and left is not False and self.get_tile(tile.x + 2, tile.y) != WALL:
                    wall_type = 6
                elif upper == WALL and lower == WALL and left == WALL and right != WALL and right is not False and self.get_tile(tile.x - 2, tile.y) != WALL:
                    wall_type = 6
                elif upper == WALL and lower == WALL and left != WALL and right == WALL and left is not False and self.get_tile(tile.x + 2, tile.y) == WALL and self.get_tile(tile.x + 3, tile.y) == WALL:
                    wall_type = 6
                elif upper == WALL and lower == WALL and left == WALL and right != WALL and right is not False and self.get_tile(tile.x - 2, tile.y) == WALL and self.get_tile(tile.x - 3, tile.y) == WALL:
                    wall_type = 6
                yield tile.x, tile.y, wall_type
