*This project has been created as part of the 42 curriculum by <lscarpul> and <enucci>.*

## Description

A-Maze-ing is a project that generates and displays mazes based on a configuration file. It includes features for creating perfect mazes, ensuring specific structural constraints, and providing an interactive terminal-based visualizer.

The maze generation logic is encapsulated in a reusable Python module.

## Instructions

### 1. Setup

It is recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:

```bash
make install
```

### 2. Execution

To run the program, use the `run` rule from the Makefile, which executes the main script with a default configuration file:

```bash
make run
```

Or run it directly:

```bash
python3 a_maze_ing.py config.txt
```

### 3. Linting

To check the code against `flake8` and `mypy` standards:

```bash
make lint
```

## Resources

-   **Maze Generation Algorithms**: [Wikipedia page on Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm) - A great overview of different algorithms.
-   **AI Usage**: AI (GitHub Copilot) was used to accelerate the initial boilerplate code generation, suggest type hints, and write docstrings. The core logic for the maze algorithms and application structure was designed and implemented manually.

---
*This section will be completed as the project progresses.*
