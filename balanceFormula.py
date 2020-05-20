import re
import sympy
import functools
import json
import math
from collections import Counter
from operator import itemgetter, attrgetter

ELEMENTS=[
'H' ,                                                                                                                                                                                     'He',
'Li', 'Be',                                                                                                                                                 'B' , 'C' , 'N' , 'O' , 'F' , 'Ne',
'Na', 'Mg',                                                                                                                                                 'Al', 'Si', 'P' , 'S' , 'Cl', 'Ar',
'K' , 'Ca', 'Sc',                                                                                     'Ti', 'V' , 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
'Rb', 'Sr', 'Y' ,                                                                                     'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I' , 'Xe',
'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W' , 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U' , 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og',
'Uue', 'NaE'
]

_basicCharges = [
1,                                                                                               0,
1, 2,                                                                         3, -4, -3, -2, -1, 0,
1, 2,                                                                         3, -4, -3, -2, -1, 0,
1, 2, 9,                                           9, 9, 9, 9, 9, 9, 9, 9, 9, 3, -4, -3, -2, -1, 0,
1, 2, 9,                                           9, 9, 9, 9, 9, 9, 9, 9, 9, 3,  9, -3, -2, -1, 0,
1, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3,  9, -3, -2, -1, 0,
1, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3,  9, -3, -2, -1, 0,
9, 9
]

IONIC_CHARGES = dict(zip(ELEMENTS, _basicCharges))

IONIC_CHARGES['Zn'] = 2
IONIC_CHARGES['Ag'] = 1
IONIC_CHARGES['Sn'] = 9
IONIC_CHARGES['Pb'] = 9

with open(r'/home/Robert/Documents/Misc. Repos/Periodic-Table-JSON/PeriodicTableJSON.json', 'r') as f:
    elementalInfo = json.load(f)

elementalInfo = elementalInfo["elements"]


class Element:
    "Creates an element"

    def __init__(self, string):
        self.symbol = "NaE"
        self.amount = 1
        # self.amount = int(self.amount)

        try:
            self.symbol = re.match(r'([A-Z][a-z])|([A-Z])', string)[0]
            string = string.replace(self.symbol, '', re.match(r'([A-Z][a-z])|([A-Z])', string).endpos)
        except:
            pass
        try:
            self.amount = re.match(r'(\d\d)|\d', string)[0]
        except:
            pass

    def draw(self):
        print(self.symbol, end = '', sep = '')
        if self.amount != 1:
            print(self.amount, end = '', sep = '')

    def getWeight(self):
        try:
            return elementalInfo[self.symbol]["atomic_mass"] * self.amount
        except:
            print('Error: Invalid Element')

    def ionicCharge(self):
        return IONIC_CHARGES[self.symbol]

    def getFullName(self):
        return elementalInfo[self.symbol]['name']


class Compound:
    "A collection of elements"

    def __init__(self, string):
        self.amount = 1
        self.elements = []

        while string:
            try:
                findElement = re.match(r'([A-Z][a-z]\d\d)|([A-Z][a-z]\d)|([A-Z][a-z])|([A-Z]\d\d)|([A-Z]\d)|([A-Z])', string)
                element = Element(findElement[0])
                string = string.replace(findElement[0], '', findElement.endpos)

                self.elements.append(element)
            except:
                pass

    def draw(self):
        if self.amount != 1:
            print(int(self.amount), end = '', sep = '')
            print('(', end = '', sep = '')
        for i in self.elements:
            i.draw()
        if self.amount != 1:
            print(')', end='', sep = '')

    def getWeight(self):
        total = 0
        for i in self.elements:
            total += i.getWeight()
        return total

    def isIonicBond(self):
        print("I still don't completely understand this myself, so... 6.")
        return True

    def getName(self):
        name = "Sodium triwhoknows dioxlalate"
        return name


