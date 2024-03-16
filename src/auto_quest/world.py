import random

from character import new_character

STARTER_COUNT = 3
SEED = "onion seed"


class World:
    def __init__(self, species, actions):
        self.species = species
        self.actions = actions
        random.seed(SEED)

    def create_starters(self):
        starters = []
        while len(starters) < STARTER_COUNT:
            species = random.randint(0, len(self.species) - 1)
            if species not in starters:
                starters.append(species)
        return [self.species[species] for species in starters]
