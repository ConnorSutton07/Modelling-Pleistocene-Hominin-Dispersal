from core.cell import Cell 
import numpy as np

class World:
    def __init__(self, shape: tuple):
        self.shape = shape
        self.cells = np.array([[None for i in range(self.shape[0])] for j in range(self.shape[1])], dtype = Cell)
        self.time_step = 0

    def step(self) -> None:
        cell_info = self.get_current_state()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                hexagonal_info = self.get_hexagonal_neighbor_info((i, j), cell_info)
                colonized_cell, dead = self.cells[i][j].update(hexagonal_info)
                if colonized_cell is not None:
                    pass
                    #self.cells[colonized_cell] = Cell()
                if dead:
                    self.cells[i][j].becomeExtinct()


        self.time_step += 1 

    def get_current_state(self) -> list:
        cell_info = [[None for i in range(self.shape[0])] for j in range(self.shape[1])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                cell_info[i][j] = self.cells[i][j].get_info()
        return cell_info


    def get_hexagonal_neighbor_info(self) -> dict:
        pass

    




