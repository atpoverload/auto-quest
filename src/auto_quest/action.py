from random import random


class Effect:
    def apply(self, user, target):
        return ''


def attack_scaling(user, target):
    user_power = user.level * user.strength
    target_power = target.strength + target.smarts + target.speed
    return user_power / target_power


class Attack(Effect):
    def __init__(self, power, accuracy):
        self.power = power
        self.accuracy = accuracy

    def to_dict(self):
        return {
            'type': 'attack',
            'power': self.power,
            'accuracy': self.accuracy,
        }

    def apply(self, user, target):
        """ Deal scaled damage to the target. """
        if target.has_condition('defend'):
            return f"{target.name} is defending"
        # TODO: find a way to provide a custom random engine
        if random() > self.accuracy / 100:
            return f"{user.name} missed"

        user_power = user.level * user.strength
        target_power = target.strength + target.smarts + target.speed
        scale = user_power / target_power

        target.damage(int(self.power * scale))

        return f"{user.name} attacks {target.name}"


class Heal(Effect):
    def __init__(self, power):
        self.power = power

    def to_dict(self):
        return {
            'type': 'heal',
            'power': self.power,
        }

    def apply(self, user, target):
        """ Recover fraction of max health for the user. """
        user.heal(int((self.power * user.max_health) // 100))

        return f"{user.name} heals"


class Condition(Effect):
    def __init__(self, condition):
        self.condition = condition

    def to_dict(self):
        return {
            'type': 'condition',
            'condition': self.condition,
        }

    def apply(self, user, target):
        """ Adds a condition to the target. """
        if target.has_condition('defend'):
            return f"{target.name} is defending"
        target.add_condition(self.condition)

        return f"{target.name} has {self.condition}"


class Defend(Effect):
    def to_dict(self):
        return {'type': 'defend'}

    def apply(self, user, target):
        """ Applies defend to the user. """
        user.add_condition('defend')

        return f"{user.name} defends"


def dict_to_effect(effect):
    """ Parses a dict into the associated effect. """
    if 'type' not in effect:
        return None
    if effect['type'] == 'attack':
        return Attack(effect['power'], effect['accuracy'])
    elif effect['type'] == 'heal':
        return Heal(effect['power'])
    elif effect['type'] == 'defend':
        return Defend()
    else:
        return None


class Action:
    def from_dict(action):
        return Action(action['name'], list(map(dict_to_effect, action['effects'])), action['priority'])

    def __init__(self, name, effects, priority=0):
        """ General helping wrapper for moves. """
        self.name = name
        self.effects = effects
        self.priority = priority

    def to_dict(self):
        return {
            'name': self.name,
            'effects': [effect.to_dict() for effect in self.effects],
            'priority': self.priority,
        }

    def act(self, user, target):
        logs = []
        logs.append(f"{user.name} uses {self.name}")
        logs.extend([effect.apply(user, target) for effect in self.effects])
        return logs


def run_turn(player, player_action, enemy, enemy_action):
    # get the turn order
    order = []

    if player_action.priority > enemy_action.priority:
        order = [player, enemy]
        action_order = [player_action, enemy_action]
    elif player_action.priority < enemy_action.priority:
        order = [enemy, player]
        action_order = [enemy_action, player_action]
    elif player.speed > enemy.speed:
        order = [player, enemy]
        action_order = [player_action, enemy_action]
    elif player.speed < enemy.speed:
        order = [enemy, player]
        action_order = [enemy_action, player_action]
    elif random() < 0.5:
        order = [player, enemy]
        action_order = [player_action, enemy_action]
    else:
        order = [enemy, player]
        action_order = [enemy_action, player_action]

    # don't let things happen if someone is dead
    logs = []
    if player.health > 0 and enemy.health > 0:
        logs.extend(action_order[0].act(order[0], order[1]))
    if player.health > 0 and enemy.health > 0:
        logs.extend(action_order[1].act(order[1], order[0]))

    player.remove_condition('defend')
    enemy.remove_condition('defend')

    return logs
