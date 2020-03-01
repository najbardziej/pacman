# pacman
Semester project for symbolic languages (python3 with pygame).

## Explanation of some ingame mechanics

### Ghost movement
Ghosts have three different modes: 
1. **CHASE** - Default movement of ghosts. Each of ghosts has different behaviour.
2. **SCATTER** - Few seconds when ghosts give up the chase. The ghosts are heading for their respective 'home corners' 
3. **FRIGHTENED** - Starts when Pac-Man eats one of 'energizers'. Ghosts move randomly.

Each of ghosts checks their target on every path intersection (except four, shown on image below) and check which path to choose. 

![map](https://media.gameinternals.com/pacman-ghosts/intersection-map.png)

Ghosts may never choose to reverse their direction of travel, however, sometimes when the movement mode is changed, they are forced to (chase-to-scatter, chase-to-frightened, scatter-to-chase, and scatter-to-frightened).

**Mode cycle time (in seconds)**
| Mode     | Level 1 | Levels 2-4 | Levels 5+ |
|:--------:| -------:| ----------:| ---------:|
| Scatter  | 7       | 7          | 5         |
| Chase    | 20      | 20         | 20        |
| Scatter  | 7       | 7          | 5         |
| Chase    | 20      | 20         | 20        |
| Scatter  | 5       | 5          | 5         |
| Chase    | 20      | 1033       | 1037      |
| Scatter  | 5       | 5          | 5         |
| Chase    | inf     | inf        | inf       |
	
#### Blinky - The red ghost
His home corner is the top-right one. Uses pacman position as the target.

#### Pinky - The pink ghost
His home corner is the top-left one. Uses position 4 tiles ahead of pacman as the target.

#### Inky - The blue ghost
His home corner is the bottom-right one. To calculate the target draws the vector from the position of 'Blinky' to the position 2 tiles ahead of pacman and doubles it.

#### Clyde - The orange ghost
His home corner is the bottom-left one. If his distance to pacman is greater than 8 tiles - moves exactly like 'Blinky'. Otherwise, moves like in 'Scatter' mode.


##### Sources:
https://www.gamasutra.com/view/feature/132330/the_pacman_dossier.php

https://gameinternals.com/understanding-pac-man-ghost-behavior
