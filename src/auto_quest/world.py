from random import randint

from character import new_character

STARTER_COUNT = 3


class World:
    def __init__(self, species, actions):
        self.species = species
        self.actions = actions

    def create_starters(self):
        starters = []
        while len(starters) < STARTER_COUNT:
            # TODO: find a way to provide a custom random engine
            species = randint(0, len(self.species) - 1)
            if species not in starters:
                starters.append(species)
        return [self.species[species] for species in starters]

    def random_character(self, level):
        return new_character(self.species[randint(0, len(self.species) - 1)], level=level)
