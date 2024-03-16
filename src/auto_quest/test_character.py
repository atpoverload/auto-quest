import unittest

from character import new_character

BASE_ATTRIBUTE = 10


class TestCharacter(unittest.TestCase):
    def test_character(self):
        character = new_character(species={
            'name': 'onion',
            'attributes': {
                'health': BASE_ATTRIBUTE,
                'strength': BASE_ATTRIBUTE,
                'smarts': BASE_ATTRIBUTE,
                'speed': BASE_ATTRIBUTE,
            },
            'moves': {},
            'experience': [100, 125],
        })

        character.gain_level()
        self.assertEqual(
            character.character['attributes'],
            {
                'health': BASE_ATTRIBUTE,
                'strength': BASE_ATTRIBUTE,
                'smarts': BASE_ATTRIBUTE,
                'speed': BASE_ATTRIBUTE,
            })
        self.assertEqual(character.status['health'], 0)

        character.refresh()
        self.assertEqual(character.status['health'], BASE_ATTRIBUTE)

        character.damage(1)
        self.assertEqual(character.status['health'], BASE_ATTRIBUTE - 1)

        character.heal(1)
        self.assertEqual(character.status['health'], BASE_ATTRIBUTE)

        character.damage(100)
        self.assertEqual(character.status['health'], 0)

        character.heal(100)
        self.assertEqual(character.status['health'], BASE_ATTRIBUTE)
