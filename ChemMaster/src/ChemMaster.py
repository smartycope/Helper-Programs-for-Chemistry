# Thank you Brigham, for being an idiot
# This program is dedicated to Tommy, the weirdo who found this code and showed it to his teacher Brigham keys
import re
import functools
import json
import math
import os
import sys
from collections import Counter
from operator import itemgetter, attrgetter, iadd
# external modules
import sympy
from cursesmenu import *
from cursesmenu.items import *
from chempy import Substance
from chempy import Equilibrium
from sympy import symbols
from chempy.electrolytes import ionic_strength
# my own modules
from equation import Equation
from compound import Compound
from element  import Element

#define DEBUG True
#define ('q', 'quit', 'done', 'finish', 'finished', 'exit') ('q', 'quit', 'done', 'finish', 'finished', 'exit')
#define ('r', 'b', 'back', 'restart', 'beginning', 'begin', 'r', 'b', 'back', 'restart', 'beginning', 'begin', 'begining', 'start', 'home', 'h') ('r', 'b', 'back', 'restart', 'beginning', 'begin', 'r', 'b', 'back', 'restart', 'beginning', 'begin', 'begining', 'start', 'home', 'h')
#define ('opt', 'option', 'options') ('opt', 'option', 'options')
#define # #

DEBUG = False
_cmd = bool()
if len(sys.argv) <= 1:
    _cmd = False
else:
    _cmd = True
    # return
if len(sys.argv) > 3:
    print('Too many command line arguments. Expected 2 and got', len(sys.argv), '\b.')
    exit(0)


ELEMENTS=[
    'H' ,                                                                                                                                                                                     'He',
    'Li', 'Be',                                                                                                                                                 'B' , 'C' , 'N' , 'O' , 'F' , 'Ne',
    'Na', 'Mg',                                                                                                                                                 'Al', 'Si', 'P' , 'S' , 'Cl', 'Ar',
    'K' , 'Ca', 'Sc',                                                                                     'Ti', 'V' , 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
    'Rb', 'Sr', 'Y' ,                                                                                     'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I' , 'Xe',
    'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W' , 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
    'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U' , 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og',
    'Uue'
]
_basicCharges = [
    1,                                                                                               0,
    1, 2,                                                                         3, -4, -3, -2, -1, 0,
    1, 2,                                                                         3, -4, -3, -2, -1, 0,
    1, 2, 9,                                           9, 9, 9, 9, 9, 9, 9, 9, 9, 3, -4, -3, -2, -1, 0,
    1, 2, 9,                                           9, 9, 9, 9, 9, 9, 9, 9, 9, 3,  9, -3, -2, -1, 0,
    1, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3,  9, -3, -2, -1, 0,
    1, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3,  9, -3, -2, -1, 0,
    9
]


IONIC_CHARGES = dict(zip(ELEMENTS, _basicCharges))
IONIC_CHARGES['Zn'] = 2
IONIC_CHARGES['Ag'] = 1
IONIC_CHARGES['Sn'] = 9
IONIC_CHARGES['Pb'] = 9


with open(r'/home/Robert/hello/chemistry programs/ChemMaster/PeriodicTableJSON.json', 'r') as f:
    elementalInfo = json.load(f)


with open(r'/home/Robert/hello/chemistry programs/ChemMaster/ChemistryOptions.json') as f:
    options = json.load(f)

elementalInfo = elementalInfo["elements"]
elementFullNames = list()

class NotAnElementError(Exception):
    pass


for el in ELEMENTS:
    elementFullNames.append(elementalInfo[el]['name'])


def clear():
    if options['Clear the Terminal'] and not _cmd:
        os.system('cls' if os.name == 'nt' else 'clear')
    # print(chr(27) + "[2J")
    # pass


def handleCommandLineParams():
    # if len(sys.argv) <= 1:
    #     _cmd = False
    #     return
    # if len(sys.argv) > 3:
    #     print('Too many command line arguments. Expected 2 and got', len(sys.argv), '\b.')
    #     exit(0)

    # _cmd = True
    # print("_cmd is true")
    if len(sys.argv) in (2, 3):
        sys.argv.pop(0)
        # args = tuple(sys.argv)

        getInfo(parseInput(sys.argv.pop(0)), True,  sys.argv.pop(0))
        exit(0)


