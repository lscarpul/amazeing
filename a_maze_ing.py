import sys
from mazegen.generator import MazeGenerator

# Mappa per la conversione dei muri in valori binari per l'output esadecimale.
# Ogni muro ha un valore di bit specifico come da requisiti.
WALL_TO_BIT = {
    'N': 1,  # Bit 0
    'E': 2,  # Bit 1
    'S': 4,  # Bit 2
    'W': 8,  # Bit 3
}


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

        # --- Logica di Orchestrazione ---
        print("1. Configurazione caricata. Inizio la generazione del labirinto...")

        # 1. Crea un'istanza del generatore di labirinti con i parametri letti
        maze_generator = MazeGenerator(width, height, seed, is_perfect)

        # 2. Chiama il metodo per generare la struttura del labirinto
        maze_generator.generate()
        print("2. Labirinto generato.")

        # 3. Chiama il metodo per trovare il percorso più breve dall'entrata
        # all'uscita
        if maze_generator.solve(entry_coords, exit_coords):
            print("3. Soluzione trovata.")
        else:
            print(
                "3. Attenzione: Non è stata trovata una soluzione tra entrata e uscita.")

        # 4. Scrive il labirinto generato e la soluzione nel file di output
        write_maze_to_file(
            maze_generator,
            output_file,
            entry_coords,
            exit_coords)
        print(f"4. Labirinto e soluzione scritti nel file '{output_file}'.")

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
