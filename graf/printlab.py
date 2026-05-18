import sys
from typing import List, Tuple, Set


class ANSIColors:
    RESET = "\033[0m"
    WALL = "\033[97m"         # White FG for walls
    PATH = "\033[40m"         # Black BG
    START = "\033[45m"        # Magenta BG (from the image)
    EXIT = "\033[41m"         # Red BG
    PATTERN_42 = "\033[47m"   # Light Grey BG
    SOLUTION = "\033[46m"     # Cyan BG


def build_visual_matrix(hex_lines: List[str]) -> List[List[str]]:
    if not hex_lines:
        return []
    logical_height = len(hex_lines)
    logical_width = len(hex_lines[0])

    # 2x+1 così i muri tra due celle vengono stampati una volta sola (si sovrappongono/condividono)
    visual_height = logical_height * 2 + 1
    visual_width = logical_width * 2 + 1

    # Di default tutto è muro
    matrix = [['⬜' for _ in range(visual_width)] for _ in range(visual_height)]
    for y in range(logical_height):
        for x in range(logical_width):
            cell_value = int(hex_lines[y][x], 16)
            cy = y * 2 + 1
            cx = x * 2 + 1

            # Il centro della cella è sempre un passaggio
            matrix[cy][cx] = '⬛'

            # Scava i passaggi verso i vicini se non c'è il muro
            if not (cell_value & 1):
                matrix[cy - 1][cx] = '⬛'  # Nord
            if not (cell_value & 2):
                matrix[cy][cx + 1] = '⬛'  # Est
            if not (cell_value & 4):
                matrix[cy + 1][cx] = '⬛'  # Sud
            if not (cell_value & 8):
                matrix[cy][cx - 1] = '⬛'  # Ovest
    return matrix

def render_interactive(maze_gen, entry: Tuple[int, int], exit_coords: Tuple[int, int], show_path: bool, color_scheme: int):
    # Convert cell walls to hex strings
    hex_lines = []
    walls_map = {'N': 1, 'E': 2, 'S': 4, 'W': 8}
    for row in maze_gen.get_grid():
        r = ""
        for cell in row:
            val = 0
            for d, hw in cell.walls.items():
                if hw: val += walls_map[d]
            r += f"{val:x}"
        hex_lines.append(r)
        
    matrix = build_visual_matrix(hex_lines)
    
    # Identify path cells from solution
    solution_cells = set()
    if show_path and maze_gen.get_solution_path():
        sol = maze_gen.get_solution_path()
        cx, cy = entry
        solution_cells.add((cx, cy))
        for step in sol:
            if step == 'N': cy -= 1
            elif step == 'S': cy += 1
            elif step == 'E': cx += 1
            elif step == 'W': cx -= 1
            solution_cells.add((cx, cy))

    celle_42 = maze_gen.celle_bloccate if hasattr(maze_gen, 'celle_bloccate') else set()

    height = len(hex_lines)
    width = len(hex_lines[0]) if height > 0 else 0

    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            # Trova quali celle logiche tocca questa coordinata (per i muri condivisi)
            y_indices = [(y - 1) // 2] if y % 2 == 1 else [(y - 2) // 2, y // 2]
            x_indices = [(x - 1) // 2] if x % 2 == 1 else [(x - 2) // 2, x // 2]
            
            touched_cells = [
                (lx, ly) for lx in x_indices for ly in y_indices
                if 0 <= lx < width and 0 <= ly < height
            ]
            
            touches_42 = any(c in celle_42 for c in touched_cells)
            
            logical_y = max(0, min((y - 1) // 2, height - 1))
            logical_x = max(0, min((x - 1) // 2, width - 1))
            center_coord = (logical_x, logical_y)
            
            char = matrix[y][x]
            
            # Palette di colori intercambiabili
            palette = ['🟥', '🟦', '🟧', '🟨', '🟩', '🟪', '🟫']
            
            # 3 Colori univoci assegnati in base al color_scheme
            color_path42 = palette[color_scheme % len(palette)]
            color_wall42 = palette[(color_scheme + 1) % len(palette)]
            color_solution = palette[(color_scheme + 2) % len(palette)]

            if touches_42 and char == '⬜':
                char = color_wall42
            elif center_coord in celle_42 and char == '⬛':
                char = color_path42
            elif center_coord == entry and char == '⬛':
                char = '🏁' # Start flag per non usare i quadrati colorati
            elif center_coord == exit_coords and char == '⬛':
                char = '🏠' # Traguardo per l'Exit per non usare i quadrati colorati
            elif center_coord in solution_cells and char == '⬛':
                char = color_solution

            # Stampa il carattere senza formattazioni o moltiplicatori perché gli emoji sono già 1:1 e colorati
            print(char, end="")
        print() # a capo fine riga
