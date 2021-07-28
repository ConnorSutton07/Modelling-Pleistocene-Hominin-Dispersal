import numpy as np

class Cell:
    def __init__(self, 
                 active: bool, 
                 P_ext: float, 
                 P_col: float, 
                 genotype: np.array = np.array([128.0, 128.0, 128.0]), 
                 mutation_vector: np.array = None):
        """

        """       
        self.active = active # ignored in simulation if false
        self.occupied = False # initalize all cells to unoccupied
        self.P_ext = P_ext + np.random.normal(0) # probability of extinction based on vegetation
        self.P_col = P_col + np.random.normal(0) # probability of colonization based on altitude
        self.genotype = genotype
        self.mutation_vector = mutation_vector if mutation_vector is not None else None # add noise to this
        
    def becomeOccupied(self, genotype: np.array, mutation_vector: np.array) -> None:
        self.occupied = True
        self.genotype = genotype
        self.mutation_vector = mutation_vector
        
    def becomeExtinct(self) -> None:
        self.occupied = False
        self.genotype = None 
        self.mutation_vector = None
        
    def get_info(self) -> dict:
        return None if not self.active else {
            'genotype':        self.genotype,
            'mutation-vector': self.mutation_vector,
            'P_col':           self.P_col,
            'P_ext':           self.P_ext,
            'occupied':        self.occupied
        }
    
    def update(self, info: list): # called each time step if cell is active and populated
        pass
        # self.P_density_ext = self.checkPopulationDensity(e) 
        # self.P_ext = self.P_ext + self.elv_P_ext + self.density_P_ext # update probability of extinction
        # #e.cells[self.x][self.y].P_ext = self.P_ext
        # if (self.active and self.occupied):
        #     if (random() < p_col):
        #         potential_directions = self.getValidNeighboringCells(e)
        #         if (len(potential_directions) > 0):
        #             direction = potential_directions[int(random() * len(potential_directions))]
        #             self.colonizeNeighbor(direction, e)
        #     if (random() < self.P_ext):
        #         self.becomeExtinct()