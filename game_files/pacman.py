"""Pacman game - application entry-point"""
import sys
import pygame

import constants, game


def delay(time_ms):
    """Time delay between each frame"""
    pygame.time.wait(int(time_ms))


def main():
    """Main function of the game"""
    pygame.init()

    game_obj = game.Game()
    game_obj.initialize_level(True)

    while game_obj.lives > 0:
        step_ms = game_obj.step()
        delay(constants.DELAY - step_ms)

    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
