#! /usr/bin/python3

import csv
import sys

class Element(object):
    """ object representing an element in the periodic table """

    def __init__(self, info: list):
        assert len(info) == 4

        self.setNumber(int(info[2]))
        self.setName(str(info[0]))
        self.setSymbol(str(info[1]))
        self.setWeight(str(info[3]))

    def setName(self, n: str):
        self.name = n

    def setSymbol(self, s: str):
        self.symbol = s

    def setNumber(self, n: int):
        self.number = n

    def setWeight(self, w: str):
        self.weight = w

    def getName(self):
        return self.name

    def getSymbol(self):
        return self.symbol

    def getNumber(self):
        return self.number

    def getWeight(self):
        return self.weight

    def printElement(self):
        print(f"\tNumber: {self.number}\n\tName:   {self.name}\n\tSymbol: {self.symbol}\n\tWeight: {self.weight}\n")


class StoichiometryCalculator(object):
    """ object representing the periodic table of elements """

    def __init__(self):
        self.elements = {} # dict holding 118 elements
        self.loadPeriodicTable()
        self.prompt()

    def loadPeriodicTable(self):
        with open("elements.csv", encoding="utf-8") as file:
            for row in csv.reader(file):
                self.elements[row[1]] = Element(row)

    
    def prompt(self):

        i = 0
        molecules = []
        formula = ""
        weight = 0.0

        while True:

            if i == 0:
                entry = input("Enter formula: ")
            else:
                entry = input("Enter new formula, or (1) moles to grams (2) grams to moles: ")

            print("")
            
            if entry == "exit":
                break
            elif entry == "1":
                # use formula that has been entered already
                if not formula:
                    print("ERROR: formula not provided\n", file=sys.stderr)
                    continue

                self.molesToGrams(formula, weight)
            elif entry == "2":
                # use formula that has been entered already

                if not formula:
                    print("ERROR: formula not provided\n", file=sys.stderr)
                    continue

                self.gramsToMoles(formula, weight)
            else: # user entered a formula
                molecules = self.breakDownFormula(entry)

                if molecules:
                    formula = entry
                    weight = self.getWeight(molecules)
                    print(f"\tformula: {formula}, weight: {weight}\n")

                    p = self.getPercentageComposition(molecules)
                    print("")

            i += 1


    def elementExists(self, element: str):

        if not element in self.elements:
            print(f"ERROR: {element} not found\n", file=sys.stderr)
            return 0

        self.elements[element].printElement()
        return 1

    
    def breakDownFormula(self, formula: str):
        """ this will return a list with the separate molecules in the provided formula """

        molecule = []  # this will store info about the individual molecule
        molecules = [] # this will store the complete set of molecule information

        element = ""
        subscript = "1"
        i = 0

        while i < len(formula):

            # start of element
            if formula[i].isupper():

                # store previous molecule
                if element:
                    if self.elementExists(element):
                        molecule = [ element, self.elements[element].getWeight(), subscript ]
                        molecules.append(molecule)
                    else:
                        return 0

                # new molecule
                element = formula[i]
                subscript = "1"

            # 2 character element name
            if formula[i].islower():
                element += formula[i]

            # subscript
            if i != 0 and formula[i].isdigit():
                subscript = formula[i]
                
                while i + 1 < len(formula) and formula[i + 1].isdigit():
                    subscript += formula[i + 1]
                    i += 1

            i += 1

        # store last molecule
        if self.elementExists(element):
            molecule = [ element, self.elements[element].getWeight(), subscript ]
            molecules.append(molecule)
        else:                                                                                                                                                                                 
            return 0

        return molecules



    def getWeight(self, molecules: list):
        """ calculate the total weight of the formula in grams """
        
        weight = 0

        for m in molecules:
            weight += float(m[1]) * int(m[2])

        return weight



    def getPercentageComposition(self, molecules: list):
        """ calculate the percentage composition of each element in the formula """
        
        totalWeight = self.getWeight(molecules)

        for m in molecules:
            weight = float(m[1]) * int(m[2])
            s = int(m[2]) if int(m[2]) > 1 else ""
            print(f"\t{m[0]}{s}: {weight}g / {totalWeight}g * 100 = {weight / totalWeight * 100} %")

            # store percentage composition for other uses
            m.append(weight / totalWeight)


    def molesToGrams(self, formula: str, weight: float):
        """ converts a certain amount of moles to grams """

        req = input("Enter moles: ")

        try:
            moles = float(req)
        except ValueError:
            print("ERROR: not a float\n", file=sys.stderr)
            return 0

        print(f"\n\t{moles} mol {formula} = {weight * moles} g\n")


    def gramsToMoles(self, formula: str, weight: float):
        """ converts a certain amount of grams to moles """

        req = input("Enter grams: ")

        try:
            grams = float(req)
        except ValueError:
            print("ERROR: not a float\n", file=sys.stderr)
            return 0

        print(f"\n\t{grams} g {formula} = {grams / weight} mol\n")



if __name__ == "__main__":
    calc = StoichiometryCalculator()
