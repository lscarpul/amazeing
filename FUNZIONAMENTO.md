# Funzionamento Generale del Progetto "a-maze-ing"

Questo documento spiega l'architettura e il flusso di esecuzione del progetto.

## Architettura a Moduli

Il progetto è diviso in due componenti principali per massimizzare la chiarezza e la riutilizzabilità del codice, seguendo una metafora di "Capo Cantiere" e "Ingegnere".

1.  **L'Applicazione (Il "Capo Cantiere")**:
    *   **File**: `a_maze_ing.py`
    *   **Ruolo**: Gestisce il flusso di lavoro di alto livello. È il punto di ingresso del programma.
    *   **Responsabilità**:
        *   Leggere e interpretare le istruzioni dal file `config.txt`.
        *   Validare i dati di input.
        *   Orchestrare le chiamate al "motore" del labirinto.
        *   Formattare i dati ricevuti dal motore nel formato di output richiesto (esadecimale).
        *   Scrivere il file di output finale (`maze.txt`).
        *   (In futuro) Gestire l'interfaccia utente e le interazioni.
    *   **Conoscenza**: Non conosce i dettagli complessi su *come* generare o risolvere un labirinto, sa solo a chi chiederlo.

2.  **Il Motore (L'"Ingegnere")**:
    *   **File**: `mazegen/generator.py`
    *   **Ruolo**: Contiene tutta la logica specializzata e gli algoritmi per la creazione e risoluzione dei labirinti.
    *   **Responsabilità**:
        *   Definire la struttura dati del labirinto (la griglia e le celle).
        *   Implementare l'algoritmo di generazione del labirinto (es. Recursive Backtracker).
        *   Implementare l'algoritmo per trovare il percorso più breve (es. Breadth-First Search).
        *   Fornire metodi chiari (`generate()`, `solve()`) che l'applicazione può chiamare.
    *   **Conoscenza**: È l'esperto. Sa esattamente come costruire e analizzare un labirinto, ma non si preoccupa di come i suoi risultati verranno presentati o da dove provengono le istruzioni iniziali.

## Flusso di Esecuzione: Passo dopo Passo

Quando un utente esegue il comando `python3 a_maze_ing.py config.txt`, si avvia la seguente catena di eventi:

1.  **Avvio e Lettura**:
    *   `a_maze_ing.py` viene eseguito.
    *   La funzione `parse_config` apre e legge il file `config.txt`.
    *   Le specifiche (dimensioni, entrata, uscita, nome del file di output) vengono caricate in un dizionario di configurazione.

2.  **Orchestrazione e Delega**:
    *   La funzione `main` in `a_maze_ing.py` prende le specifiche.
    *   Crea un'istanza della classe `MazeGenerator` dal modulo `mazegen`, passando le dimensioni e il seme (seed) come parametri. Questo è l'equivalente di "assumere l'ingegnere per un nuovo progetto".

3.  **Generazione del Labirinto**:
    *   `a_maze_ing.py` chiama il metodo `generate()` sull'oggetto `MazeGenerator`.
    *   All'interno di `mazegen/generator.py`, l'algoritmo **Recursive Backtracker (DFS)** si attiva:
        *   Parte da una cella, la segna come visitata.
        *   Sceglie un vicino non visitato a caso.
        *   Rimuove il muro tra la cella corrente e il vicino scelto.
        *   Si sposta sul vicino e ripete il processo.
        *   Se si trova in un vicolo cieco, torna indietro (backtracking) finché non trova un percorso alternativo.
        *   Il processo termina quando tutte le celle sono state visitate.

4.  **Risoluzione del Labirinto**:
    *   `a_maze_ing.py` chiama il metodo `solve()` sull'oggetto `MazeGenerator`, fornendo le coordinate di entrata e uscita.
    *   All'interno di `mazegen/generator.py`, l'algoritmo **Breadth-First Search (BFS)** si attiva:
        *   Usa una coda per esplorare il labirinto "a livelli" a partire dalla cella di ingresso.
        *   Tiene traccia del percorso per arrivare a ogni cella.
        *   La prima volta che raggiunge la cella di uscita, ha la garanzia di aver trovato uno dei percorsi più brevi.
        *   Il percorso viene ricostruito e salvato come una stringa di direzioni (es. "EESW...").

5.  **Finalizzazione e Scrittura**:
    *   `a_maze_ing.py` ora ha accesso al labirinto completo e alla sua soluzione tramite i metodi del `MazeGenerator`.
    *   La funzione `write_maze_to_file` viene chiamata.
    *   Questa funzione itera sulla griglia del labirinto, converte lo stato dei muri di ogni cella in un valore esadecimale e scrive il risultato nel file `maze.txt`.
    *   Infine, aggiunge al file la riga vuota, le coordinate di entrata/uscita e la stringa della soluzione.

Questo design modulare non solo rende il codice più facile da leggere e gestire, ma garantisce anche che il "motore" (`mazegen`) sia completamente indipendente e possa essere riutilizzato in qualsiasi altro progetto futuro che necessiti di un generatore di labirinti.

## Stato Attuale del Progetto (A che punto siamo)

In base alla pianificazione del lavoro tra Persona A (Motore) e Persona B (Applicazione), ecco un riepilogo dello stato dei lavori.

### ✅ Cosa abbiamo completato (Finito)
1. **Logica di Generazione (`mazegen`)**: Algoritmo *Recursive Backtracker* implementato e tradotto in italiano.
2. **Requisiti Speciali Labirinto**:
   - Inserimento forzato del pattern "42" (`_scolpisci_pattern_42`).
   - Evitamento proattivo di aree aperte grandi (max 2xN) (`_creerebbe_area_aperta`).
3. **Logica di Risoluzione (`mazegen`)**: Algoritmo *Breadth-First Search (BFS)* per calcolare il percorso ottimo dall'entrata all'uscita senza cicli.
4. **Struttura Base dell'App (`a_maze_ing.py`)**: Lettura file `config.txt`, gestione errori base e orchestrazione.
5. **Esportatore Esadecimale (`a_maze_ing.py`)**: Traduzione dello stato dei muri della griglia in stringhe esadecimali bit-a-bit richieste dal PDF per l'output in `maze.txt`.
6. **Infrastruttura**: Creazione di `Makefile`, `.gitignore` e `config.txt`.

### 🚧 Cosa manca teoricamente (I Prossimi Passi)
1. **Packaging del Modulo (Requisito Obbligatorio della *Persona A*)**:
   - Trasformare la cartella `mazegen/` in un vero modulo riutilizzabile Python.
   - Serve aggiungere i file `__init__.py` e `pyproject.toml` (oppure `setup.py`) per usare il pacchetto standard `build`.
   - Generare fisicamente i file di libreria `.whl` (wheels) installabili via `pip`.
2. **Visualizzazione Visiva/Interattiva (Requisito Obbligatorio della *Persona B*)**:
   - Creare un rendering ASCII su terminale (in `a_maze_ing.py`).
   - Aggiungere il "ciclo applicativo", dove il programma non muore subito, ma attende tasti in input per: *Rigenerare* (creare un nuovo maze) o *Mostrare/Nascondere* la via d'uscita a video.
3. **Pulizia Linting & Test**: Far girare `make lint` per essere sicuri che la sintassi passi rigorosamente `mypy` (i tipi statici esatti) e `flake8` senza crash.