def getInfo(object, _cmd, cmdOption = ''):
    # print(f"_cmd is {_cmd}")
    # assert(len(cmdOption) == _cmd)
    if not _cmd:
        print('')
        clear()
    if type(object) == Element:
        clear()
        while True:
            if not _cmd:
                choice = input(f'\nWhat would you like to know about {elementalInfo[object.symbol]["name"]}?\n'
                                '1\tAtomic Number\n'
                                '2\tAtomic Mass\n'
                                '3\tPeriod\n'
                                '4\tPhase of Matter at Room Temperature\n'
                                '5\tBoiling Point\n'
                                '6\tMelting Point\n'
                                '7\tCategory\n'
                                '8\tColor\n'
                                '9\tAppearance\n'
                                '10\tDensity\n'
                                '11\tWho it was Discovered by\n'
                                '12\tWho it was Named by\n'
                                '13\tMolar Heat\n'
                                '14\tSummary\n'
                                '15\tPosition on the Periodic Table\n'
                                '-16\tElectron Shells\n'
                                '17\tElectron Configuration\n'
                                '18\tElectron Affinity\n'
                                '19\tElectronegativity Pauling\n'
                                '20\tIonization Energies\n'
                                '21\tCharge\n'
                                '22\tEverything\n'
                                '23\tGo Back\n\n'
                                )
            else:
                choice = cmdOption


            if   choice.lower() in ('1', 'number', 'n', 'one', 'num', 'atomic num', 'atomic number'):
                clear()
                print(elementalInfo[object.symbol]['number'])
                return
            elif choice.lower() in ('2', 'two', 'mass', 'atomic mass', 'weight', 'atomic weight'):
                clear()
                print(elementalInfo[object.symbol]['atomic_mass'])
                return
            elif choice.lower() in ('3', 'three', 'period', 'row'):
                clear()
                print(elementalInfo[object.symbol]['period'])
                return
            elif choice.lower() in ('4', 'four', 'phase'):
                clear()
                print(elementalInfo[object.symbol]['phase'])
                return
            elif choice.lower() in ('5', 'five', 'boil', 'boiling', 'boil point', 'boiling point'):
                clear()
                print(elementalInfo[object.symbol]['boil'])
                return
            elif choice.lower() in ('6', 'six', 'melt', 'melting', 'melt point', 'melting point'):
                clear()
                print(elementalInfo[object.symbol]['melt'])
                return
            elif choice.lower() in ('7', 'seven', 'category'):
                clear()
                print(elementalInfo[object.symbol]['category'])
                return
            elif choice.lower() in ('8', 'eight', 'color', 'shade'):
                clear()
                print(elementalInfo[object.symbol]['color'])
                return
            elif choice.lower() in ('9', 'nine', 'apperance', 'look'):
                clear()
                print(elementalInfo[object.symbol]['appearance'])
                return
            elif choice.lower() in ('10', 'ten', 'density'):
                clear()
                print(elementalInfo[object.symbol]['density'])
                return
            elif choice.lower() in ('11', 'eleven', 'discovered by', 'discovered', 'discover', 'discovery'):
                clear()
                print(elementalInfo[object.symbol]['discovered_by'])
                return
            elif choice.lower() in ('12', 'twelve', 'named by', 'named', 'name', 'namer', 'named', 'naming'):
                clear()
                print(elementalInfo[object.symbol]['named_by'])
                return
            elif choice.lower() in ('13', 'thirteen', 'molar heat', 'heat', 'molar'):
                clear()
                print(elementalInfo[object.symbol]['molar_heat'])
                return
            elif choice.lower() in ('14', 'fourteen', 'summary', 'conclusion', 'summation'):
                clear()
                print(elementalInfo[object.symbol]['summary'])
                return
            elif choice.lower() in ('15', 'fifteen', 'position', 'location', 'pos', 'loc', 'where at', 'at', 'where'):
                clear()
                print(elementalInfo[object.symbol]['xpos'], ", ", elementalInfo[object.symbol]['ypos'], sep='')
                return
            elif choice.lower() in ('16', 'sixteen', 'electron shells', 'shells', 'shell', 'es', 'els', 'el sh', 'elsh', 'el s'):
                clear()
                print("Sorry, I don't understand enough about chemistry to tell you.")
                return
            elif choice.lower() in ('17', 'seventeen', 'electron configuration', 'electron configureation', 'electron config', 'configuration', 'configureation', 'config', 'ec', 'elc', 'conf', 'electron conf', 'elconf', 'econf', 'el conf'):
                clear()
                print(elementalInfo[object.symbol]["electron_configuration"])
                return
            elif choice.lower() in ('18', 'eighteen', 'electron affinity', 'affinity', 'electron a', 'ea', 'ela', 'elaf'):
                clear()
                print(elementalInfo[object.symbol]["electron_affinity"])
                return
            elif choice.lower() in ('19', 'nineteen', 'electronegativity pauling', 'electronegativity', 'pauling', 'eln', 'negativity', 'neg', 'el n', 'en', 'elneg', 'el neg', 'eneg', 'e neg'):
                clear()
                print(elementalInfo[object.symbol]["electronegativity_pauling"])
                return
            elif choice.lower() in ('20', 'twenty', 'ionization energies', 'ionization', 'ionization energy', 'ion energy', 'energy', 'energies'):
                clear()
                print(elementalInfo[object.symbol]['ionization_energies'])
                return
            elif choice.lower() in ('21', 'twenty one', 'twenty-one', 'twentyone', 'charge', 'ionic', 'ionic charge', 'bond energy', 'bonding energy', 'bond charge', 'bonding charge'):
                clear()
                print(IONIC_CHARGES[object.symbol])
                return
            elif choice.lower() in ('21', 'twenty one', 'twenty-one', 'twentyone', 'all', 'everything', 'every'):
                clear()
                print(elementalInfo[object.symbol]['summary'])
                return
            elif choice.lower() in ('22', 'twenty two', 'twenty-two', 'twentytwo') + ('r', 'b', 'back', 'restart', 'beginning', 'begin', 'r', 'b', 'back', 'restart', 'beginning', 'begin', 'begining', 'start', 'home', 'h'):
                clear()
                return
            elif choice.lower() in ('q', 'quit', 'done', 'finish', 'finished', 'exit'):
                quit(0)
            else:
                print("Sorry, I don't know what to do with that.")
                if _cmd:
                    return

            '''
                else:
                    ans = [
                        'number',
                        'atomic_mass',
                        'period',
                        'phase',
                        'boil',
                        'melt',
                        'category',
                        'color',
                        'appearance',
                        'density',
                        'discovered_by',
                        'named_by',
                        'molar_heat',
                        'summary',
                        'electron_configuration',
                        'electron_affinity',
                        'electronegativity_pauling',
                    ]

                    clear()
                    # print(dict(zip(range(1, 22), ans)))
                    # print(dict(zip(tuple(range(1, 14)) + (17, 18, 19), ans)).get(choice))
                    print(elementalInfo[object.symbol][dict(zip(tuple(range(0, 13)) + (16, 17, 18), ans)).get(choice)])
            '''

            # except(ValueError):
                # if option.upper() == 'R':
                #     clear()
                #     return
                # elif option.upper() == 'Q':
                #     quit(0)
                # else:
                #     print("Sorry, I don't know what to do with that.")

                # option = input(f"Press I for more info on {elementalInfo[object.symbol]['name']}, R to go back, or Q to quit.\n")
                # if   option.upper() == 'I':
                #     continue
                # elif option.upper() == 'R':
                #     clear()
                #     return
                # elif option.upper() == 'Q':
                #     quit(0)
                # else:
                #     print("Sorry, I don't know what to do with that.")

    elif type(object) == Compound:
        clear()
        while True:
            if not _cmd:
                choice = input(f'\nWhat would you like to know about {object.draw()}?\n'
                                '1\tAtomic Weight\n'
                                '2\tType of Bond\n'
                                '3\tIt\'s name\n'
                                '4\tCharge\n'
                                '5\tEverything\n'
                                '6\tGo Back\n\n'
                                )
            else:
                cmdOption = choice.lower()

            if   choice in ('1', 'one', 'mass', 'weight', 'atomic mass', 'atomic weight'):
                clear()
                print(object.getWeight())
                return
            elif choice in ('2', 'two', 'bond', 'type of bond', 'bond type'):
                clear()
                print("Ionic" if object.isIonicBound() else "Covelent")
                return
            elif choice in ('3', 'three', 'name', 'get name', 'its name', 'it\'s name'):
                clear()
                print(object.getName())
                return
            elif choice in ('4', 'four', 'charge'):
                clear()
                print(object.getCharge())
                return
            elif choice in ('5', 'five', 'all', 'everything', 'every', 'summary', 'conclusion', 'summation'):
                clear()
                print(object.getName(), "is a", "\bn ionicly" if object.isIonicBound() else "covelently", "bound compound with a charge of", object.getCharge(), '\b.')
                return
            elif choice in ('6', 'six') + ('r', 'b', 'back', 'restart', 'beginning', 'begin', 'r', 'b', 'back', 'restart', 'beginning', 'begin', 'begining', 'start', 'home', 'h'):
                clear()
                return
            elif choice.lower() in ('q', 'quit', 'done', 'finish', 'finished', 'exit'):
                quit(0)
            else:
                print('Sorry, I don\'t know what to do with that.')
                if _cmd:
                    return

    elif type(object) == Equation:
        clear()
        while True:
            if not _cmd:
                choice = input(f'What would you like to know about {object.draw()}?\n'
                                '1\tIs it Balanced\n'
                                '2\tWhat kind of Reaction it is\n'
                                '3\tEverything\n'
                                '4\tGo Back\n\n'
                                )
            else:
                cmdOption = choice.lower()

            if   choice in ('1', 'one', 'is balanced', 'is it balanced', 'balance', 'balanced', 'even', 'is even', 'is it even'):
                clear()
                print("The Formula is Balanced." if object.isBalanced() else "The Formula is Unbalanced.")
                return
            elif choice in ('2', 'two', 'what kind of reaction it is', 'reaction', 'kind of reaction', 'kind reaction', 'reaction kind', 'reaction type', 'type reaction', 'type of reaction'):
                clear()
                print(object.getType())
                return
            elif choice in ('3', 'three', 'all', 'everything', 'every', 'summary', 'conclusion', 'summation'):
                clear()
                object.draw()
                print("is a", "balanced" if object.isBalanced() else "\bn unbalanced", object.getType(), "equation.\n")
                return
            elif choice in ('4', 'four') + ('r', 'b', 'back', 'restart', 'beginning', 'begin', 'r', 'b', 'back', 'restart', 'beginning', 'begin', 'begining', 'start', 'home', 'h'):
                clear()
                return
            elif choice.lower() in QUIT_ALIASES:
                quit(0)
            else:
                print('Sorry, I don\'t know what to do with that.')
                if _cmd:
                    return

