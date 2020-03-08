import time

from Game import Game

game = Game(tickrate=60,
            tile_size=16,
            game_map_file="gamemap.txt",
            caption="Pacman")

game.draw_walls()

while True:
    start_time = time.time() * 1000
    game.step()
    game.delay(int(game.get_base_delay() 
                   - time.time() * 1000 
                   + start_time))
