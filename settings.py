"""
Contains constants that will be used to initialize and parameterize the
simulation model

"""

from numpy.random import randint

#-----------------------------
#         World Setup
#-----------------------------
WORLD_SHAPE = (310, 250)
X_OFFSET = 60
INITIAL_POPULATION = [(randint(120, 131), randint(140, 170)) for _ in range(20)]  # Scattered populations around East African Rift System
σ = 3

#-----------------------------
#      Genetic Variation
#-----------------------------
α = 0.5    # amplifies genetic drift
ß = 0.1    # standard deviation of genotype mutation


#-----------------------------
#  Conditional Probabilities
#-----------------------------

# vegetation
TEMPERATE_FORST       = 0.06
GRASSLAND             = 0.05
DESERT                = 0.10
TROPICAL_FOREST       = 0.10
WARM_TEMPERATE_FOREST = 0.08
TUNDRA                = 0.50
BOREAL_FOREST         = 0.12
SAVANNA               = 0.05

# elevation
BASE = 0.30
LOW  = 0.25
MID  = 0.15
HIGH = 0.10