def set(object, value):
    object = value
    return object

def getInfoNew(object):
    if type(object) == Element:
        ans = str()
        # menu = SelectionMenu('Atomic Number', 'Atomic Mass', 'Period', 'Phase of Matter at Room Temperature', 'Boiling Point', 'Melting Point', 'Category', 'Color', 'Appearance', 'Density', 'Who it was Discovered by', 'Who it was Named by', 'Molar Heat', 'Summary', 'Position on the Periodic Table', '-Electron Shells', 'Electron Configuration', 'Electron Affinity', 'Electronegativity Pauling', 'Ionization Energies', 'Everything', 'Go Back')
        menu = CursesMenu(f"What would you like to know about {elementalInfo[object.symbol]['name']}?", ans)
        pretties = ('Atomic Number', 'Atomic Mass', 'Period', 'Phase of Matter at Room Temperature', 'Boiling Point', 'Melting Point', 'Category', 'Color', 'Appearance', 'Density', 'Who it was Discovered by', 'Who it was Named by', 'Molar Heat', 'Summary', '-Electron Shells', 'Electron Configuration', 'Electron Affinity', 'Electronegativity Pauling', 'Ionization Energies')
        jsons = ('number', 'atomic_mass', 'period', 'phase', 'boil', 'melt', 'category', 'color', 'appearance', 'density', 'discovered_by', 'named_by', 'molar_heat', 'summary', 'electron_configuration', 'electron_affinity', 'electronegativity_pauling', 'ionization_energies')
        # menu.subtitle = "Hi there."
        # for pretty, json in zip(pretties, jsons):
            # menu.append_item(FunctionItem(pretty, lambda string: (menu.subtitle := string), [str(elementalInfo[object.symbol][json])]))
            # menu.
        # menu.append_item(FunctionItem('Position on the Periodic Table', lambda string: menu.subtitle := string, [str(elementalInfo[object.symbol]['xpos']) + '\b, ' + str(elementalInfo[object.symbol]['ypos'])]))
        menu.append_item(FunctionItem('Quit', exit, [0]))

    elif type(object) == Compound:
        menu = CursesMenu(f"What would you like to know about {object.draw()}?\n")
        menu.append_item(FunctionItem('Atomic Weight', object.getWeight()))
        menu.append_item(FunctionItem('Type of Bond', print, "Ionic" if object.isIonicBound() else "Covelent"))
        menu.append_item(FunctionItem('It\'s name', object.getName()))
        menu.append_item(FunctionItem('Charge', object.getCharge()))
        menu.append_item(FunctionItem('Everything', print, [object.getName(), "is a", "\bn ionicly" if object.isIonicBound() else "covelently", "bound compound with a charge of", object.getCharge(), '\b.']))
        menu.append_item(FunctionItem('Quit', exit, [0]))

    elif type(object) == Equation:
        menu = CursesMenu(f'What would you like to know about {object.draw()}?\n')
        menu.append_item(FunctionItem('Is it Balanced', print, "The Formula is Balanced." if object.isBalanced() else "The Formula is Unbalanced."))
        menu.append_item(FunctionItem('What kind of Reaction it is', object.getType()))
        menu.append_item(FunctionItem('Everything', print, f'{object.draw()} is a', "balanced" if object.isBalanced() else "\bn unbalanced", object.getType(), "equation.\n"))
        menu.append_item(FunctionItem('Quit', exit, [0]))

    menu.show()


