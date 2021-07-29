"""
Contains constants that will be used to initialize and parameterize the
simulation model

"""

#-----------------------
#      World Setup
#-----------------------
WORLD_SHAPE = (205, 155)
INITIAL_POPULATION = [  # Scattered populations around East African Rift System
    (84, 91),
    (85, 92),
    (85, 96),
    (86, 90),
    (87, 94),
    (88, 93)
]

#-----------------------
#   Genetic Variation
#-----------------------
α = 3    # amplifies genetic drift
ß = 0.01 # standard deviation of genotype mutation