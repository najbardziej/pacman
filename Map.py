import pygame
from Tile import Tile


class Map:
    __tiles = []
    
    def __init__(self, game_map, tile_size):
        for y, line_str in enumerate(game_map):
            for x, cell in enumerate(line_str):
                self.__tiles.append(Tile(x, y, cell))
        self.tile_size = tile_size

    def get_width(self):
        return (self.__tiles[-1].x + 1) * self.tile_size
    
    def get_height(self):
        return (self.__tiles[-1].y + 1) * self.tile_size

    def get_walls(self):
        for tile in self.__tiles:
            if tile.cell == ' ':
                yield tile.x, tile.y
