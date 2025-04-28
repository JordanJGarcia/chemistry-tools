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

        # each formula stores the following data
        self.setMolecules([])
        self.setFormula("")
        self.setWeight(0.0)
        self.setGrams(0.0)
        self.setMoles(0.0)
        self.setML(0.0)

    # setters
    def setMolecules(self, m: list):
        self.molecules = m

    def setFormula(self, f: str):
        self.formula = f

    def setWeight(self, w: float):
        self.weight = w

    def setGrams(self, g: float):
        self.grams = g

    def setMoles(self, m: float):
        self.moles = m

    def setML(self, m: float):
        self.ml = m

    # getters
    def getMolecules(self):
        return self.molecules

    def getFormula(self):
        return self.formula

    def getWeight(self):
        return self.weight

    def getGrams(self):
        return self.grams

    def getMoles(self):
        return self.moles

    def getML(self):
        return self.ml


    # other
    def loadPeriodicTable(self):
        with open("elements.csv", encoding="utf-8") as file:
            for row in csv.reader(file):
                self.elements[row[1]] = Element(row)

    
    def prompt(self):
        """ this is the main menu the user interfaces with """

        i = 0

        while True:

            if i == 0:
                entry = input("Enter formula: ")
            else:
                entry = input("Enter new formula, or (m) moles to grams (g) grams to moles (M) moles to mL: ")

            print("")
            
            if entry == "exit":
                break
            elif entry == "m":
                # ensure valid formula has been provided
                if not self.getFormula():
                    print("ERROR: formula not provided\n", file=sys.stderr)
                    continue

                self.molesToGrams()
            elif entry == "g":
                if not self.getFormula():
                    print("ERROR: formula not provided\n", file=sys.stderr)
                    continue

                self.gramsToMoles()
            elif entry == "M":
                if not self.getFormula():
                    print("ERROR: formula not provided\n", file=sys.stderr)
                    continue

                self.molesToML()
            else: # user entered a formula
                self.setMolecules(self.breakDownFormula(entry))

                if not self.getMolecules():
                    continue

                self.setFormula(entry)
                self.setMoles(0.0)
                self.setGrams(0.0)
                self.setML(0.0)
                self.calculateWeight()

                if self.getWeight() == 0:
                    print(f"ERROR: could not calculate weight for {self.getFormula()}\n", file=sys.stderr)
                    self.setFormula("")
                    i = 0 # to reset prompt
                    continue
                else:
                    print(f"\tformula: {self.getFormula()}, weight: {self.getWeight()}\n")
                    self.calculatePercentageComposition(self.getMolecules())
                    print("")

            i += 1


    def elementExists(self, element: str):
        """ check if element exists in *our* periodic table, which is populated from the elements.csv file """

        if not element in self.elements:
            print(f"ERROR: {element} not found\n", file=sys.stderr)
            return 0

        self.elements[element].printElement()
        return 1

    
    def breakDownFormula(self, formula: str):
        """ this will return a list with the separate molecules (as lists themselves) in the provided formula """
        """ or it will return an empty list upon error """

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
                        return []

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
            return []

        return molecules



    def calculateWeight(self):
        """ calculate the total weight of the current formula """
        
        weight = 0

        for m in self.molecules:
            try:
               elementWeight  = float(m[1])
            except ValueError:
                print(f"ERROR: {m[0]} weight '{m[1]}' not a float", file=sys.stderr)
                return 0

            weight += elementWeight * int(m[2])

        self.setWeight(weight)



    def calculatePercentageComposition(self, molecules: list):
        """ calculate the percentage composition of each element in the formula """
        
        for m in molecules:
            moleculeWeight = float(m[1]) * int(m[2])
            percentage = moleculeWeight / self.getWeight() * 100

            s = int(m[2]) if int(m[2]) > 1 else ""
            print(f"\t{m[0]}{s}: {moleculeWeight}g / {self.getWeight()}g * 100 = {percentage} %")

            # store percentage composition for other uses
            m.append(moleculeWeight / self.getWeight())


    def requestValue(self, value: float, unit: str):
        """ used to check if user wants to use current value in moles/mL/grams or set a new value """

        req = ""

        if value != 0:
            while True:
                req = input(f"use {value} {unit}? (y or n) ")

                if req != "n" and req != "y":
                    print(f"\nERROR: invalid option '{req}'\n", file=sys.stderr)
                    continue
                break

        if req == "n" or value == 0:
            while True:
                req = input(f"enter {unit}: ")

                try:
                    newValue = float(req)
                except ValueError:
                    print("\nERROR: not a float\n", file=sys.stderr)
                    continue
                return newValue

        return value


    def molesToGrams(self):
        """ converts a certain amount of moles to grams """
    
        self.setMoles(self.requestValue(self.getMoles(), "mol"))
        self.setGrams(float(self.getWeight() * self.getMoles()))

        print(f"\n\t{self.getMoles()} mol {self.getFormula()} = {self.getGrams()} g\n")


    def gramsToMoles(self):
        """ converts a certain amount of grams to moles """

        self.setGrams(self.requestValue(self.getGrams(), "g"))
        self.setMoles(float(self.getGrams() / self.getWeight()))

        print(f"\n\t{self.getGrams()} g {self.getFormula()} = {self.getMoles()} mol\n")


    def molesToML(self):
        """ converts given moles to a liquid molarity """

        self.setMoles(self.requestValue(self.getMoles(), "mol"))

        while True:
            req = input("M of solution (moles/1000ml): ")

            try:
                molarity = float(req)
            except ValueError:
                print("\nERROR: not a float\n", file=sys.stderr)
                continue
            break


        self.setML(float(self.getMoles() * 1000 / molarity))
        print(f"\n\t{self.getMoles()} mol {self.getFormula()} of {molarity} M solution = {self.getML()} mL\n")
        


if __name__ == "__main__":
    calc = StoichiometryCalculator()
