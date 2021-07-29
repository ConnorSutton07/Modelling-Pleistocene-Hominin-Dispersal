import numpy as np
from numpy.random import random, choice, normal
from settings import α, ß

class Cell:
    """
    Cell class for cellular automata simulation
    Uses probabilities of extinction and colonization to spread about world
    Incorporates genetic data to distinguish cell populations

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

    def __init__(self, active: bool, P_ext: float = None, P_col: float = None):
        """
        Initializes a new, unoccupied Cell.

        """       
        self.active = active 
        self.occupied = False 
        self.P_ext = P_ext 
        self.P_col = P_col 
        self.genotype = None
        self.mutation_vector = None

    def is_occupied(self) -> bool:
        return self.occupied
        
    def become_occupied(self, 
                       genotype: np.array = np.array([128.0, 128.0, 128.0], dtype = float), 
                       mutation_vector: np.array = None
                       ) -> None:
        """
        Cell becomes occupied, and inhabitor's genotype and mutation vector are set.

        If these are unspecified, then this must be an intitial population; 
        in this case, a default genotype and random mutation vector are used

        """
        self.occupied = True
        self.genotype = genotype
        if mutation_vector is None:
            self.mutation_vector = np.array([random() for _ in range(3)])
        else:
            self.mutation_vector = mutation_vector + np.array([normal(scale = ß) for _ in range(3)])
        self.mutation_vector = self.mutation_vector / np.linalg.norm(self.mutation_vector)
        
    def become_extinct(self) -> None:
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
        # update genotype
        neighbor_genotypes = np.array([neighbor['genotype'] for neighbor in neighbor_info if neighbor is not None]).T 
        avgs = np.array([np.mean(neighbor_genotypes[0]), np.mean(neighbor_genotypes[1]), np.mean(neighbor_genotypes[2])])
        self.genotype = ((self.genotype + avgs) / 2) + (self.mutation_vector * α)

        # attempt to colonize
        colonized_cell = None 
        coloized = False
        unoccupied_neighbors = [(neighbor['location'], neighbor['P_col)']) for neighbor in neighbor_info if neighbor is not None]
        if len(unoccupied_neighbors > 0):
            cell_to_colonize = choice(unoccupied_neighbors)
            if random() < cell_to_colonize[1]:
                colonized_cell = cell_to_colonize[0]
                coloized = True

        # maybe die
        dead = True if random() < (self.P_ext + (0.15 * colonized)) else False

        return colonized_cell, dead