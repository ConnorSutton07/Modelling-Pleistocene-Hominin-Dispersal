from core.world import HexagonalWorld 
from settings import *
from PIL import Image
import os

class Driver:
    def __init__(self):
        self.introduction()
        self.paths = {
            'figures': os.path.join(os.getcwd(), 'figures'),
            'maps':    os.path.join(os.getcwd(), 'maps'),
            'results': os.path.join(os.getcwd(), 'results')
        }

    def run(self):
        world = self.create_initial_world()
        for _ in range(800):
            world.step()
        self.generate_map(world.get_occupied_cells())

    def create_initial_world(self):
        world = HexagonalWorld(WORLD_SHAPE)
        veg_im = Image.open(os.path.join(self.paths['maps'], "vegetation_map.png"))
        elv_im = Image.open(os.path.join(self.paths['maps'], "elevation_map.png"))
        rows, cols = WORLD_SHAPE
        for i in range(0, rows * 5, 5):
            for j in range(0, cols * 5, 5):
                P_ext = self.pixel_to_extinction_probability(veg_im.getpixel((i,j)))
                P_col = self.pixel_to_colinization_probability(elv_im.getpixel((i, j)))
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
            P_ext = 0.03
        elif (pix[0] == 255 and pix[1] == 128 and pix[2] == 0): # Grassland
            P_ext = 0.03
        elif (pix[0] == 255 and pix[1] == 242 and pix[2] == 0): # Desert
            P_ext = 0.06
        elif (pix[0] == 0 and pix[1] == 79 and pix[2] == 0): # Tropical Forest
            P_ext = 0.03
        elif (pix[0] == 22 and pix[1] == 204 and pix[2] == 250): # Tundra
            P_ext = 0.50
        elif (pix[0] == 164 and pix[1] == 252 and pix[2] == 67): # Warm-temperate Forest
            P_ext = 0.06
        elif (pix[0] == 128 and pix[1] == 128 and pix[2] == 255): # Boreal Forest
            P_ext = 0.33
        elif (pix[0] == 132 and pix[1] == 97 and pix[2] == 37): # Savanna
            P_ext = 0.02
        elif (pix[0] == pix[1] == pix[2] == 200):
            P_ext = 1.0
        return P_ext

    @staticmethod
    def pixel_to_colinization_probability(pix) -> float:
        P_col = 0.2
        if (pix[0] == 203 and pix[1] == 131 and pix[2] == 7):
            P_col = 0.15
        elif (pix[0] == 203 and pix[1] == 41 and pix[2] == 21):
            P_col = 0.10
        elif (pix[0] == 112 and pix[1] == 6 and pix[2] == 6):
            P_col = 0.05
        return P_col

    def generate_map(self, cells: list) -> None:
        im = Image.open(os.path.join(self.paths['maps'], 'afroeurasia.png'))
        for i in range(len(cells)):
            pos = cells[i][0]
            color = tuple(cells[i][1].astype(int).tolist())
            for x in range(5):
                for y in range(5):
                    im.putpixel((int(pos[0] * 5 + (x - 2)), int(pos[1] * 5 + (y - 2))), color)
        im.save(os.path.join(self.paths['results'], 'result.png'))

        


    def introduction(self):
        title = "Modelling Pleistocene Hominin Dispersal"
        print()
        print("     +" + "-" * len(title) + "+")
        print("      " + title)
        print("     +" + "-" * len(title) + "+")
        print() 



