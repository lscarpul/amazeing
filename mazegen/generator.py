import random
from collections import deque


class Cella:
    """
    Rappresenta una singola cella nella griglia del labirinto.
    Mantiene lo stato dei suoi muri e se è stata visitata.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visitata = False
        # Inizialmente tutti i muri sono intatti (True)
        self.muri = {'N': True, 'E': True, 'S': True, 'W': True}


class GeneratoreLabirinto:
    """
    Classe principale per la generazione e risoluzione del labirinto.
    Implementa Recursive Backtracker e Breadth-First Search (BFS).
    """
    # Pattern per il "4" e il "2" da scolpire nel labirinto.
    # 1 rappresenta un muro chiuso permanente, 0 uno spazio da generare.
    _PATTERN_4 = [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ]
    _PATTERN_2 = [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
    ]

    def __init__(
            self,
            larghezza: int,
            altezza: int,
            seme: int = None,
            perfetto: bool = True):
        self.larghezza = larghezza
        self.altezza = altezza
        self.perfetto = perfetto
        if seme is not None:
            random.seed(seme)

        self.griglia: list[list[Cella]] = []
        self.percorso_soluzione = None
        self.celle_bloccate = set()
        self._inizializza_griglia()

    def _inizializza_griglia(self):
        """Crea la griglia iniziale piena di muri."""
        self.griglia = [[Cella(x, y) for x in range(self.larghezza)]
                        for y in range(self.altezza)]

    def get_grid(self):
        """Restituisce la griglia del labirinto, convertita in formato compatibile con a_maze_ing."""
        # Mantengo compatibilità con l'oggetto Cell e le chiavi in inglese
        # attese fuori
        class WrapperCella:
            def __init__(self, cella_interna):
                self.x = cella_interna.x
                self.y = cella_interna.y
                self.walls = cella_interna.muri
        return [[WrapperCella(c) for c in riga] for riga in self.griglia]

    def get_solution_path(self):
        return self.percorso_soluzione

    def generate(self, start_x: int = 0, start_y: int = 0) -> None:
        """Avvia la generazione del labirinto."""
        for riga in self.griglia:
            for cella in riga:
                cella.visitata = False

        # 1. Scolpisci il pattern "42" prima di iniziare la generazione
        self._create_pattern_42()

        # 2. Trova una cella di partenza valida che non sia bloccata
        cella_partenza = self._trova_cella_partenza_valida(start_x, start_y)
        if cella_partenza is None:
            print(
                "Attenzione: Non è stato possibile trovare una cella di partenza valida.")
            return

        cella_partenza.visitata = True
        self._generazione_ricorsiva(cella_partenza)

        if not self.perfetto:
            self._rendi_imperfetto()

    def _rendi_imperfetto(self):
        """Rimuove casualmente alcuni muri interni per creare cicli (labirinto non perfetto)."""
        numero_muri_da_rimuovere = max(
            1, (self.larghezza * self.altezza) // 20)
        muri_rimossi = 0
        tentativi = 0

        while muri_rimossi < numero_muri_da_rimuovere and tentativi < numero_muri_da_rimuovere * 10:
            tentativi += 1
            x = random.randint(1, self.larghezza - 2)
            y = random.randint(1, self.altezza - 2)
            cella = self.griglia[y][x]

            # Scegli una direzione casuale per il muro
            dir_casuale = random.choice(['N', 'E', 'S', 'W'])

            # Non abbattere se il muro non c'è già,
            # oppure se cerchiamo di abbattere i bordi esterni
            if not cella.muri[dir_casuale]:
                continue

            cella_vicina = None
            if dir_casuale == 'N':
                cella_vicina = self.griglia[y - 1][x]
            elif dir_casuale == 'S':
                cella_vicina = self.griglia[y + 1][x]
            elif dir_casuale == 'E':
                cella_vicina = self.griglia[y][x + 1]
            elif dir_casuale == 'W':
                cella_vicina = self.griglia[y][x - 1]

            # Controlla per non unire percorsi che formino inavvertitamente
            # piazze enormi (se vuoi esserne sicuro)
            # Non rimuovere muri che coinvolgono le celle bloccate (pattern 42)
            if (cella.x, cella.y) in self.celle_bloccate or (cella_vicina.x, cella_vicina.y) in self.celle_bloccate:
                continue

            if not self._check_open_area_creation(cella, cella_vicina):
                self._abbatti_muro(cella, cella_vicina)
                muri_rimossi += 1

    def _create_pattern_42(self):
        """Scolpisce il '42' nella griglia bloccandone lo spazio affinché le celle restino muri non attraversabili."""
        altezza_pattern = 5
        larghezza_4 = 3
        larghezza_2 = 3
        spazio = 1
        larghezza_totale = larghezza_4 + spazio + larghezza_2

        if self.larghezza < larghezza_totale + 2 or self.altezza < altezza_pattern + 2:
            print("Attenzione: Labirinto troppo piccolo per contenere il pattern '42'.")
            return

        start_y = (self.altezza - altezza_pattern) // 2
        start_x = (self.larghezza - larghezza_totale) // 2

        # Pattern 4
        for y_pattern, riga_pattern in enumerate(self._PATTERN_4):
            for x_pattern, valore_blocco in enumerate(riga_pattern):
                if valore_blocco == 1:
                    cella = self.griglia[start_y + y_pattern][start_x + x_pattern]
                    # Segnamola come visitata così il generatore DFS non romperà muri qui dentro
                    cella.visitata = True
                    self.celle_bloccate.add((cella.x, cella.y))

        # Pattern 2
        offset_x_2 = larghezza_4 + spazio
        for y_pattern, riga_pattern in enumerate(self._PATTERN_2):
            for x_pattern, valore_blocco in enumerate(riga_pattern):
                if valore_blocco == 1:
                    cella = self.griglia[start_y + y_pattern][start_x + offset_x_2 + x_pattern]
                    cella.visitata = True
                    self.celle_bloccate.add((cella.x, cella.y))

    def _trova_cella_partenza_valida(
            self, start_x: int, start_y: int) -> Cella:
        if not self.griglia[start_y][start_x].visitata:
            return self.griglia[start_y][start_x]

        for y in range(self.altezza):
            for x in range(self.larghezza):
                if not self.griglia[y][x].visitata:
                    return self.griglia[y][x]
        return None

    def _check_open_area_creation(
            self,
            cella_attuale: Cella,
            cella_vicina: Cella) -> bool:
        """
        Controlla se l'abbattimento del muro tra due celle creerebbe un'area aperta (es. un blocco 2x2 senza muri incrociati).
        Poiché i corridoi sono larghi 1, l'unico modo per avere uno spazio 3x3 è passare prima da un 2x2.
        Bloccando il 2x2, rispettiamo rigorosamente la regola.
        """
        dx = cella_vicina.x - cella_attuale.x
        dy = cella_vicina.y - cella_attuale.y

        # Se ci muoviamo orizzontalmente (Est o Ovest)
        if dx != 0:
            # Controlla sopra
            if cella_attuale.y > 0 and cella_vicina.y > 0:
                adiacente_attuale = self.griglia[cella_attuale.y -
                                                 1][cella_attuale.x]
                adiacente_vicina = self.griglia[cella_vicina.y -
                                                1][cella_vicina.x]
                # Se il muro sopra della cella_attuale e della cella_vicina è
                # aperto, E il muro tra le adiacenti è aperto
                if not cella_attuale.muri['N'] and not cella_vicina.muri[
                        'N'] and not adiacente_attuale.muri['E' if dx == 1 else 'W']:
                    return True
            # Controlla sotto
            if cella_attuale.y < self.altezza - 1 and cella_vicina.y < self.altezza - 1:
                adiacente_attuale = self.griglia[cella_attuale.y +
                                                 1][cella_attuale.x]
                adiacente_vicina = self.griglia[cella_vicina.y +
                                                1][cella_vicina.x]
                if not cella_attuale.muri['S'] and not cella_vicina.muri[
                        'S'] and not adiacente_attuale.muri['E' if dx == 1 else 'W']:
                    return True

        # Se ci muoviamo verticalmente (Nord o Sud)
        if dy != 0:
            # Controlla a sinistra
            if cella_attuale.x > 0 and cella_vicina.x > 0:
                adiacente_attuale = self.griglia[cella_attuale.y][cella_attuale.x - 1]
                adiacente_vicina = self.griglia[cella_vicina.y][cella_vicina.x - 1]
                if not cella_attuale.muri['W'] and not cella_vicina.muri[
                        'W'] and not adiacente_attuale.muri['S' if dy == 1 else 'N']:
                    return True
            # Controlla a destra
            if cella_attuale.x < self.larghezza - 1 and cella_vicina.x < self.larghezza - 1:
                adiacente_attuale = self.griglia[cella_attuale.y][cella_attuale.x + 1]

                if not cella_attuale.muri['E'] and not cella_vicina.muri[
                        'E'] and not adiacente_attuale.muri['S' if dy == 1 else 'N']:
                    return True

        return False

    def _abbatti_muro(self, cella_a: Cella, cella_b: Cella):
        dx = cella_b.x - cella_a.x
        dy = cella_b.y - cella_a.y
        if dx == 1:
            cella_a.muri['E'] = False
            cella_b.muri['W'] = False
        elif dx == -1:
            cella_a.muri['W'] = False
            cella_b.muri['E'] = False
        elif dy == 1:
            cella_a.muri['S'] = False
            cella_b.muri['N'] = False
        elif dy == -1:
            cella_a.muri['N'] = False
            cella_b.muri['S'] = False

    def _vicini_non_visitati(self, cella: Cella) -> list[Cella]:
        vicini = []
        if cella.y > 0 and not self.griglia[cella.y - 1][cella.x].visitata:
            vicini.append(self.griglia[cella.y - 1][cella.x])
        if cella.x < self.larghezza - \
                1 and not self.griglia[cella.y][cella.x + 1].visitata:
            vicini.append(self.griglia[cella.y][cella.x + 1])
        if cella.y < self.altezza - \
                1 and not self.griglia[cella.y + 1][cella.x].visitata:
            vicini.append(self.griglia[cella.y + 1][cella.x])
        if cella.x > 0 and not self.griglia[cella.y][cella.x - 1].visitata:
            vicini.append(self.griglia[cella.y][cella.x - 1])
        return vicini

    def _generazione_ricorsiva(self, cella_attuale: Cella):
        vicini = self._vicini_non_visitati(cella_attuale)
        random.shuffle(vicini)

        for vicino in vicini:
            if not vicino.visitata:
                # Controlla per impedire di creare aree aperte (es. 2x2 e
                # conseguentemente 3x3)
                if not self._check_open_area_creation(cella_attuale, vicino):
                    self._abbatti_muro(cella_attuale, vicino)
                    vicino.visitata = True
                    self._generazione_ricorsiva(vicino)

    def solve(self, entrata: tuple[int, int], uscita: tuple[int, int]) -> bool:
        """
        Risolve il labirinto usando l'algoritmo Breadth-First Search (BFS).
        Restituisce True se trova un percorso, False altrimenti.
        """
        start_x, start_y = entrata
        end_x, end_y = uscita

        cella_partenza = self.griglia[start_y][start_x]
        cella_arrivo = self.griglia[end_y][end_x]

        # La coda per la BFS: contiene tuple (Cella_Attuale, Percorso_Fino_Ad_Ora)
        # Il percorso è una lista di stringhe direzionali (es. ['N', 'E', 'S'])
        coda = deque([(cella_partenza, [])])

        # Insieme per tenere traccia delle celle già esplorate per evitare
        # cicli infiniti
        visitate = {cella_partenza}

        while coda:
            cella_corrente, percorso_corrente = coda.popleft()

            # Se abbiamo raggiunto l'uscita, salviamo il percorso come stringa
            # e terminiamo
            if cella_corrente == cella_arrivo:
                self.percorso_soluzione = "".join(percorso_corrente)
                return True

            # Ottiene tutti i vicini raggiungibili (senza muri in mezzo)
            vicini_aperti = self._vicini_raggiungibili(cella_corrente)

            for direzione, vicino in vicini_aperti.items():
                if vicino not in visitate:
                    visitate.add(vicino)
                    # Aggiunge il vicino alla coda con il nuovo percorso
                    # aggiornato
                    nuovo_percorso = percorso_corrente + [direzione]
                    coda.append((vicino, nuovo_percorso))

        # Se la coda si svuota senza aver trovato l'uscita
        self.percorso_soluzione = ""
        return False

    def _vicini_raggiungibili(self, cella: Cella) -> dict[str, Cella]:
        """
        Trova le celle adiacenti a cui è possibile accedere (muro aperto).
        Restituisce un dizionario con la direzione come chiave ('N', 'S', 'E', 'W').
        """
        raggiungibili = {}
        x, y = cella.x, cella.y

        if not cella.muri['N'] and y > 0:
            raggiungibili['N'] = self.griglia[y - 1][x]
        if not cella.muri['E'] and x < self.larghezza - 1:
            raggiungibili['E'] = self.griglia[y][x + 1]
        if not cella.muri['S'] and y < self.altezza - 1:
            raggiungibili['S'] = self.griglia[y + 1][x]
        if not cella.muri['W'] and x > 0:
            raggiungibili['W'] = self.griglia[y][x - 1]

        return raggiungibili


# L'esportatore esterno continua ad utilizzare "MazeGenerator"
MazeGenerator = GeneratoreLabirinto
