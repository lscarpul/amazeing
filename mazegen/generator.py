import random
from collections import deque
from typing import Optional, Set, Tuple, List, Any, Deque


class Cella:
    """
    Rappresenta una singola cella nella griglia del labirinto.
    Mantiene lo stato dei suoi muri e se è stata visitata.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visitata = False
        self.muri = {'N': True, 'E': True, 'S': True, 'W': True}


class GeneratoreLabirinto:
    """
    Classe principale per la generazione e risoluzione del labirinto.
    Implementa Recursive Backtracker e Breadth-First Search (BFS).
    """
    _PATTERN_4 = [
        [1, 0, 1],
        [1, 0, 1],
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
            seme: Optional[int] = None,
            perfetto: bool = True):
        self.larghezza = larghezza
        self.altezza = altezza
        self.perfetto = perfetto
        self.seme = seme

        self.griglia: List[List[Cella]] = []
        self.percorso_soluzione: Optional[str] = None
        self.celle_bloccate: Set[Tuple[int, int]] = set()
        self._inizializza_griglia()

    def _inizializza_griglia(self) -> None:
        """Crea la griglia iniziale piena di muri."""
        self.griglia = [[Cella(x, y) for x in range(self.larghezza)]
                        for y in range(self.altezza)]

    def get_grid(self) -> List[List[Any]]:
        """Restituisce la griglia del labirinto,
        convertita in formato compatibile con a_maze_ing."""
        class WrapperCella:
            def __init__(self, cella_interna: Cella) -> None:
                self.x = cella_interna.x
                self.y = cella_interna.y
                self.walls = cella_interna.muri
        return [[WrapperCella(c) for c in riga] for riga in self.griglia]

    def get_solution_path(self) -> Optional[str]:
        return self.percorso_soluzione

    def generate(self, start_x: int = 0, start_y: int = 0) -> None:
        """Avvia la generazione del labirinto."""
        random.seed(self.seme)

        for riga in self.griglia:
            for cella in riga:
                cella.visitata = False

        self._create_pattern_42()

        cella_partenza = self._trova_cella_partenza_valida(start_x, start_y)
        if cella_partenza is None:
            print(
                "Attenzione: Non è stato possibile "
                "trovare una cella di partenza valida.")
            return

        cella_partenza.visitata = True
        self._generazione_ricorsiva(cella_partenza)

        if not self.perfetto:
            self._rendi_imperfetto()

    def _rendi_imperfetto(self) -> None:
        """Rimuove casualmente alcuni muri interni
        per creare cicli (labirinto non perfetto)."""
        n_wall_to_rem = max(
            1, (self.larghezza * self.altezza) // 20)
        muri_rimossi = 0
        tentativi = 0

        while muri_rimossi < n_wall_to_rem and tentativi < n_wall_to_rem * 10:
            tentativi += 1
            x = random.randint(1, self.larghezza - 2)
            y = random.randint(1, self.altezza - 2)
            cella = self.griglia[y][x]

            dir_casuale = random.choice(['N', 'E', 'S', 'W'])

            if not cella.muri[dir_casuale]:
                continue

            cell_vicina = None
            if dir_casuale == 'N':
                cell_vicina = self.griglia[y - 1][x]
            elif dir_casuale == 'S':
                cell_vicina = self.griglia[y + 1][x]
            elif dir_casuale == 'E':
                cell_vicina = self.griglia[y][x + 1]
            elif dir_casuale == 'W':
                cell_vicina = self.griglia[y][x - 1]

            if cell_vicina and not self._check_open_area_creation(cella,
                                                                  cell_vicina):
                self._abbatti_muro(cella, cell_vicina)
                muri_rimossi += 1

    def _create_pattern_42(self) -> None:
        """Scolpisce il '42' nella griglia bloccandone lo spazio affinché
        le celle restino muri non attraversabili."""
        height_pattern = 5
        larghezza_4 = 3
        larghezza_2 = 3
        spazio = 1
        width_tot = larghezza_4 + spazio + larghezza_2

        if self.larghezza < width_tot + 2 or self.altezza < height_pattern + 2:
            print("Attenzione: Labirinto troppo "
                  "piccolo per contenere il pattern '42'.")
            return

        start_y = (self.altezza - height_pattern) // 2
        start_x = (self.larghezza - width_tot) // 2

        for y_pattern, riga_pattern in enumerate(self._PATTERN_4):
            for x_pattern, valore_blocco in enumerate(riga_pattern):
                if valore_blocco == 1:
                    cella = self.griglia[start_y +
                                         y_pattern][start_x + x_pattern]
                    cella.visitata = True
                    self.celle_bloccate.add((cella.x, cella.y))

        offset_x_2 = larghezza_4 + spazio
        for y_pattern, riga_pattern in enumerate(self._PATTERN_2):
            for x_pattern, valore_blocco in enumerate(riga_pattern):
                if valore_blocco == 1:
                    cella = self.griglia[start_y +
                                         y_pattern][start_x +
                                                    offset_x_2 + x_pattern]
                    cella.visitata = True
                    self.celle_bloccate.add((cella.x, cella.y))

    def _trova_cella_partenza_valida(
            self, start_x: int, start_y: int) -> Optional[Cella]:
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
        Controlla se l'abbattimento del muro tra
        due celle creerebbe un'area aperta massima 3x3.
        Sono ammesse aree 2x3 e 3x2,
        ma evitate rigidamente quelle 3x3
        (blocchi completi senza muri incrociati).
        """
        if cella_attuale.x == cella_vicina.x:
            dir_a, dir_b = (
                'S', 'N') if cella_attuale.y < cella_vicina.y else ('N', 'S')
        else:
            dir_a, dir_b = (
                'E', 'W') if cella_attuale.x < cella_vicina.x else ('W', 'E')

        prev_a = cella_attuale.muri[dir_a]
        prev_b = cella_vicina.muri[dir_b]

        cella_attuale.muri[dir_a] = False
        cella_vicina.muri[dir_b] = False

        crea_3x3 = False

        min_x = min(cella_attuale.x, cella_vicina.x)
        max_x = max(cella_attuale.x, cella_vicina.x)
        min_y = min(cella_attuale.y, cella_vicina.y)
        max_y = max(cella_attuale.y, cella_vicina.y)

        for start_x in range(max_x - 2, min_x + 1):
            for start_y in range(max_y - 2, min_y + 1):
                if (
                    0 <= start_x and start_x + 2 < self.larghezza
                    and 0 <= start_y and start_y + 2 < self.altezza
                ):
                    tutto_aperto = True
                    for y in range(start_y, start_y + 3):
                        for x in range(start_x, start_x + 2):
                            if self.griglia[y][x].muri['E']:
                                tutto_aperto = False
                                break
                        if not tutto_aperto:
                            break

                    if tutto_aperto:
                        for x in range(start_x, start_x + 3):
                            for y in range(start_y, start_y + 2):
                                if self.griglia[y][x].muri['S']:
                                    tutto_aperto = False
                                    break
                            if not tutto_aperto:
                                break

                    if tutto_aperto:
                        crea_3x3 = True
                        break
            if crea_3x3:
                break

        cella_attuale.muri[dir_a] = prev_a
        cella_vicina.muri[dir_b] = prev_b

        return crea_3x3

    def _abbatti_muro(self, cella_a: Cella, cella_b: Cella) -> None:
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

    def _generazione_ricorsiva(self, cella_attuale: Cella) -> None:
        vicini = self._vicini_non_visitati(cella_attuale)
        random.shuffle(vicini)

        for vicino in vicini:
            if not vicino.visitata:
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

        coda: Deque[Tuple[Cella, List[str]]] = deque([(cella_partenza, [])])

        visitate = {cella_partenza}

        while coda:
            cella_corrente, percorso_corrente = coda.popleft()

            if cella_corrente == cella_arrivo:
                self.percorso_soluzione = "".join(percorso_corrente)
                return True

            vicini_aperti = self._vicini_raggiungibili(cella_corrente)

            for direzione, vicino in vicini_aperti.items():
                if vicino not in visitate:
                    visitate.add(vicino)
                    nuovo_percorso = percorso_corrente + [direzione]
                    coda.append((vicino, nuovo_percorso))

        self.percorso_soluzione = ""
        return False

    def _vicini_raggiungibili(self, cella: Cella) -> dict[str, Cella]:
        """
        Trova le celle adiacenti a cui è possibile accedere (muro aperto).
        Restituisce un dizionario con la direzione come chiave
        ('N', 'S', 'E', 'W').
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


MazeGenerator = GeneratoreLabirinto
