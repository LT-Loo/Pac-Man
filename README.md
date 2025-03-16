## About Pac-Man
The Pac-Man game is a dynamic maze action video game, where players take on the role of Pac-Man, navigating enclosed maze to devour all pellets scattered throughout while evading the pursuit of the ghosts.

## Key Features
### Random Maze Generation
The game features two distinct map options: the default map and the random map. The latter incorporates a sophisticated maze generator, implementing the iterative randomised depth-first search algorithm. This feature enhances the gaming experience by dynamically creating unique and challenging mazes, adding an element of excitement for players.

### Ghost Tracking Ability
There are two types of ghosts in the game:
| Ghost Colour | Behaviour | Explanation |
| :---: | --- | --- |
| Red | Roam the maze aimlessly | Whenever the ghost encounters an intersection point, it randomly selects an available path and commits to its chosen direction |
| Pink | Actively pursue Pac-Man | Implement a tracking mechanism based on the ___A* search algorithm___ to efficiently calculate and pursue the shortest path to reach Pac-Man |

## Technology Used
- Language: Python
- Library: Pygame

## Contributors
| Name | Contribution | Explanation |
| :---: | :---: | --- |
| Loo | Game Developer | Designed and developed game |
| Richard | Documentation | Project planning & game requirement analysis |
| Luke | Documentation | Game requirement analysis & software architecture |
| Malachi | Documentation | Software architecture & presentation video development |