class Equation:

    def __init__(self, formula):
        self.leftSide = []
        self.rightSide = []

        # take out all the whitespace
        formula = formula.replace(' ', '')

        # split by +'s
        formula = re.split(r'[-][>]', formula)

        left  = formula.pop(0)
        right = formula.pop(0)
        left  = re.split(r'[+]', left)
        right = re.split(r'[+]', right)

        for i in left:
            compound = Compound(i)
            self.leftSide.append(compound)

        for i in right:
            compound = Compound(i)
            self.rightSide.append(compound)

    def draw(self):
        print('')
        for i in self.leftSide:
            i.draw()
            if i != self.leftSide[len(self.leftSide) - 1]:
                print(" + ", end = '', sep = '')

        print(" -> ", end = '', sep = '')

        for c in self.rightSide:
            c.draw()
            if c != self.rightSide[len(self.rightSide) - 1]:
                print(" + ", end = '', sep = '')

        print('')

    def getType(self):
        print("I haven't done this yet...")

    def isBalanced(self):
        leftTotals, rightTotals = {}, {}

        for leftCompound in self.leftSide:
            for leftElement in leftCompound.elements:
                if leftElement.symbol in leftTotals:
                    leftTotals[leftElement.symbol] += int(leftElement.amount) * leftCompound.amount
                else:
                    leftTotals[leftElement.symbol] = int(leftElement.amount) * leftCompound.amount

        for rightCompound in self.rightSide:
            for rightElement in rightCompound.elements:
                if rightElement.symbol in rightTotals:
                    rightTotals[rightElement.symbol] += int(rightElement.amount) * rightCompound.amount
                else:
                    rightTotals[rightElement.symbol] = int(rightElement.amount) * rightCompound.amount

        for sym, amt in leftTotals.items():
            if rightTotals[sym] != amt:
                return False

        return True

    def balanceCoeficients(self):
        if self.isBalanced():
            pass
        else:
            els = list()

            # Get a list of element symbols
            for compound in self.leftSide:
                for element in compound.elements:
                    els.append(element.symbol)

            els_index = dict(zip(els, range(len(els))))  # {'C': 0, 'H': 1, 'O': 2}

            # Build matrix to solve
            w = len(self.leftSide) + len(self.rightSide) # 4
            h = len(els) # 3
            A = [[0] * w for _ in range(h)] # [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

            # load the matrix with element coefficients
            for col, compound in enumerate(self.leftSide):
                for el in compound.elements:
                    row = els_index[el.symbol]
                    A[row][col] = int(el.amount)
            for col, compound in enumerate(self.rightSide, len(self.leftSide)):
                for el in compound.elements:
                    row = els_index[el.symbol]
                    A[row][col] = -int(el.amount)   # invert coefficients for RHS

            # Solve using Sympy for absolute-precision math
            A = sympy.Matrix(A)

            # find first basis vector == primary solution
            coeffs = A.nullspace()[0]

            # find least common denominator, multiply through to convert to integer solution
            coeffs *= sympy.lcm([term.q for term in coeffs])

            tmp = 0

            for i, comp in enumerate(self.leftSide):
                comp.amount = coeffs[i]
                tmp = i
            for i, comp in enumerate(self.rightSide):
                comp.amount = coeffs[i+tmp+1]


print('''
Welcome to Copeland's Stoichometric Helper!\n
Enter a compound, an element, or a solved or unsovled chemical equation for more options.
''')

choice = input()

# is an equation
if re.match(r"[->]", choice):
    formula = Equation(choice)
    if formula.isBalanced():
        subChoice = input('''
        I see you\'ve entered a balanced chemical formula. Press I for info about the formula, R to
        go back to the beginning, or Q to quit.
        ''')

        if   subChoice.upper() == 'I':
            getInfo(formula)
        elif subChoice.upper() == 'R':
            restart = True
        elif subChoice.upper() == 'Q':
            quit(0)




# is a compound
if re.match(r"([A-Z][a-z]\d\d)|([A-Z][a-z]\d)|([A-Z][a-z])|([A-Z]\d\d)|([A-Z]\d)|([A-Z][A-Z])", choice):

# is an element
if re.match(r'([A-Z][a-z])|([A-Z])', choice):


formula = Equation(input("Enter chemical formula, or enter to quit:\n"))

# useful for debugging
# debugFormula = "C8H18 + O2 -> CO2 + H2O"
# debugFormula = "C8H8 + C2H2 -> C5H5"
# print(debugFormula)
# formula = Equation(debugFormula)

formula.draw()

print('')
formula.balanceCoeficients()
formula.draw()
print(formula.isBalanced())