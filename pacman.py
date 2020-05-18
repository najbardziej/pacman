import pygame
import os
import sys

from game_files import constants, Game


def delay(time_ms):
    pygame.time.wait(int(time_ms))


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "512, 32"
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
