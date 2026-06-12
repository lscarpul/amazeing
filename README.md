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

### 3. Rendering Interattivo e Comandi a Terminale

Eseguendo `a-maze-ing config.txt` non solo verrà prodotto in silenzio il file esadecimale come da requisiti, ma si avvierà una "console grafica interattiva" che stamperà su terminale il labirinto, dandoti modo di interagirvi.
Menù in esecuzione:
- `[1]` **Re-generate**: Ripopola il blocco con una mappa random (ignora il SEED di config.txt riapplicando uno schema a caso).
- `[2]` **Show/Hide path**: Mostra graficamente qual è l'esatto percorso (snake) più corto verso la soluzione calcolato dall'engine, tracciando passo a passo senza sbavature nord, est, sud e ovest.
- `[3]` **Rotate Colors**: Evidenzia il labirinto con un tema di colori alternato per il terminale.
- `[4]` **Quit**: Termina il loop.

### 4. Sviluppo e Testing

Per eseguire lo script senza installare il pacchetto, puoi usare la regola `run` del Makefile:

```bash
make run
```

O eseguirlo direttamente con python:

```bash
python3 a_maze_ing.py config.txt
```

### 5. Compilazione pacchetto e Pulizia

Puoi compilare un pacchetto wheel distribuibile (in `/dist`) eseguendo:
```bash
make build
```

Per pulire i file temporanei generati da Python (`.pyc`, `__pycache__`):
```bash
make clean
```
Mentre per cancellare anche le build del pacchetto (le directory `build/`, `dist/` ed `*.egg-info`):
```bash
make fclean
```

### 6. Linting

Per verificare che il codice rispetti gli standard (`flake8` e `mypy`):

```bash
make lint
```

## Resources

-   **Algoritmo di Generazione**: [Recursive Backtracker](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker).
-   **Algoritmo di Risoluzione**: [Breadth-First Search (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search).

---

