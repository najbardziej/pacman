import Game
import constants

game = Game.Game()

while True:
    step_ms = game.step()
    game.delay(constants.DELAY - step_ms)
