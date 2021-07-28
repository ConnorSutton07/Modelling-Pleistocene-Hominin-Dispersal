from core.cell import Cell 

class World:
    def __init__(self, shape: tuple):
        self.cells = cells = np.array([[None for i in range(shape[0])] for j in range(shape[1])], dtype = Cell)
        
