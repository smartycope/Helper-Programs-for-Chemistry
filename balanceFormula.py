import re
from collections import Counter
# import collections

MM_of_Elements = {'H' : 1.00794,     'He': 4.002602,  'Li': 6.941,     'Be': 9.012182, 'B' : 10.811,      'C' : 12.0107,
                  'N' : 14.0067,     'O' : 15.9994,   'F' : 18.9984032,'Ne': 20.1797,  'Na': 22.98976928, 'Mg': 24.305,
                  'Al': 26.9815386,  'Si': 28.0855,   'P' : 30.973762, 'S' : 32.065,   'Cl': 35.453,      'Ar': 39.948,
                  'K' : 39.0983,     'Ca': 40.078,    'Sc': 44.955912, 'Ti': 47.867,   'V' : 50.9415,     'Cr': 51.9961,
                  'Mn': 54.938045,   'Fe': 55.845,    'Co': 58.933195, 'Ni': 58.6934,  'Cu': 63.546,      'Zn': 65.409,
                  'Ga': 69.723,      'Ge': 72.64,     'As': 74.9216,   'Se': 78.96,    'Br': 79.904,      'Kr': 83.798,
                  'Rb': 85.4678,     'Sr': 87.62,     'Y' : 88.90585,  'Zr': 91.224,   'Nb': 92.90638,    'Mo': 95.94,
                  'Tc': 98.9063,     'Ru': 101.07,    'Rh': 102.9055,  'Pd': 106.42,   'Ag': 107.8682,    'Cd': 112.411,
                  'In': 114.818,     'Sn': 118.71,    'Sb': 121.760,   'Te': 127.6,    'I' : 126.90447,   'Xe': 131.293,
                  'Cs': 132.9054519, 'Ba': 137.327,   'La': 138.90547, 'Ce': 140.116,  'Pr': 140.90465,   'Nd': 144.242,
                  'Pm': 146.9151,    'Sm': 150.36,    'Eu': 151.964,   'Gd': 157.25,   'Tb': 158.92535,   'Dy': 162.5,
                  'Ho': 164.93032,   'Er': 167.259,   'Tm': 168.93421, 'Yb': 173.04,   'Lu': 174.967,     'Hf': 178.49,
                  'Ta': 180.9479,    'W' : 183.84,    'Re': 186.207,   'Os': 190.23,   'Ir': 192.217,     'Pt': 195.084,
                  'Au': 196.966569,  'Hg': 200.59,    'Tl': 204.3833,  'Pb': 207.2,    'Bi': 208.9804,    'Po': 208.9824,
                  'At': 209.9871,    'Rn': 222.0176,  'Fr': 223.0197,  'Ra': 226.0254, 'Ac': 227.0278,    'Th': 232.03806,
                  'Pa': 231.03588,   'U' : 238.02891, 'Np': 237.0482,  'Pu': 244.0642, 'Am': 243.0614,    'Cm': 247.0703,
                  'Bk': 247.0703,    'Cf': 251.0796,  'Es': 252.0829,  'Fm': 257.0951, 'Md': 258.0951,    'No': 259.1009,
                  'Lr': 262,         'Rf': 267,       'Db': 268,       'Sg': 271,      'Bh': 270,         'Hs': 269,
                  'Mt': 278,         'Ds': 281,       'Rg': 281,       'Cn': 285,      'Nh': 284,         'Fl': 289,
                  'Mc': 289,         'Lv': 292,       'Ts': 294,       'Og': 294,      'ZERO': 0
                  }

class Element:
    "Creates an element"

    def __init__(self, string):
        self.name = "ZERO"
        self.amount = 1

        try:
            self.name = re.match(r'([A-Z][a-z])|([A-Z])', string)[0]
            string = string.replace(self.name, '', re.match(r'([A-Z][a-z])|([A-Z])', string).endpos)
        except:
            ''
        try:
            self.amount = re.match(r'(\d\d)|\d', string)[0]
        except:
            ''
    def draw(self):
        print(self.name, end = '', sep = '')
        if self.amount != 1:
            print(self.amount, end = '', sep = '')


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
                ''

    def draw(self):
        if self.amount != 1:
            print(self.amount, end = '', sep = '')
            print('(', end = '', sep = '')
        for i in self.elements:
            i.draw()
        if self.amount != 1:
            print(')', end='', sep = '')

    def getWeight(self):
        print("I haven't implemented this yet. Sorry :(")


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


