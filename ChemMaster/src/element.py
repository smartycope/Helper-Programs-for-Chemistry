# from dataclasses import dataclass
import re

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

class NotAnElementError(Exception):
    pass

# @dataclass
class Element:
    "Creates an element"
    def __init__(self, string):
        self.symbol = "NaE"
        self.amount = 1
        # self.amount = int(self.amount)

        try:
            self.symbol = re.match(r'([A-Z][a-z])|([A-Z])', string)[0]
            string = string.replace(self.symbol, '', re.match(r'([A-Z][a-z])|([A-Z])', string).endpos)
            if self.symbol not in ELEMENTS:
                raise NotAnElementError
        except(TypeError):
            pass
        try:
            self.amount = re.match(r'(\d\d)|\d', string)[0]
            # string = string.replace(self.symbol, '', re.match(r'(\d\d)|\d', string).endpos)
        except(TypeError):
            pass

    def draw(self):
        print(self.symbol, end = '', sep = '')
        if self.amount != 1:
            print(self.amount, end = '', sep = '')

    def getWeight(self):
        try:
            return elementalInfo[self.symbol]["atomic_mass"] * int(self.amount)
        except:
            print('Error: Invalid Element "', end='')
            self.draw()
            print('"')
            # print(f'symbol = {self.symbol} | amount = {self.amount}')

    def ionicCharge(self):
        return IONIC_CHARGES[self.symbol]

    def getFullName(self):
        return elementalInfo[self.symbol]['name']
