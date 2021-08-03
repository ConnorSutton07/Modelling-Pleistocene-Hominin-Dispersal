from core.world import * 
from settings import *
from PIL import Image
from icecream import ic
from tqdm import tqdm
import os
import numpy as np
import argparse

class Driver:
    def __init__(self):
        self.introduction()

        self.modes = {
            'density':   self.run_density,
            'variation': self.run_variation
        }
        self.paths = {
            'figures': os.path.join(os.getcwd(), 'figures'),
            'maps':    os.path.join(os.getcwd(), 'maps'),
            'results': os.path.join(os.getcwd(), 'results')
        }

        args = self.parse_args()
        self.mode = args.mode

    def run(self):
        steps = int(input('Steps: '))
        self.modes[self.mode](steps)

    def run_density(self, steps: int):
        worlds = [self.create_initial_world() for _ in range(3)]
        for _ in tqdm(range(steps)):
                for world in worlds:
                    world.step()
        self.generate_density_map([world.get_all_cells() for world in worlds])
        self.generate_variation_map2([world.get_all_cells() for world in worlds])

    def run_variation(self, steps: int):
        world = self.create_initial_world()
        for _ in tqdm(range(steps)):
            world.step()
        self.generate_density_map([world.get_all_cells()])
        self.generate_variation_map2([world.get_all_cells()])

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('mode', choices = self.modes.keys(), nargs = '?', const = 'variation', help = 'determines which mode to run')
        args = parser.parse_args()
        return args

    def create_initial_world(self):
        world = GeneticWorld(WORLD_SHAPE)
        veg_im = Image.open(os.path.join(self.paths['maps'], "vegetation_map.png"))
        elv_im = Image.open(os.path.join(self.paths['maps'], "elevation_map.png"))
        rows, cols = WORLD_SHAPE
        for i in range(0, rows * σ, σ):
            for j in range(0, cols * σ, σ):
                P_ext = self.pixel_to_extinction_probability(veg_im.getpixel((i + X_OFFSET, j)))
                P_col = self.pixel_to_colinization_probability(elv_im.getpixel((i + X_OFFSET, j)))
                if P_ext is None:
                    world.create_cell((int(i/σ), int(j/σ)), False) # inactive cell
                else:
                    world.create_cell((int(i/σ), int(j/σ)), True, P_ext, P_col) # active cell with parameters based on vegetation, elevation

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
            P_ext = TEMPERATE_FORST
        elif (pix[0] == 255 and pix[1] == 128 and pix[2] == 0): # Grassland
            P_ext = GRASSLAND
        elif (pix[0] == 255 and pix[1] == 242 and pix[2] == 0): # Desert
            P_ext = DESERT
        elif (pix[0] == 0 and pix[1] == 79 and pix[2] == 0): # Tropical Forest
            P_ext = TROPICAL_FOREST
        elif (pix[0] == 22 and pix[1] == 204 and pix[2] == 250): # Tundra
            P_ext = TUNDRA 
        elif (pix[0] == 164 and pix[1] == 252 and pix[2] == 67): # Warm-temperate Forest
            P_ext = WARM_TEMPERATE_FOREST
        elif (pix[0] == 128 and pix[1] == 128 and pix[2] == 255): # Boreal Forest
            P_ext = BOREAL_FOREST
        elif (pix[0] == 132 and pix[1] == 97 and pix[2] == 37): # Savanna
            P_ext = SAVANNA
        return P_ext

    @staticmethod
    def pixel_to_colinization_probability(pix) -> float:
        P_col = BASE
        if (pix[0] == 203 and pix[1] == 131 and pix[2] == 7):
            P_col = LOW
        elif (pix[0] == 203 and pix[1] == 41 and pix[2] == 21):
            P_col = MID
        elif (pix[0] == 112 and pix[1] == 6 and pix[2] == 6):
            P_col = HIGH
        return P_col

    def generate_variation_map(self, cells: list) -> None:
        im = Image.open(os.path.join(self.paths['maps'], 'afroeurasia.png'))
        for i in range(len(cells)):
            pos = cells[i][0]
            color = tuple(cells[i][1].astype(int).tolist())
            for x in range(σ):
                for y in range(σ):
                    im.putpixel((int(pos[0] * σ + x + 2) + X_OFFSET, int(pos[1] * σ + y - 2)), color)
        im.save(os.path.join(self.paths['results'], 'variation_map.png'))

    def generate_variation_map2(self, worlds: list) -> None:
        im = Image.open(os.path.join(self.paths['maps'], 'afroeurasia.png'))
        for i in range(WORLD_SHAPE[0]):
            for j in range(WORLD_SHAPE[1]):
                avg_c = np.zeros((3,))
                num_occupied = 0
                for cells in worlds:
                    if cells[i][j].is_occupied(): 
                        avg_c += cells[i][j].get_genotype()
                        num_occupied += 1
                if num_occupied > 0:
                    avg_c = tuple((avg_c / num_occupied).astype(int).tolist())
                    for x in range(σ):
                        for y in range(σ):
                            im.putpixel((int(i * σ + x + 1) + X_OFFSET, int(j * σ + y - 8)), avg_c)
            # color = tuple(cells[i][1].astype(int).tolist())
            # for x in range(σ):
            #     for y in range(σ):
            #         im.putpixel((int(pos[0] * σ + x + 2) + X_OFFSET, int(pos[1] * σ + y - 2)), color)
        im.save(os.path.join(self.paths['results'], 'variation_map.png'))

    def generate_density_map(self, worlds: list) -> None:
        im = Image.open(os.path.join(self.paths['maps'], 'afroeurasia.png'))
        for i in range(WORLD_SHAPE[0]):
            for j in range(WORLD_SHAPE[1]):
                num_occupied = 0
                for cells in worlds:
                    if cells[i][j].is_occupied(): num_occupied += 1
                if num_occupied > 0:
                    c = int(255 - ((num_occupied / len(worlds)) * 255))
                    for x in range(σ):
                        for y in range(σ):
                            im.putpixel((int(i * σ + x + 1) + X_OFFSET, int(j * σ + y - 8)), (c, c, c))
        im.save(os.path.join(self.paths['results'], 'density_map.png'))


 
    def introduction(self):
        title = "Modelling Pleistocene Hominin Dispersal"
        print()
        print("     +" + "-" * len(title) + "+")
        print("      " + title)
        print("     +" + "-" * len(title) + "+")
        print()