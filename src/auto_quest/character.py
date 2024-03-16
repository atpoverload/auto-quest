import copy

ATTRIBUTES = ['health', 'strength', 'smarts', 'speed']


def new_character(species, name=None, level=0):
    """ Creates a fresh character. """
    character = Character(
        species=species,
        character={
            'name': name if name is not None else species['name'],
            'attributes': {attribute: 0 for attribute in ATTRIBUTES},
            'actions': [],
            'experience': 0,
            'level': 0,
        },
        status={
            'health': 0,
            'conditions': set(),
        },
    )
    if level > 0:
        for _ in range(level):
            character.gain_level()
        character.refresh()
    return character


class Character:
    def __init__(self, species, character, status):
        self._species = species
        self._character = character
        self._status = status

    def to_dict(self):
        return {
            'species': self._species,
            'character': self._character,
            'status': self._status,
        }

    def __str__(self):
        return str(self.to_dict())

    @property
    def name(self):
        return self._character['name']

    @property
    def species(self):
        return self._species['name']

    @property
    def level(self):
        return self._character['level']

    @property
    def health(self):
        return self._status['health']

    @property
    def max_health(self):
        return self._character['attributes']['health']

    @property
    def strength(self):
        return self._character['attributes']['strength']

    @property
    def smarts(self):
        return self._character['attributes']['smarts']

    @property
    def speed(self):
        return self._character['attributes']['speed']

    @property
    def actions(self):
        return copy.copy(self._character['actions'])

    @property
    def conditions(self):
        return copy.copy(self._status['conditions'])

    def damage(self, value):
        """ Decreases health so it won't be negative. """
        self._status['health'] = int(max(self._status['health'] - value, 0))

    def heal(self, value):
        """ Increases health so it doesn't exceed the character's max health. """
        self._status['health'] = int(min(
            self._status['health'] + value, self._character['attributes']['health']))

    def has_condition(self, condition):
        """ Checks if the condition is active. """
        return condition in self._status['conditions']

    def add_condition(self, condition):
        """ Adds the condition. """
        self._status['conditions'].add(condition)

    def remove_condition(self, condition):
        """ Removes the condition. """
        if condition in self._status['conditions']:
            self._status['conditions'].remove(condition)

    def refresh(self):
        """ Resets to max health and removes all conditions. """
        self._status['health'] = self._character['attributes']['health']
        self._status['conditions'] = set()

    def gain_level(self):
        """ Sets the character to their scaled stats and maybe learns a new move. """
        self._character['level'] += 1
        self._character['attributes'] = {
            'health':  int(self.level * self._species['attributes']['health']),
            'strength':  int(self.level * self._species['attributes']['strength']),
            'smarts':  int(self.level * self._species['attributes']['smarts']),
            'speed':  int(self.level * self._species['attributes']['speed']),
        }
        if self.level in self._species['actions']:
            self._character['actions'].append(
                self._species['actions'][self.level])
