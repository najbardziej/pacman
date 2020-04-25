import Game

game = Game.Game()

while True:
    step_ms = game.step()
    game.delay(game.get_base_delay() - step_ms)
