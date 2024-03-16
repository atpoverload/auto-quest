USER_CONTROLLER = 'user'


def display_character(character):
    name = character.name if character.name == character.species else f'{character.name} ({character.species})'
    conditions = ' '.join(list(character.conditions)) if len(
        character.conditions) > 0 else ''
    return [
        f"{name} LVL:{character.level}",
        f"HP:{character.health}/{character.max_health} {conditions}",
    ]


class CliDisplay:
    # TODO: custom output
    def __init__(self, controller=None):
        if controller is None:
            self.controller = USER_CONTROLLER
        else:
            self.controller = controller

        header = 4 * "\t"
        self.input_formatter = header + "{}"
        self.message_formatter = header + "  {}"

    def read_input(self):
        return input(self.input_formatter.format('> '))

    def display_choice(self, choices):
        print(self.message_formatter.format('  '.join(choices)))
        if self.controller != USER_CONTROLLER:
            return self.controller(choices)
        else:
            choice = input(self.input_formatter.format('> ')).strip()
            while True:
                try:
                    choice = int(choice)
                    if choice < len(choices):
                        return choice
                except:
                    if choice in choices:
                        return choices.index(choice)
                print(self.message_formatter.format(
                    f"{choice if len(choice) > 0 else None} is not valid!"))

    def display_battle(self, player, enemy):
        print(self.message_formatter.format(
            'ENEMY: ' + ' '.join(display_character(enemy))))
        print(self.message_formatter.format(
            'PLAYER: ' + ' '.join(display_character(player))))
        print(self.message_formatter.format(
            f'STR:{player.strength} SMT:{player.smarts} SPD:{player.speed}'))
        print(self.message_formatter.format('ACTIONS:'))
        return self.display_choice(player.actions)

    def display_log(self, log):
        if isinstance(log, str):
            print(self.message_formatter.format(log))
        else:
            print('\n'.join(map(self.message_formatter.format, log)))
