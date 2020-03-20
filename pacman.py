import Game
import SpriteSheet

TICKRATE = 60
TILE_SIZE = 32
GAME_MAP_FILE = "gamemap.txt"
SPRITE_SHEET_FILE = "sprite-sheet.png"
SPRITE_SHEET_SPRITE_SIZE = 48
SPRITE_SHEET_SPRITE_SPACING = 8

game = \
    Game.Game(
        tickrate=TICKRATE,
        tile_size=TILE_SIZE,
        game_map_file=GAME_MAP_FILE,
        sprite_sheet_file=SPRITE_SHEET_FILE,
        sprite_sheet_sprite_size=SPRITE_SHEET_SPRITE_SIZE,
        sprite_sheet_sprite_spacing=SPRITE_SHEET_SPRITE_SPACING
    )

game.draw_walls()

while True:
    step_ms = game.step()
    game.delay(game.get_base_delay() - step_ms)
