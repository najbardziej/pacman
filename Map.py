import Tile

WALL   = ' '
PELLET = '.'
POWER_PELLET = 'o'
NOTHING = '#'

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

    def remove_pellet(self, tile_x, tile_y):
        tile = next(t for t in self.__tiles if t.x == tile_x and t.y == tile_y)
        if tile.cell == PELLET:
            tile.cell = NOTHING
            return 10
        if tile.cell == POWER_PELLET:
            tile.cell = NOTHING
            return 50
        return False

    def get_pellets(self):
        for tile in self.__tiles:
            if tile.cell == PELLET:
                yield tile.x, tile.y, PELLET
            if tile.cell == POWER_PELLET:
                yield tile.x, tile.y, POWER_PELLET

    def get_walls(self):
        for tile in self.__tiles:
            if tile.cell == WALL:
                wall = {}
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        wall[(i, j)] = self.get_tile(tile.x + i, tile.y + j) == WALL

                if wall[0, +1] and wall[+1, 0] and (not wall[-1, 0] or not wall[+1, +1]) and (not wall[0, -1] or wall[-1, 0]):
                    wall_type = 0
                elif wall[0, +1] and wall[+1, 0] and wall[0, -1] and not wall[-1, 0] and not wall[+1, +1]:
                    wall_type = 0
                elif wall[0, +1] and wall[-1, 0] and (not wall[0, -1] or not wall[-1, +1]) and (not wall[+1, 0] or wall[0, -1]):
                    wall_type = 1
                elif wall[0, +1] and wall[-1, 0] and wall[+1, 0] and not wall[0, -1] and not wall[-1, +1]:
                    wall_type = 1
                elif wall[0, -1] and wall[-1, 0] and (not wall[+1, 0] or not wall[-1, -1]) and (not wall[0, +1] or wall[+1, 0]):
                    wall_type = 2
                elif wall[0, +1] and wall[-1, 0] and wall[0, +1] and not wall[+1, 0] and not wall[-1, -1]:
                    wall_type = 2
                elif wall[0, -1] and wall[+1, 0] and (not wall[0, +1] or not wall[+1, -1]) and (not wall[-1, 0] or wall[0, +1]):
                    wall_type = 3
                elif wall[0, -1] and wall[+1, 0] and wall[-1, 0] and not wall[0, +1] and not wall[+1, -1]:
                    wall_type = 3
                elif wall[0, +1] and wall[0, -1] and (wall[+1, 0] + wall[-1, 0] != 2):
                    wall_type = 4
                else:
                    wall_type = 5

                yield tile.x, tile.y, wall_type