'''
#use a dictionary to map elements to their weights
weights = MM_of_Elements

def getInt(clist):
    """helper for parsing a list of chars as an int (returns 1 for empty list)"""
    if not clist: return 1
    return int(''.join(clist))




def getWeight(formula):
    """ get the combined weight of the formula in the input string """
    formula = list(formula)
    #initialize the weight to zero, and a list as a buffer for numbers
    weight = 0
    num_buffer = []
    #get the first element weight
    el_weight = weights[formula.pop(0)]
    while formula:
        next = formula.pop(0)
        if next in weights:
            #next character is an element, add current element weight to total
            weight += el_weight * getInt(num_buffer)
            #get the new elements weight
            el_weight = weights[element]
            #clear the number buffer
            num_buffer = []
        else:
            #next character is not an element -> it is a number, append to buffer
            num_buffer.append(next)
    #add the last element's weight and return the value
    return weight + el_weight * getInt(num_buffer)


def getWeight(formula):
    """ get the combined weight of the formula in the input string """


    #initialize the weight to zero, and a list as a buffer for numbers
    weight = 0
    num_buffer = []
    name_buffer = []
    #get the first element weight
    el_weight = weights[formula.pop(0)]

    while formula:
        next = formula.pop(0)
        second = formula.pop(0)
        # cheating to treat the list like a vector
        formula.insert(0, second)

        if next.digit():
            num_buffer.append(next)
        elif next.alpha() and next.upper():
            name_buffer.append(next)


        if next in weights:
            #next character is an element, add current element weight to total
            weight += el_weight * getInt(num_buffer)
            #get the new elements weight
            el_weight = weights[element]
            #clear the number buffer
            num_buffer = []
        elif next.lower():
            if next in weights:
            #next character is an element, add current element weight to total
            weight += el_weight * getInt(num_buffer)
            #get the new elements weight
            el_weight = weights[element]
            #clear the number buffer
            num_buffer = []
    #add the last element's weight and return the value

    # while formula:


    return weight + el_weight * getInt(num_buffer)



while True:
    #main loop
    chemical_formula = input("Enter chemical formula, or enter to quit: ")
    if not chemical_formula:
        break
    parseEquation(chemical_formula).draw();
    # print("Combined weight is %s" % getWeight(chemical_formula))

'''



# Compound = input('Molar Mass Caluclator \nExample: H2O not h2o \nEnter Compound Formula: ')
# IsPolyatomic, End, Multiply = False, False, False
# PolyatomicMass, MM, Multiplier = 0, 0, 1
# Element = 'ZERO'

# for i in range(0, len(Compound) + 1):
#     E = Compound[i:i + 1]
#     if IsPolyatomic:
#         if End:
#             IsPolyatomic = False
#             MM += int(E) * PolyatomicMass
#         elif E.isdigit():
#             if Multiply: Multiplier = int(str(Multiplier) + E)
#             else: Multiplier = int(E)
#             Multiply = True
#         elif E.islower(): Element += E
#         elif E.isupper():
#             PolyatomicMass += Multiplier * MM_of_Elements[Element]
#             Element, Multiplier, Multiply = E, 1, False
#         elif E == ')':
#             PolyatomicMass += Multiplier * MM_of_Elements[Element]
#             Element, Multiplier = 'ZERO', 1
#             End, Multiply = True, False
#     elif E == '(':
#         MM += Multiplier * MM_of_Elements[Element]
#         Element, Multiplier = 'ZERO', 1
#         IsPolyatomic, Multiply = True, False
#     elif E.isdigit():
#         if Multiply:
#             Multiplier = int(str(Multiplier) + E)
#         else: Multiplier = int(E)
#         Multiply = True
#     elif E.islower(): Element += E
#     elif E.isupper():
#         MM += Multiplier * MM_of_Elements[Element]
#         Element, Multiplier, Multiply = E, 1, False
#     elif i == len(Compound):
#         MM += Multiplier * MM_of_Elements[Element]
#         Element, Multiplier, Multiply = E, 1, False
# print(f'The Molar mass of {Compound} is {round(MM)} g/mol')





'''
atom_regex = '([A-Z][a-z]*)(\d*)'
openers = '({['
closers = ')}]'


def is_balanced(formula):
    """Check if all sort of brackets come in pairs."""
    # Very naive check, just here because you always need some input checking
    c = Counter(formula)
    return c['['] == c[']'] and c['{'] == c['}'] and c['('] == c[')']


def _dictify(tuples):
    """Transform tuples of tuples to a dict of atoms."""
    res = dict()
    for atom, n in tuples:
        try:
            res[atom] += int(n or 1)
        except KeyError:
            res[atom] = int(n or 1)
    return res


def _fuse(mol1, mol2, w=1):
    """
    Fuse 2 dicts representing molecules. Return a new dict.
    This fusion does not follow the laws of physics.
    """
    return {atom: (mol1.get(atom, 0) + mol2.get(atom, 0)) * w for atom in set(mol1) | set(mol2)}


def _parse(formula):
    """
    Return the molecule dict and length of parsed part.
    Recurse on opening brackets to parse the subpart and
    return on closing ones because it is the end of said subpart.
    """
    q = []
    mol = {}
    i = 0

    while i < len(formula):
        # Using a classic loop allow for manipulating the cursor
        token = formula[i]

        if token in closers:
            # Check for an index for this part
            m = re.match('\d+', formula[i+1:])
            if m:
                weight = int(m.group(0))
                i += len(m.group(0))
            else:
                weight = 1

            submol = _dictify(re.findall(atom_regex, ''.join(q)))
            return _fuse(mol, submol, weight), i

        elif token in openers:
            submol, l = _parse(formula[i+1:])
            mol = _fuse(mol, submol)
            # skip the already read submol
            i += l + 1
        else:
            q.append(token)

        i+=1

    # Fuse in all that's left at base level
    return _fuse(mol, _dictify(re.findall(atom_regex, ''.join(q)))), i


def parse_formula(formula):
    """Parse the formula and return a dict with occurences of each atom."""
    if not is_balanced(formula):
        raise ValueError("Watch your brackets ![{]$[&?)]}!]")

    return _parse(formula)[0]
'''

print("C8H18 + O2 -> CO2 + H2O")
# formula = Equation(input("Enter chemical formula, or enter to quit:\n"))
formula = Equation("C8H18 + O2 -> CO2 + H2O")
formula.draw()

# C8H18 + O2 -> CO2 + H2O