def optionsMenu():
    # with open(r'ChemistryOptions.json', 'w') as f:
    print('   Option                                      Currently Set To\n'
            '================================================================\n'
            '1: Clear the terminal after each option \t' + str(options['Clear the Terminal']) + '\n')

    optionToChange = input('What option would you like to change?\n')

    if optionToChange.lower() in ('r', 'b', 'back', 'restart', 'beginning', 'begin', 'r', 'b', 'back', 'restart', 'beginning', 'begin', 'begining', 'start', 'home', 'h'):
        pass
    elif optionToChange.lower() in ('q', 'quit', 'done', 'finish', 'finished', 'exit'):
        quit(0)
    else:
        changeTo = input('What should I change it to?\n')

        if optionToChange.lower() in ('1', 'clear', 'c'):
            options['Clear the Terminal'] = bool(changeTo)
        print(options)
            # json.dump('Clear the Terminal', bool(changeTo))
        # json.JSONEncoder.encode(options)
    # print(type(options))
        # f.dumps(options)
    # clear()


def _setValue(option):
    options[option] = input(option + " is currently set to " + str(options[option]) + '. What would you like to change it to?\n')
def optionsMenuNew():
    menu = CursesMenu("Options", "Subtitle")
    for option in options:
        menu.append_item(FunctionItem(option, _setValue, [option]))

    menu.show()


