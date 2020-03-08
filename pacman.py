import pygame
from Game import Game
pygame.init()

game = Game(tickrate=60,
            tile_size=16,
            game_map_file="gamemap.txt")

pygame.display.set_mode((game.get_screen_width(),
                         game.get_screen_height()))
pygame.display.set_caption("Pacman")

while True:
    start_time = pygame.time.get_ticks()

    end_time = pygame.time.get_ticks()
    pygame.time.delay(int(game.get_base_delay() 
                          - end_time 
                          + start_time))
