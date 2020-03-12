import Game

TICKRATE = 60
TILE_SIZE = 16
GAME_MAP_FILE = "gamemap.txt"
CAPTION = "Pacman"

game = Game.Game(tickrate=TICKRATE,
                 tile_size=TILE_SIZE,
                 game_map_file=GAME_MAP_FILE,
                 caption=CAPTION)

game.draw_walls()

while True:
    step_ms = game.step()
    game.delay(game.get_base_delay() - step_ms)
