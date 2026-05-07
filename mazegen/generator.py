# mazegen/generator.py

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}

class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[Cell]] = []
        self._initialize_grid()
    
    def _initialize_grid(self):
         self.grid = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]

    def generate(self) -> None:

        pass
    
    def solve(self, entry: tuple[int, int], exit: tuple[int, int]) -> none:

        pass
    
    def get_solution(self) -> str:

        return ""
