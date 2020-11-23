#!/usr/bin/python3
''' combat.py:
    author: Arlo Gittings
    created: 2019.03.30
    description: A basic combat simulator
'''
import re
import datetime
import numpy

class Avatar:
    ''' Avatar:
        Class that holds all stats and available methods for players and
        NPCs.
    '''
    name = ''
    stats = {}
    level = 0
    backstory = ''
    char_class = ''
    race = ''
    sex = ''
    role = ''
    age = 0
    alignment = ''
    equipment = []

    def show(self):
        '''Show:
               Displays avatar data in a human readable format
        '''
        divider = '\n-------------------------------'
        id_block =  divider + \
                   '\n' + self.name +'\nAge: ' + self.age +\
                   divider + \
                   '\nLevel: ' + str(self.level) + \
                   '\nRace:  ' + self.race + \
                   '\nClass: ' + self.role + divider
        print(id_block)

        for i in self.stats:
            value = str(self.stats[i])
            spacer = (14 - len(i)) * ' '
            print('\t' + i + ':' + spacer + value)


def get_user():
    '''get_user:
       determins if we are making a new character or loading from a saved
       character and initiates the proper process. Then passes back the
       Avatar object for the game to proceed.
    '''
    new_game = clean_input("(N)ew, (L)oad, (Q)uit: ", 'NLQ').lower()
    if new_game == 'n':
        return create_character()
    elif new_game == 'l':
        print('Loading. . .')
        return True
    else:
        print('There are other worlds than these')
        return False

def clean_input(s, valid_data):
    '''clean_input:
       Requires:
           s: (The prompt string
           valid_data: descriptor of the proper format
       Returns:
           response: validated data
       On Error:
           provides proper data format and recursively prompts for new
           input.
        '''

    if valid_data == 'alpha':
        re_str = r'^[A-Za-z][A-Za-z\-_\ ][A-Za-z\-_\ ]+$'
        fail_str = "Enter only leters, spaces, dashes or underscores:"
    elif valid_data == 'MorF':
        re_str = '^[FfMm]$'
        fail_str = 'Enter M or F.'
    elif valid_data == 'NLQ':
        re_str = '^[LlNnQq]$'
        fail_str = 'Enter N, L or Q.'
    elif valid_data == 'int':
        re_str = r'^[0-9]+$'
        fail_str = 'Enter only numbers.'
    else:
        re_str = ''
    response = input(s).strip()
    if re.match(re_str, response):
        return response
    else:
        print(fail_str)
        return clean_input(s, valid_data)

def roll_die(s, c):
    '''roll_die:
        Requires:
            s: number of sides
            c: count of results to return
        Return:
            unnamed: list of integers within range 1-s
        On Error:
            Undefined.
    '''
    return numpy.random.randint(1, s, c)

def mod_stat(stat, l):
    '''mod_stat:
       Requires:
           stat: Name of the stat to modify
           l: list of viable values to assign to the stat
       Returns:
           value: The selected value
           l: the remaining available list of values after value is removed
       On Error:
           Print valid parameters for selection and recursively request
           player select from the list.
    '''
    value = int(clean_input(stat, 'int'))
    try:
        located = l.index(value)
    except ValueError:
        print('Select a value from the list\n', l)
        value, l = mod_stat(stat, l)
    else:
        del l[located]
    return value, l

def gen_stats():
    '''gen_stats:
           Create stats for new characters.
       Requires:
           Nothing
       Returns:
           base_stats: dictionary of randomly generated, user assigned
           values
       On Error:
           undefined
    '''
    available = []
    base_stats = {'Strength': 0,
                  'Dexterity': 0,
                  'Constitution': 0,
                  'Intelligence': 0,
                  'Wisdon': 0,
                  'Charisma': 0
                 }
    for i in range(len(base_stats)):
        temp = sorted(roll_die(6, 5))
        temp = sum(temp[1:-1])
        available.append(temp)
    available = sorted(available)

    print('Your skill scores:\n\t' + str(available) + '\nAssign your base stats:')
    for i in base_stats:
        s = '\t' + i + ': '
        base_stats[i], available = mod_stat(s, available)

    return base_stats

def set_race(avatar):
    '''set_race:
           Select from available races and modify stats, and sets traits
       Requires:
           avatar: class that describes the character
       Returns:
           response: the user selected race.
           avatar.stats: dictionary of modified stats
       On Error:
           print available races and prompt user to select from the list.
    '''
    races = ['Human',
             'Elf',
             'Dwarf',
             'Halfling'
            ]
    bonuses = {'Human': {'Strength': 1,
                         'Dexterity': 1,
                         'Constitution': 1,
                         'Intelligence': 1,
                         'Wisdon': 1,
                         'Charisma': 1
                        },
               'Elf': {'Dexterity': 2,},
               'Dwarf': {'Constitution': 2},
               'Halfling': {'Dexterity': 2}
              }
    print('Available races:')
    for race in races:
        print('\t' + race)

    response = clean_input('Select a race: ', 'alpha').capitalize()

    try:
        races.index(response)
    except ValueError:
        print('Select a race from the list')
        response, avatar.stats = set_race(avatar)

    for bonus in bonuses[response]:
        avatar.stats[bonus] = avatar.stats[bonus] + bonuses[response][bonus]

    return response, avatar.stats

def set_role():
    '''set_role
       Requires:
       Returns:
       On Error:
    '''
    roles = ['Barbarian', 'Fighter', 'Monk', 'Rogue',
             'Cleric', 'Druid', 'Paladin', 'Bard',
             'Mystic', 'Sorcerer', 'Wizard', 'Warlock',
             'Artificer', 'Ranger'
            ]
    print('Available classes:')
    i = 1
    print('\t', end='')

    for role in roles:
        spacer = (12 - len(role)) * ' '
        print(role, end=spacer)
        if not i%4:
            print('\n', end='\t')
        i += 1
    print()
    response = clean_input('Select a class: ', 'alpha')
    try:
        roles.index(response.capitalize())
    except ValueError:
        print('Select a class from the list')
        response = set_role()

    return response.capitalize()

def create_character():
    '''create_character:
       Requires:
       Returns:
       On Error:
    '''
    print('Creating new game. . .\n')
    character = Avatar()

    character.name = clean_input("Your name: ", 'alpha')
    character.level = 1
    character.sex = clean_input("(M)ale or (F)emale: ", 'MorF')
    character.stats = gen_stats()
    character.race, character.stats = set_race(character)
    character.age = clean_input('Age: ', 'int')
    character.role = set_role()
    return character

TICKER = datetime.datetime.now().strftime('%Y.%m.%d-%H%m%S')
print(TICKER)

PLAYER = get_user()
PLAYER.show()
