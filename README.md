*This project has been created as part of the 42 curriculum by <lscarpul>, <enucci>.*

## Description
A-Maze-ing is a Python project that generates, solves, and displays random mazes based on parameters provided in a configuration file. It implements a reusable maze generation module capable of producing both perfect and imperfect mazes, while guaranteeing the inclusion of a '42' pattern where size permits.

## Instructions
### Compilation and Installation
The project provides a reusable `mazegen` package. To compile the package:
```bash
make build
```
This generates a `.whl` and `.tar.gz` artifact in the `dist/` directory.
To install the complete CLI application:
```bash
pip install dist/amazeing-0.1.0-py3-none-any.whl
```
Alternatively, just setup a local environment:
```bash
python3 -m venv venv
source venv/bin/activate
make install
```

### Execution
Run the script using a configuration file:
```bash
python3 a_maze_ing.py config.txt
```
If installed as a package, you can just run:
```bash
a-maze-ing config.txt
```
This will generate the maze, save it in hexadecimal format to the output file specified in the config, and launch an interactive terminal menu where you can test features such as re-generation and shortest path visualization.

## Resources
- **Recursive Backtracker Algorithm**: [Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker). Used for the generation task of the maze.
- **Breadth-First Search (BFS)**: [Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search). Used for the pathfinding and solving part of the project.
- **Python Setuptools**: Official documentation used to build the reusable Python module and CLI entry points.

## Configuration File
The configuration file dictates the constraints of the maze:
- Lines starting with `#` are comments.
- Format must be `KEY=VALUE`.
- Required keys:
  - `WIDTH`: Width of the maze (integer).
  - `HEIGHT`: Height of the maze (integer).
  - `ENTRY`: Starting coordinate string `X,Y`.
  - `EXIT`: Ending coordinate string `X,Y`.
  - `OUTPUT_FILE`: Path to the file where the maze will be printed.
  - `PERFECT`: Boolean (`True` or `False`) to toggle perfect maze generation.
- Optional keys:
  - `SEED`: An integer value to ensure identical maze replication.

## Maze Algorithm
We chose the **Recursive Backtracker** algorithm to generate the maze structure. The algorithm starts at an initial cell, marks it visited, and randomly drills walls to adjacent unvisited cells using a recursive approach (Depth-First). This digs deep paths into the grid until it hits a dead-end, then naturally backtracks to explore other branches.

## Reason for choosing this algorithm
The Recursive Backtracker was chosen primarily because it is straightforward to implement and heavily guarantees that all areas will be reachable. It inherently avoids creating completely isolated open rooms (which helps with our 3x3 restrictions) and outputs aesthetically pleasing, highly branchy, "deep" mazes that feel challenging compared to other simple algorithms like Binary Tree. 

## Reusable Module
The core logic resides in a reusable Python package called `mazegen`.
To use it in other projects:
```python
from mazegen.generator import MazeGenerator

maze = MazeGenerator(larghezza=20, altezza=20, perfetto=True)
maze.generate(start_x=0, start_y=0)
maze.solve(entrata=(0,0), uscita=(19,19))

path = maze.get_solution_path()
```
The module seamlessly manages state, avoids 3x3 empty zones dynamically, forces a `42` pattern inside the grid, and can optionally poke holes in walls to provide an "imperfect" maze topology.

## Team and project management
- **Roles**:
  - `lscarpul`: Focused on the Reusable Module architecture, Recursive Backtracking logic, BFS solving algorithm, and constraints validation.
  - `enucci`: Managed the Interactive UI visualizer, file I/O operations, error handling, packaging, and configuration parsing.
- **Planning**: We outlined the core engine first, aiming to get basic hex output working in the first week. Then we spent the final days on the interactive viewer and packaging logic. Our planning evolved slightly when we had to completely rework our wall-deletion logic to dynamically prevent 3x3 empty zones.
- **What worked well**: The separation of `mazegen` as a library from the main CLI application allowed parallel work without merging conflicts.
- **What could be improved**: Testing could have been wider; we could have added automated `pytest` units instead of manually running scenarios against the edge cases.
- **Tools**: We used **Git** for version control via GitHub, **Trello** for kanban-style task tracking, and **Mypy/Flake8** for continuous linting during the development process.
