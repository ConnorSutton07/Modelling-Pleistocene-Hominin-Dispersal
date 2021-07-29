from core.world import HexagonalWorld 
from settings import *
from PIL import Image

class Driver:
    def __init__(self):
        self.introduction()

    def run(self):
        world = self.create_initial_world()
        #world = World(WORLD_SHAPE)

    def create_initial_world(self):
        world = HexagonalWorld(WORLD_SHAPE)
        veg_im = Image.open("vegetation_map.png")
        elv_im = Image.open("elevation_map.png")
        rows, cols = WORLD_SHAPE
        for i in range(0, rows * 5, 5):
            for j in range(0, cols * 5, 5):
                P_ext = Driver.pixel_to_extinction_probability(veg_im.getpixel((i,j)))
                P_col = Driver.pixel_to_colinization_probability(elv_im.getpixel((i, j)))
                if P_ext is None:
                    world.create_cell((int(i/5), int(j/5)), False) # inactive cell
                else:
                    world.create_cell((int(i/5), int(j/5)), True, P_ext, P_col) # active cell with parameters based on vegetation, elevation

        # arbitrary selection of cells in the East African Rift Valley -- do this randomly later
        for member in INITIAL_POPULATION:
            world.populate(member)
        return world

    @staticmethod
    def pixel_to_extinction_probability(pix) -> float:
        if pix[0] == pix[1] == pix[2] == 255: # if not an all-white pixel
            return None
        P_ext = 1.0
        if (pix[0] == 7 and pix[1] == 120 and pix[2] == 11): # Temperate Forest
            P_ext = 0.12
        elif (pix[0] == 255 and pix[1] == 128 and pix[2] == 0): # Grassland
            P_ext = 0.12
        elif (pix[0] == 255 and pix[1] == 242 and pix[2] == 0): # Desert
            P_ext = 0.17
        elif (pix[0] == 0 and pix[1] == 79 and pix[2] == 0): # Tropical Forest
            P_ext = 0.12
        elif (pix[0] == 22 and pix[1] == 204 and pix[2] == 250): # Tundra
            P_ext = 1.0
        elif (pix[0] == 164 and pix[1] == 252 and pix[2] == 67): # Warm-temperate Forest
            P_ext = 0.18
        elif (pix[0] == 128 and pix[1] == 128 and pix[2] == 255): # Boreal Forest
            P_ext = 1.0
        elif (pix[0] == 132 and pix[1] == 97 and pix[2] == 37): # Savanna
            P_ext = 0.08
        elif (pix[0] == pix[1] == pix[2] == 200):
            P_ext = 1.0
        return P_ext

    @staticmethod
    def pixel_to_colinization_probability(pix) -> float:
        P_col = 0 
        if (pix[0] == 203 and pix[1] == 131 and pix[2] == 7):
            P_col = 0.2
        elif (pix[0] == 203 and pix[1] == 41 and pix[2] == 21):
            P_col = 0.10
        elif (pix[0] == 112 and pix[1] == 6 and pix[2] == 6):
            P_col = 0.05
        return P_col


    def introduction(self):
        title = "Modelling Pleistocene Hominin Dispersal"
        print()
        print("     +" + "-" * len(title) + "+")
        print("      " + title)
        print("     +" + "-" * len(title) + "+")
        print() 



