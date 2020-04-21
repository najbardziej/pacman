import Game

game = Game.Game()

while True:
    step_ms = game.step()
    if step_ms > 0.01:
        print(step_ms)
    game.delay(game.get_base_delay() - step_ms)
