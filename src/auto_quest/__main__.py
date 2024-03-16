import json
import os

from argparse import ArgumentParser
from random import randint

from action import Action, run_turn
from character import new_character
from cli import CliDisplay
from world import World


CLI_DISPLAY = 'cli'


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
        default=os.path.join(os.path.dirname(__file__), 'test_world.json'),
        dest='world_file',
        help='the world file to load'
    )
    parser.add_argument(
        '--generate',
        default=None,
        help='generates a new world. if a world file is provided, the generated world will be saved there'
    )
    parser.add_argument(
        '-c',
        '--controller',
        default=None,
        choices=['random', 'file.py'],
        help='how the player is controlled, which is manual by default. a python file can be provided for decisions making'
    )
    parser.add_argument('--seed', default=None, help='randomization seed')
    return parser.parse_args()


def create_world(args):
    if args.generate is not None:
        return
        # with open(args.world_file, 'w') as f:
        #     json.dump(world, f)
    else:
        with open(args.world_file, 'r') as f:
            world_dict = json.load(f)
        return World(
            species=[{
                'name': species['name'],
                'attributes': species['attributes'],
                # TODO: json can't have dicts of ints -> obj
                'actions': {int(k): v for k, v in species['actions'].items()}
            } for species in world_dict['species']],
            actions={action.name: action for action in map(
                Action.from_dict, world_dict['actions'])}
        )


def create_display(args):
    if args.display == 'cli':
        if args.controller == 'random':
            return CliDisplay(controller=lambda choices: choose(choices))
        else:
            return CliDisplay()


def main():
    args = parse_args()

    try:
        world = create_world(args)
        display = create_display(args)

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
        enemy = new_character(starters[(choice + 1) % len(starters)], level=8)

        # battle
        logs = []
        while player.health > 0 and enemy.health > 0:
            display.display_log(f'Turn {len(logs) + 1}')
            choice = display.display_battle(player, enemy)

            player_action = world.actions[player.actions[choice]]
            enemy_action = world.actions[enemy.actions[choose(enemy.actions)]]
            log = run_turn(player, player_action, enemy, enemy_action)

            display.display_log(log)
            logs.append(log)
            print()
    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()
