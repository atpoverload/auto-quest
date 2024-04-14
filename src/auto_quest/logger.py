USER_CONTROL = 'user'


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
    def __init__(self, logic=None):
        if logic is None or logic == USER_CONTROL:
            self.logic = USER_CONTROL
        else:
            self.logic = logic

        header = 4 * '\t'
        self.input_fmt = header + '{}'
        self.message_fmt = header + '  {}'

    def read_input(self):
        return input(self.input_fmt.format('> ')).strip()

    def display_choice(self, choices):
        print(self.message_fmt.format('  '.join(choices)))
        if self.logic != USER_CONTROL:
            return self.logic(choices)
        else:
            while True:
                choice = self.read_input()
                try:
                    choice = int(choice)
                    if choice < len(choices):
                        return choice
                    else:
                        print(self.message_fmt.format(
                            f"{choice} is not valid!"))
                        continue
                except:
                    if choice in choices:
                        return choices.index(choice)
                print(self.message_fmt.format(
                    f"{choice if len(choice) > 0 else None} is not valid!"))

    def display_character(self, character):
        print(self.message_fmt.format(' '.join(display_character(character))))
        print(self.message_fmt.format(
            f'STR:{character.strength} SMT:{character.smarts} SPD:{character.speed}'))
        print(self.message_fmt.format(
            f"ACTIONS: {' '.join(character.actions)}"))

    def display_battle_frame(self, player, enemy):
        print(self.message_fmt.format(
            'ENEMY: ' + ' '.join(display_character(enemy))))
        print(self.message_fmt.format(
            'PLAYER: ' + ' '.join(display_character(player))))

    def display_battle(self, player, enemy):
        self.display_battle_frame(player, enemy)
        print(self.message_fmt.format(
            f'STR:{player.strength} SMT:{player.smarts} SPD:{player.speed}'))
        print(self.message_fmt.format('ACTIONS:'))
        return self.display_choice(player.actions)

    def display_log(self, log):
        if isinstance(log, str):
            print(self.message_fmt.format(log))
        else:
            print('\n'.join(map(self.message_fmt.format, log)))
