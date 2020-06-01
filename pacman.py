# pylint: disable=no-member
import sys
import pygame

from game_files import constants, Game


def delay(time_ms):
    pygame.time.wait(int(time_ms))


def main():
    pygame.init()

    game = Game.Game()
    game.initialize_level(True)

    while game.lives > 0:
        step_ms = game.step()
        delay(constants.DELAY - step_ms)

    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
