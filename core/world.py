from core.cell import Cell 
import numpy as np
from icecream import ic

class HexagonalWorld:
    """
    Hexagonal grid spice containing a population of cells

       Attributes
    ----------------
    shape: tuple(N, M)
        N x M shape of cell grid
    cells: np.array
        The grid of cells
    time_step: int
        number of time steps since world creation

    """
    def __init__(self, shape: tuple):
        self.shape = shape
        self.cells = np.array([[None for i in range(self.shape[1])] for j in range(self.shape[0])], dtype = Cell)
        self.time_step = 0

    def create_cell(self, index, active: bool, P_ext: float = None, P_col: float = None) -> None:
        self.cells[index] = Cell(active, P_ext, P_col)

    def populate(self, index) -> None:
        self.cells[index].become_occupied()

    def step(self) -> None:
        cell_info = self.get_current_state()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                #if self.cells[i][j].is_occupied():
                if cell_info[i][j] is not None and cell_info[i][j]['occupied']:
                    hexagonal_info = self.get_hexagonal_neighbor_info(i, j, cell_info)
                    colonized_cell, dead = self.cells[i][j].update(hexagonal_info)
                    if colonized_cell is not None:
                        self.cells[colonized_cell].become_occupied(cell_info[i][j]['genotype'], cell_info[i][j]['mutation-vector'])
                    if dead:
                        self.cells[i][j].become_extinct()
        self.time_step += 1 

    def get_current_state(self) -> list:
        cell_info = [[None for i in range(self.shape[1])] for j in range(self.shape[0])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                cell_info[i][j] = self.cells[i][j].get_info()
                if cell_info[i][j] is not None: cell_info[i][j].update({'location': (i, j)})
        return cell_info


    def get_hexagonal_neighbor_info(self, i, j, cell_info) -> dict:
        """ 
        Retrieves the info of cells in a hexagonal neighborhood around the given index.
        Scheme:

          [2] [4]
        [1] [3] [5]              [1][2][3][4][5]
          [7] [9]        ->      [6][7][8][9][A]
        [6] [8] [A]                 [B]   [C]
          [B] [C]

        """
        hexagonal_info = []
        for a in range(-1, 1):
            for b in range(-1, 2):
                if not (a == b == 0): 
                    hexagonal_info.append(cell_info[i + a][j + b])
        hexagonal_info.append(cell_info[i + 1][j])
        return hexagonal_info


    




