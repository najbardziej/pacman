import pygame

pygame.init()

# original pacman resolution - 224x228 with 8x8px tiles (28x36)
pygame.display.set_mode((224, 288))
pygame.display.set_caption("Pacman")

game_map_str = '''
                            
 ............  ............ 
 .    .     .  .     .    . 
 o ## . ### .  . ### . ## o 
 .    .     .  .     .    . 
 .......................... 
 .    .  .        .  .    . 
 .    .  .        .  .    . 
 ......  ....  ....  ...... 
      .     #  #     .      
##### .     #  #     . #####
##### .  ###xb#x###  . #####
##### .  #   ee   #  . #####
      .  # ###### #  .      
tttttt.### i#p#c# ###.tttttt
      .  # ###### #  .      
##### .  #        #  . #####
##### .  ##########  . #####
##### .  #        #  . #####
      .  #        #  .      
 ............  ............ 
 .    .     .  .     .    . 
 .    .     .  .     .    . 
 o..  ......Xs#X......  ..o 
   .  .  .        .  .  .   
   .  .  .        .  .  .   
 ......  ....  ....  ...... 
 .          .  .          . 
 .          .  .          . 
 .......................... 
                            
'''

game_map = []
for y, line_str in enumerate(game_map_str.splitlines()):
    for x, cell in enumerate(line_str):
        print(x, y - 1, cell)

tick_count = 60
base_delay = 1000 / tick_count

while True:
    start_time = pygame.time.get_ticks()

    end_time = pygame.time.get_ticks()
    pygame.time.delay(int(base_delay - end_time + start_time))
