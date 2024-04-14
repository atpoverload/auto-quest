from random import random, randint


def randomize_attributes(attributes_types, attribute_total):
    attributes = {attribute: random() for attribute in attributes_types}
    total_attributes = sum(attributes.values())
    return {attribute: int(attribute_total * attributes[attribute] / total_attributes) for attribute in attributes}


def randomize_actions(levels, actions_pool):
    actions = {}
    counter = 0
    while len(actions) < len(levels):
        action = actions_pool[randint(0, len(actions_pool) - 1)]
        if action not in actions.values():
            actions[levels[counter]] = action
            counter += 1
    return actions


def randomize_species(species, actions):
    return {
        'name': species['name'],
        'attributes': randomize_attributes(species['attributes'].keys(), sum(species['attributes'].values())),
        'actions': randomize_actions(
            list(species['actions'].keys()),
            list(actions.keys())
        ),
    }
