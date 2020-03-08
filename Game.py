from Map import Map


class Game:
    def __init__(self, tickrate, tile_size, game_map_file):
        with open(game_map_file) as file:
            game_map = [line.rstrip('\n') for line in file]
        self.map = Map(game_map=game_map,
                       tile_size=tile_size)
        self.__delay = 1000 / tickrate
    
    def get_base_delay(self):
        return self.__delay

    def get_screen_width(self):
        return self.map.get_width()
    
    def get_screen_height(self):
        return self.map.get_height() + 3 * self.map.tile_size
