# from dataclasses import dataclass
import re
from element import Element
import json

with open(r'/home/Robert/hello/chemistry programs/ChemMaster/PeriodicTableJSON.json', 'r') as f:
    elementalInfo = json.load(f)

# @dataclass
class Compound:
    "A collection of elements"

    def __init__(self, string):
        self.amount = 1
        self.elements = tuple()
        # print(f"The compound you just gave me is {string}")

        while string:
            # try:
            findElement = re.match(r'([A-Z][a-z]\d\d)|([A-Z][a-z]\d)|([A-Z][a-z])|([A-Z]\d\d)|([A-Z]\d)|([A-Z])', string)
            # print(f'Found element {findElement}')
            element = Element(findElement[0])
            string = string.replace(findElement[0], '', findElement.endpos)

            self.elements.append(element)
            # except:
                # print("I didn't see anything...")
                # pass

    def draw(self):
        if self.amount != 1:
            print(int(self.amount), end = '', sep = '')
            print('(', end = '', sep = '')
        for i in self.elements:
            i.draw()
        if self.amount != 1:
            print(')', end='', sep = '')

    def getWeight(self):
        total = int(0)
        for i in self.elements:
            total += i.getWeight()
        return total

    def isIonicBound(self):
        "Unfinished"
        # if len(self.elements) == 2:
        #     try:
        #         if re.match("(metal)|(^metaloid)|(^nonmetal)", elementalInfo[elements[0]])
        #            and re.match("(metal)|(^metaloid)|(^nonmetal)", elementalInfo[elements[1]]):
        #            return

        return True

    def getCharge(self):
        "Unfinished"
        return 9

    def getName(self):
        "Unfinished"
        name = "Sodium triwhoknows dioxlalate"
        return name
