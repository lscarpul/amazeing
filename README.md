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

### 2. Installazione del Pacchetto (Packaging) e Utilizzo

Il progetto è stato pacchettizzato in modo da poter essere installato nel proprio ambiente Python. Gli artefatti si trovano nella cartella `dist/`.

Per installare il pacchetto e il comando CLI:
```bash
# Esempio usando la wheel generata
pip install dist/amazeing-0.1.0-py3-none-any.whl
```

Una volta installato, il programma espone un comando globale chiamato `a-maze-ing`.
Puoi eseguirlo in questo modo da qualsiasi posizione del terminale:

```bash
a-maze-ing config.txt
```

Inoltre, il modulo `mazegen` diventa disponibile come vera e propria libreria per altri script Python:
```python
from mazegen.generator import MazeGenerator
```

### 3. Sviluppo e Testing

Per eseguire lo script senza installare il pacchetto, puoi usare la regola `run` del Makefile:

```bash
make run
```

O eseguirlo direttamente con python:

```bash
python3 a_maze_ing.py config.txt
```

### 4. Linting

Per verificare che il codice rispetti gli standard (`flake8` e `mypy`):

```bash
make lint
```

## Resources

-   **Maze Generation Algorithms**: [Wikipedia page on Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm) - A great overview of different algorithms.
-   **AI Usage**: AI (GitHub Copilot) was used to accelerate the initial boilerplate code generation, suggest type hints, and write docstrings. The core logic for the maze algorithms and application structure was designed and implemented manually.

---
*This section will be completed as the project progresses.*