def parseInput(choice):
    if DEBUG and type(choice) != str:
        print(f"parseInput recived a {type(choice)} instead of a string. Choice is {choice}")
        print(_cmd)

    # is an equation
    if re.search(r"[-][>]", choice):
        print(choice + ' was determined to be an equation') if DEBUG else ''
        return Equation(choice)

    # is an element
    elif re.search(r'([A-Z][a-z]$)|([A-Z]$)', choice) and (choice.title() in ELEMENTS) and not re.search(r'[+]', choice) and (choice.lower() not in ('opt', 'option', 'options')):
        print(choice + ' was determined to be an element.') if DEBUG else ''
        if choice.islower():
            choice = choice.title()
        return Element(choice)

    # is a compound --- and (choice.lower() != ('opt' or 'option' or 'options')
    elif re.search(r"([A-Z][a-z]\d\d$)|([A-Z][a-z]\d$)|([A-Z][a-z]$)|([A-Z]\d\d$)|([A-Z]\d$)|([A-Z][A-Z]$)", choice) and (choice.lower() not in ('opt', 'option', 'options')):
        print(choice + ' was determined to be a compound.') if DEBUG else ''
        return Compound(choice)

    elif choice.title() in elementFullNames:
        print(choice + ' was determined to be in the elements dictionary.') if DEBUG else ''
        return Element(dict(zip(elementFullNames, ELEMENTS))[choice.title()])

    elif choice.upper() in ('q', 'quit', 'done', 'finish', 'finished', 'exit'):
        print(choice + ' was determined to be a quit signal.') if DEBUG else ''
        exit(0)

    elif choice.lower() in ('opt', 'option', 'options'):
        print(choice + ' was determined to be an options signal.') if DEBUG else ''
        return -1

    else:
        print(choice + ' wasn\'t determined to be anything recognizable.') if DEBUG else ''
        print("Sorry, I don't know what to do with that.")


