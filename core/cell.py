import numpy as np
from settings import α, ß

class Cell:
    def __init__(self, 
                 active: bool, 
                 P_ext: float, 
                 P_col: float, 
                 genotype: np.array = np.array([128.0, 128.0, 128.0], dtype = float), 
                 mutation_vector: np.array = None):
        """
        Initializes a new, unoccupied Cell.

          Attributes
        --------------
        active: bool
            Determines whether this cell participates in the simulation
        P_ext: float
            Probability of extinction of an inhabiting member at every time step; based on vegetation class
        P_col: float
            Probabiltiy of colonization by an occupied neighborign cell at every time step, based on altitude
        genotype: np.array([float, float, float])
            Genetic information in the range [0, 255] that corresponds to color
        mutation_vector: np.array([float, float, float])
            The genetic shift at every time step

        """       
        self.active = active 
        self.occupied = False 
        self.P_ext = P_ext 
        self.P_col = P_col 
        self.genotype = genotype
        self.mutation_vector = mutation_vector if mutation_vector is not None else None # add noise to this

    def isOccupied(self) -> bool:
        return self.occupied
        
    def becomeOccupied(self, genotype: np.array, mutation_vector: np.array) -> None:
        self.occupied = True
        self.genotype = genotype
        self.mutation_vector = mutation_vector
        
    def becomeExtinct(self) -> None:
        """ 
        Resets all attributes that are dependent on the current inhabitor
        i.e., the probabilities of extinction or colonization remain constant
        as they depend only on the geopgraphic position of the cell.

        """
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
    
    def update(self, neighbor_info: list): # called each time step if cell is active and populated
        """
        Update that occurs once per time step for each occupied cell
        Process:
            1. Update genotype
            2. Attempt to colonize vacant neighbor
            3. (Maybe) Die

        """
        neighbor_genotypes = np.array([neighbor['genotype'] for neighbor in neighbor_info if neighbor is not None])

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