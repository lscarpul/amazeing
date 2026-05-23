import sys
from mazegen.generator import MazeGenerator
from graf.printlab import render_interactive

from typing import Dict, Tuple, Any

WALL_TO_BIT = {
    'N': 1,
    'E': 2,
    'S': 4,
    'W': 8,
}

sys.setrecursionlimit(10000)


def parse_config(config_file: str) -> Dict[str, str]:
    """
    Legge e analizza il file di configurazione.
    Restituisce un dizionario con le configurazioni.
    Gestisce gli errori di base come file non trovato o formato non valido.
    """
    config = {}
    try:
        with open(config_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' not in line:
                        raise ValueError(
                            f"La linea {line_num} non contiene '='")
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Errore: File di configurazione '{config_file}' non trovato.")
        sys.exit(1)
    except ValueError as e:
        print(f"Errore nel file di configurazione: {e}")
        sys.exit(1)
    return config


def write_maze_to_file(maze_gen: Any, output_file: str,
                       entry: Tuple[int, int], exit: Tuple[int, int]) -> None:
    """
    Converte il labirinto in formato esadecimale e lo scrive su un file.
    Aggiunge anche le coordinate di entry/exit e il percorso della soluzione.
    """
    try:
        with open(output_file, 'w') as f:
            for row in maze_gen.get_grid():
                hex_row = []
                for cell in row:
                    cell_value = 0
                    for direction, has_wall in cell.walls.items():
                        if has_wall:
                            cell_value += WALL_TO_BIT[direction]
                    hex_row.append(f"{cell_value:x}")
                f.write("".join(hex_row) + "\n")

            f.write("\n")

            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")

            solution = maze_gen.get_solution_path()
            f.write(f"{solution}\n")

    except IOError as e:
        print(f"Errore durante la scrittura del file '{output_file}': {e}")
        sys.exit(1)


def main() -> None:
    """
    Funzione principale dell'applicazione.
    Orchestra la lettura della configurazione, la generazione del labirinto,
    la sua risoluzione e la scrittura del file di output.
    """
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    config = parse_config(config_file)

    try:
        width = int(config['WIDTH'])
        height = int(config['HEIGHT'])
        if width <= 0 or height <= 0:
            raise ValueError("WIDTH and HEIGHT must be strictly positive.")

        entry_list = list(map(int, config['ENTRY'].split(',')))
        if len(entry_list) != 2:
            raise ValueError("ENTRY must have two coordinates.")
        entry_coord: Tuple[int, int] = (entry_list[0], entry_list[1])
        if not (0 <= entry_coord[0] < width and 0 <= entry_coord[1] < height):
            raise ValueError("ENTRY is outside the maze bounds.")

        exit_list = list(map(int, config['EXIT'].split(',')))
        if len(exit_list) != 2:
            raise ValueError("EXIT must have two coordinates.")
        exit_coords: Tuple[int, int] = (exit_list[0], exit_list[1])
        if not (0 <= exit_coords[0] < width and 0 <= exit_coords[1] < height):
            raise ValueError("EXIT is outside the maze bounds.")

        output_file = config['OUTPUT_FILE']

        perfect_str = config['PERFECT'].lower()
        if perfect_str not in ['true', 'false']:
            raise ValueError("PERFECT must be 'true' or 'false'.")
        is_perfect = (perfect_str == 'true')

        seed_str = config.get('SEED')
        seed = int(seed_str) if seed_str is not None else None

        maze_generator = MazeGenerator(width, height, seed, is_perfect)
        maze_generator.generate()
        maze_generator.solve(entry_coord, exit_coords)
        write_maze_to_file(maze_generator, output_file,
                           entry_coord, exit_coords)

        show_path = False
        color_scheme = 0

        while True:
            print("\n\n\n")

            render_interactive(maze_generator, entry_coord,
                               exit_coords, show_path, color_scheme)

            print("==== A-Maze-ing ====")
            print("Where you start from: 🏁 \nWhere you are going to:🏠 ")
            print("1. Re-generate a new random maze (ignore given seed)")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")

            try:
                choice = input("Choice? (1-4): ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if choice == '1':
                maze_generator = MazeGenerator(width, height, None, is_perfect)
                maze_generator.generate()
                maze_generator.solve(entry_coord, exit_coords)
                write_maze_to_file(maze_generator, output_file,
                                   entry_coord, exit_coords)
            elif choice == '2':
                show_path = not show_path
            elif choice == '3':
                color_scheme = (color_scheme + 1) % 7
            elif choice == '4':
                break
            else:
                pass

        print("\nOperazione completata con successo!")

    except KeyError as e:
        print(f"Errore: Chiave di configurazione mancante: {e}")
        sys.exit(1)
    except (ValueError, IndexError) as e:
        print(f"Errore: Valore di configurazione non valido: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
