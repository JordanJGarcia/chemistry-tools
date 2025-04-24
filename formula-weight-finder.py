#! /usr/bin/python3

import csv

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
        print(f"\nNumber: {self.number}\nName:   {self.name}\nSymbol: {self.symbol}\nWeight: {self.weight}\n")


class PeriodicTable(object):
    """ object representing the periodic table of elements """

    def __init__(self):
        self.elements = {} # dict holding 118 elements
        self.populate()
        self.prompt()

    def populate(self):
        with open("elements.csv", encoding="utf-8") as file:
            for row in csv.reader(file):
                self.elements[row[1]] = Element(row)

    
    def prompt(self):
        while True:
            f = input("Enter formula: ")

            if f == "exit":
                break

            self.getFormulaWeight(f)
                

    def getFormulaWeight(self, formula: str):
        
        element = ""
        subscript = "1"
        weight = 0

        i = 0
        size = len(formula)

        # get individual elements
        while i < size:

            # coefficient
            #if i == 0 and formula[i].isdigit():
            #    coefficient = int(formula[i])

            # start of element
            if formula[i].isupper():
                # save last molecule
                if element:
                    weight += (float(self.elements[element].getWeight()) * int(subscript))

                # new element found
                element = formula[i]
                subscript = "1"
            
            if formula[i].islower():
                element += formula[i]

            # subscript
            if i != 0 and formula[i].isdigit():
                subscript = formula[i]
                while i + 1 < len(formula) and formula[i + 1].isdigit():
                    subscript += formula[i + 1]
                    i += 1


            i += 1

        # save final molecule
        #print(f"molecule: {element}, subscript: {subscript}")
        weight += (float(self.elements[element].getWeight()) * int(subscript))
        print(f"formula: {formula}, weight: {weight}")


if __name__ == "__main__":
    table = PeriodicTable()
