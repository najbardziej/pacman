import pygame
import os
import sys

from game_files import constants, Game


def main():
    # inicjalizacja bibliotek zewnętrznych
    os.environ['SDL_VIDEO_WINDOW_POS'] = "512, 32"
    pygame.init()

    # tworzenie obiektów odpowiednich klas
    game = Game.Game()

    # wywołanie funkcji/metody wprawiającej te obiekty w ruch
    while game.lives > 0:
        step_ms = game.step()
        game.delay(constants.DELAY - step_ms)

    # sprzątanie
    pygame.display.quit()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()