def handleInput(choice):
    if type(choice) == Equation:
        if choice.isBalanced():
            clear()
            getInfoNew(choice)

        else: # choice is unbalanced
            clear()
            subChoice = input('It looks like you\'ve entered an unbalanced chemical formula. Would you like me to balance it for you? (Y/N)\n')

            while True:
                if subChoice.upper() == 'Y':
                    clear()
                    choice.draw()
                    # just to add and center the arrow
                    print('')
                    # fix this. It was cool.
                    # [print(' ', end='') for _ in range(int((len(choice) / 2)) - 1)]
                    print(r'\|/', end='')

                    choice.balanceCoeficients()
                    choice.draw()
                    print('')
                    return True
                elif subChoice.upper() == 'N':
                    while True:
                        subSubChoice = input('Alright then. Press I for info about the formula, R to go back to the beginning, or Q to quit.\n')

                        if   subSubChoice.upper() == 'I':
                            getInfoNew(choice)
                            return True
                        elif subSubChoice.upper() == 'R':
                            clear()
                            return True
                        elif subSubChoice.upper() == 'Q':
                            quit(0)
                        else:
                            print("Sorry, I don't know what to do with that.")
                    break
                elif subChoice.upper() == 'I':
                    getInfoNew(choice)
                    return True
                elif subChoice.upper() == 'R':
                    clear()
                    return True
                elif subChoice.upper() == 'Q':
                    quit(0)
                else:
                    print("Sorry, I don't know what to do with that.")

    if type(choice) == Element:
        clear()
        getInfoNew(choice)
        return True

    if type(choice) == Compound:
        clear()
        getInfoNew(choice)
        return True

    if choice == -1:
        optionsMenu() if options["Old-style Menus"] else optionsMenuNew()
        return True

    # return restart


def main():
    handleCommandLineParams()
    restart = True
    clear()
    print('Welcome to Copeland\'s Stoichometric Helper!')

    while restart:
        restart = False

        choice = input('Enter a compound, an element, or a chemical equation, or press Q to quit, or opt for options:\n')

        try:
            restart = handleInput(parseInput(choice))
        except(NotAnElementError):
            print("Sorry, that's not an element. Please enter a valid element.")
            restart = True


main()

'''
    useful for DEBUGging
    DEBUGFormula = "C8H18 + O2 -> CO2 + H2O"
    DEBUGFormula = "C8H8 + C2H2 -> C5H5"
    print(DEBUGFormula)
    formula = Equation(DEBUGFormula)

    import mpu.io
    data = mpu.io.read('example.json')
    mpu.io.write('example.json', data)
'''