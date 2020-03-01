# pacman
Semester project for symbolic languages (python3 with pygame).

## Explanation of some ingame mechanics

### Ghost movement
Ghosts have three different modes: 
1. **CHASE** - Default movement of ghosts. Each of ghosts has different behaviour.
2. **SCATTER** - Few seconds when ghosts give up the chase. The ghosts are heading for their respective 'home corners' 
3. **FRIGHTENED** - Starts when Pac-Man eats one of 'energizers'. Ghosts move randomly.

Each of ghosts checks their target on every path intersection (except four) and check which path to choose. Ghosts may never choose to reverse their direction of travel, however, sometimes when the movement mode is changed, they are forced to (chase-to-scatter, chase-to-frightened, scatter-to-chase, and scatter-to-frightened).

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
	


	

	


##### Sources:
https://www.gamasutra.com/view/feature/132330/the_pacman_dossier.php
