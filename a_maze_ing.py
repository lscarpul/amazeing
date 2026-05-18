import sys
from mazegen.generator import MazeGenerator
from graf.printlab import render_interactive

# Mappa per la conversione dei muri in valori binari per l'output esadecimale.
# Ogni muro ha un valore di bit specifico come da requisiti.
WALL_TO_BIT = {
    'N': 1,  # Bit 0
    'E': 2,  # Bit 1
    'S': 4,  # Bit 2
    'W': 8,  # Bit 3
}

sys.setrecursionlimit(10000)


def parse_config(config_file):
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
                # Ignora le righe vuote e i commenti (che iniziano con #)
                if line and not line.startswith('#'):
                    # Tenta di dividere la riga in chiave e valore
                    if '=' not in line:
                        raise ValueError(
                            f"La linea {line_num} non contiene '='")
                    key, value = line.split('=', 1)
                    # Salva la configurazione nel dizionario
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        # Se il file non esiste, stampa un errore e termina
        print(f"Errore: File di configurazione '{config_file}' non trovato.")
        sys.exit(1)
    except ValueError as e:
        # Se una riga ha un formato non valido, stampa un errore e termina
        print(f"Errore nel file di configurazione: {e}")
        sys.exit(1)
    return config


def write_maze_to_file(maze_gen, output_file, entry, exit):
    """
    Converte il labirinto in formato esadecimale e lo scrive su un file.
    Aggiunge anche le coordinate di entrata/uscita e il percorso della soluzione.
    """
    try:
        with open(output_file, 'w') as f:
            # Itera su ogni riga della griglia del labirinto
            for row in maze_gen.get_grid():
                hex_row = []
                # Itera su ogni cella della riga
                for cell in row:
                    # Calcola il valore numerico della cella basato sui suoi
                    # muri
                    cell_value = 0
                    for direction, has_wall in cell.walls.items():
                        # Se un muro esiste (è chiuso), aggiungi il suo valore
                        # di bit
                        if has_wall:
                            cell_value += WALL_TO_BIT[direction]

                    # Converte il valore in una singola cifra esadecimale e la
                    # aggiunge alla riga
                    hex_row.append(f"{cell_value:x}")

                # Scrive la riga di caratteri esadecimali nel file, seguita da
                # un a capo
                f.write("".join(hex_row) + "\n")

            # Aggiunge una riga vuota come separatore, come da requisito
            f.write("\n")

            # Scrive le coordinate di entrata e uscita
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")

            # Scrive il percorso della soluzione
            solution = maze_gen.get_solution_path()
            f.write(f"{solution}\n")

    except IOError as e:
        # Gestisce eventuali errori di scrittura del file
        print(f"Errore durante la scrittura del file '{output_file}': {e}")
        sys.exit(1)


def main():
    """
    Funzione principale dell'applicazione.
    Orchestra la lettura della configurazione, la generazione del labirinto,
    la sua risoluzione e la scrittura del file di output.
    """
    # Controlla che sia stato fornito un solo argomento (il file di
    # configurazione)
    if len(sys.argv) != 2:
        print("Uso: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    # Ottiene il nome del file di configurazione dagli argomenti della riga di
    # comando
    config_file = sys.argv[1]
    # Analizza il file di configurazione e ottiene un dizionario
    config = parse_config(config_file)

    try:
        # --- Lettura e validazione dei parametri di configurazione ---
        # Converte larghezza e altezza in interi
        width = int(config['WIDTH'])
        height = int(config['HEIGHT'])

        # Legge le coordinate di entrata, le divide e le converte in interi
        entry_coords = tuple(map(int, config['ENTRY'].split(',')))
        # Legge le coordinate di uscita
        exit_coords = tuple(map(int, config['EXIT'].split(',')))

        # Ottiene il nome del file di output
        output_file = config['OUTPUT_FILE']

        # Legge il flag 'PERFECT' e lo converte in un booleano
        is_perfect = config['PERFECT'].lower() == 'true'

        # Legge il seme per la generazione casuale (opzionale)
        # Se 'SEED' non è presente, `config.get` restituisce None
        seed = config.get('SEED')
        if seed:
            seed = int(seed)

        # --- Logica di Scrittura File Iniziale ---
        maze_generator = MazeGenerator(width, height, seed, is_perfect)
        maze_generator.generate()
        maze_generator.solve(entry_coords, exit_coords)
        write_maze_to_file(maze_generator, output_file, entry_coords, exit_coords)

        # --- Ciclo Applicativo (Persona B) ---
        show_path = False
        color_scheme = 0
        
        while True:
            # Crea un po' di spazio tra una stampa e l'altra
            print("\n\n\n")
            
            # Stampa la matrice visiva
            render_interactive(maze_generator, entry_coords, exit_coords, show_path, color_scheme)
            
            # Stampa menu testuale
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
                # Nuova generazione, ignora il seed per garantirne uno nuovo
                maze_generator = MazeGenerator(width, height, None, is_perfect)
                maze_generator.generate()
                maze_generator.solve(entry_coords, exit_coords)
                write_maze_to_file(maze_generator, output_file, entry_coords, exit_coords)
            elif choice == '2':
                show_path = not show_path
            elif choice == '3':
                color_scheme = (color_scheme + 1) % 7
            elif choice == '4':
                break
            else:
                pass # Ignora scelte non valide

        print("\nOperazione completata con successo!")

    except KeyError as e:
        # Se una chiave obbligatoria manca nel file di configurazione
        print(f"Errore: Chiave di configurazione mancante: {e}")
        sys.exit(1)
    except (ValueError, IndexError) as e:
        # Se un valore ha un formato non corretto (es. "a,b" per coordinate, o
        # testo invece di numero)
        print(f"Errore: Valore di configurazione non valido: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Il punto di ingresso del programma: se lo script è eseguito
    # direttamente, chiama la funzione main
    main()
