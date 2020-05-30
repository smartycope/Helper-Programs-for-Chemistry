# from dataclasses import dataclass
import re

# @dataclass
class Equation:
    def __init__(self, formula):
        self.leftSide = []
        self.rightSide = []

        # print("formula that equation got is", formula)

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

    def getType(self):
        "Unfinished"
        type = 'precipitation'
        return type

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
