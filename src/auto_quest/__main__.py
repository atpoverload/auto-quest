import importlib.util
import json
import os
import sys

from argparse import ArgumentParser
from random import random, randint, seed

from action import Action, NOTHING, run_turn
from character import new_character
from cli import CliDisplay
from randomizer import randomize_species
from world import World


CLI_DISPLAY = 'cli'
DEFAULT_WORLD = os.path.join(os.path.dirname(__file__), 'test_world.json')


def choose(choices):
    return randint(0, len(choices) - 1)


def parse_args():
    parser = ArgumentParser(
        prog='Auto-Quest',
        description='A simple JRPG designed to be played by both humans and programs.',
    )
    parser.add_argument(
        '-d',
        '--display',
        type=str,
        default=CLI_DISPLAY,
        choices=[CLI_DISPLAY], help='where to display the game')
    parser.add_argument(
        '-w',
        '--world',
        type=str,
        default=DEFAULT_WORLD,
        dest='world_file',
        help='the world file to use')
    parser.add_argument(
        '--logic',
        default=None,
        choices=['random', 'file.py'],
        help='how the player is controlled, which is manual by default. a python file can be provided for decisions making')
    parser.add_argument(
        '--randomize',
        action='store_true',
        help='randomizes the world')
    parser.add_argument('--seed', default=None, help='randomization seed')
    return parser.parse_args()


def create_world(args):
    if args.generate:
        return
        # if args.world_file != DEFAULT_WORLD:
        #     with open(args.world_file, 'w') as f:
        #         json.dump(world_dict, f)
    else:
        with open(args.world_file, 'r') as f:
            world_dict = json.load(f)
        world = World(
            species=[{
                'name': species['name'],
                'attributes': species['attributes'],
                # TODO: json can't have dicts of ints -> obj
                'actions': {int(k): v for k, v in species['actions'].items()}
            } for species in world_dict['species']],
            actions={action.name: action for action in map(
                Action.from_dict, world_dict['actions'])}
        )

    if args.randomize is not None:
        world = World(
            [randomize_species(s, world.actions) for s in world.species],
            world.actions,
        )

    return world


def create_display(args):
    if args.logic is None:
        logic = None
    elif args.logic == 'random':
        logic = choose
    elif os.path.exists(args.logic) and os.path.splitext(args.logic)[-1] == 'py':
        spec = importlib.util.spec_from_file_location(
            'auto_quest.logic', args.logic)
        logic = importlib.util.module_from_spec(spec)
        sys.modules['auto_quest.logic'] = logic
        spec.loader.exec_module(logic)
        logic = logic.choose

    if args.display == 'cli':
        return CliDisplay(logic=logic)


def battle(player, enemy, actions, display):
    logs = []
    while player.health > 0 and enemy.health > 0:
        display.display_log(f'Turn {len(logs) + 1}')
        choice = display.display_battle(player, enemy)

        player_action = actions[player.actions[choice]]
        enemy_action = actions[enemy.actions[choose(enemy.actions)]]
        log = run_turn(player, player_action, enemy, enemy_action)

        display.display_log(log)
        logs.append(log)
        print()
    return logs


def main():
    args = parse_args()

    # setup the world and seed
    if args.seed is not None:
        seed(args.seed)
    world = create_world(args)
    display = create_display(args)

    try:
        display.display_log('What is your name?')
        name = display.read_input().strip()
        if not name:
            name = None

        # select starters
        starters = world.create_starters()
        display.display_log('Choose a starter')
        choice = display.display_choice(
            [starter['name'] for starter in starters])

        player = new_character(starters[choice], name=name, level=5)
        enemy = new_character(starters[(choice + 1) % len(starters)], level=3)
        battles = 0

        # lab battle
        battle(player, enemy, world.actions, display)

        if player.health <= 0:
            display.display_log('died')
            return
        display.display_log(f'gained {enemy.experience} experience')
        player.gain_experience(enemy.experience)
        display.display_character(player)
        while len(player.actions) > 4:
            display.display_log('Please drop an action')
            choice = display.display_choice(player.actions)
            player.forget_action(choice)
        player.refresh()
        battles += 1
        print()

        # post-lab
        while True:
            display.display_character(player)
            choice = display.display_choice(['scout', 'battle'])

            if choice == 0:
                difficulty = int(
                    player.level + randint(0, battles) / player.level)
                enemy = world.random_character(level=difficulty)

                counter = 1
                while True:
                    if player.health <= 0:
                        display.display_log('died')
                        return
                    display.display_battle_frame(player, enemy)
                    choice = display.display_choice(['scout', 'tame', 'flee'])
                    if choice == 1:
                        counter += 1
                        if random() > 1 / counter:
                            display.display_log(
                                f'successfully tamed {enemy.name}')
                            enemy.name = player.name
                            player = enemy
                            break
                        else:
                            display.display_log(f'failed to tame {enemy.name}')
                    elif choice == 2:
                        counter += 1
                        if random() > 1 / counter:
                            display.display_log(f'successfully fled')
                            break
                        else:
                            display.display_log(f'failed to flee')
                    enemy_action = world.actions[enemy.actions[choose(
                        enemy.actions)]]
                    log = run_turn(player, NOTHING, enemy, enemy_action)
                    display.display_log(log)
                    print()
            elif choice == 1:
                difficulty = int(
                    player.level + randint(0, battles) / player.level)
                enemy = world.random_character(level=difficulty)
                battle(player, enemy, world.actions, display)

                if player.health <= 0:
                    display.display_log('died')
                    return
                display.display_log(f'gained {enemy.experience} experience')
                player.gain_experience(enemy.experience)
                while len(player.actions) > 4:
                    display.display_log('Please drop an action')
                    choice = display.display_choice(player.actions)
                    player.forget_action(choice)
                    print()
                battles += 1
            print()

    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()
