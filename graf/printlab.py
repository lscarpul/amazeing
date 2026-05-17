
import sys
from typing import List


def read_lines(labirinto_file: str):
    maze_lines = []

    try:
        with open(labirinto_file, 'r') as f:
            for line in f:
                maze_lines.append(line.strip())

    except FileNotFoundError:
        sys.exit(1)
    except PermissionError:
        sys.exit(1)
    except ValueError:
        sys.exit(1)
    return maze_lines


def save_lines(labirinto_file: str, maze_lines: List[str]):
    try:
        with open(labirinto_file, 'w') as f:
            for line in maze_lines:
                f.write(f"{line}\n")

    except PermissionError:
        sys.exit(1)
    except Exception:
        sys.exit(1)


class ANSIColors:
    """Tavolozza dei colori per il terminale usando i codici ANSI."""
    RESET = "\033[0m"         # Riporta il colore a quello base del terminale
    WALL = "\033[90m"         # Grigio scuro per i muri
    PATH = "\033[97m"         # Bianco luminoso per i passaggi
    START = "\033[92m"        # Verde per l'entrata
    EXIT = "\033[91m"         # Rosso per l'uscita
    SOLUTION = "\033[96m"     # Ciano per il percorso risolutivo


def build_visual_matrix(hex_lines: List[str]) -> List[List[str]]:
    if not hex_lines:
        return []

    logical_height = len(hex_lines)
    logical_width = len(hex_lines[0])

    visual_height = logical_height * 3
    visual_width = logical_width * 3

    #       muri
    matrix: List[List[str]] = [
        ['█' for _ in range(visual_width)]
        for _ in range(visual_height)
    ]
    # 2. LO SCAVO
    for y in range(logical_height):
        for x in range(logical_width):
            # Prendiamo il carattere esadecimale (es. 'A', '3')
            hex_char = hex_lines[y][x]

            # Trasformiamolo in un numero intero (base 16)
            cell_value = int(hex_char, 16)

            # coordinate CENTRO cella matrice 3x3
            center_y = y * 3 + 1
            center_x = x * 3 + 1

            # Scaviamo il centro della cella (è sempre calpestabile)
            matrix[center_y][center_x] = ' '

            # Controllo Muro NORD  (Bit 0 -> Valore 1)
            if not (cell_value & 1):
                matrix[center_y - 1][center_x] = ' '

            # Controllo Muro EST  (Bit 1 -> Valore 2)
            if not (cell_value & 2):
                matrix[center_y][center_x + 1] = ' '

            # Controllo Muro SUD  (Bit 2 -> Valore 4)
            if not (cell_value & 4):
                matrix[center_y + 1][center_x] = ' '

            # Controllo Muro OVEST  (Bit 3 -> Valore 8)
            if not (cell_value & 8):
                matrix[center_y][center_x - 1] = ' '

    return matrix


if __name__ == "__main__":
    import os
    
    # Costruisco il path a labirinto.txt
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lab_path = os.path.join(current_dir, 'labirinto.txt')
    
    print(f"Test lettura da: {lab_path}")
    lines = read_lines(lab_path)
    
    # Filtriamo solo le righe che compongono la griglia
    # Si fermano alla prima riga vuota o a righe contenenti virgole
    maze_only_lines = []
    for line in lines:
        if not line or ',' in line or not all(c in '0123456789ABCDEFabcdef' for c in line):
            break
        maze_only_lines.append(line)
    
    if maze_only_lines:
        print(f"Lette {len(maze_only_lines)} righe di mappa con successo!")
        visual_matrix = build_visual_matrix(maze_only_lines)
        
        print("Rendering Labirinto:")
        for row in visual_matrix:
            print("".join(row))
    else:
        print("Nessuna riga di mappa letta o file vuoto.")
