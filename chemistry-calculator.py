#! /usr/bin/python3

import csv
import sys


# global funcs

# c => class
# f => function 
# m => message
def error(c: str, f: str, m: str):
    print(f"ERROR -  {c}.{f}(): {m}\n", file=sys.stderr)

# c => class
# f => function 
# m => message
# code => exit code
def error_exit(c: str, f: str, m: str, code: int):
    print(f"ERROR -  {c}.{f}(): {m}\n", file=sys.stderr)
    sys.exit(code)


# valid subshell types
electron_spins = {0: "\u2191", 1: "\u2193"}
subshell_types = ['s', 'p', 'd', 'f']
orbital_amount = {}

amount = 1
for t in subshell_types:
    orbital_amount[t] = amount
    amount += 2


# object oriented stuff

class Electron(object):
    """ representing an electron, duh """

    def __init__(self, spin: int):
        self.set_spin(spin)


    def set_spin(self, spin: int):

        if spin not in electron_spins:
            error_exit("Electron", "set_spin", f"invalid spin {spin}, must be one of {electron_spins}", 1)

        self.spin = spin


    def __repr__(self, ):
        return electron_spins[self.spin]

        


class Orbital(object):
    """ magnetic quantum number """
    """ represents orbitals within a subshell """

    # t => type of subshell these orbitals are in (s,p,d,f)
    def __init__(self, t: str):

        if t not in subshell_types:
            error_exit("Orbital", "__init__", f"invalid subshell type {t}", 1)

        self.type = t
        self.electrons = []
        self.count = orbital_amount[self.type]

        # add as many empty orbitals as needed for subshell type
        for i in range(0, self.count):
            # None will represent no electron
            # -0.5 will be one spin
            # 0.5 will be the other
            self.electrons.append([None,None])
            

   
    # ml => magnetic quantum number
    # ms => spin quantum number, but for this its only 'up' or 'down'
    def update_electron(self, ml: int, ms: int):

        max_ml = orbital_amount[self.type]

        # valid ml is -l to +l
        if ml > max_ml or ml < 0:
            error_exit("Orbital", "update_electron", f"invalid magnetic quantum number {ml}, valid values are -{max_ml} to +{max_ml}", 1)

        # valid ms is -0.5 or +0.5
        if ms not in electron_spins:
            error_exit("Orbital", "update_electron", f"invalid spin quantum number {ms} valid values are {list(electron_spins.keys())}", 1)

        self.electrons[ml][ms] = Electron(ms)
        



    def print_orbitals(self):

        print(*self.electrons)
        #for e in self.electrons:
            #print(f"\t\t{e}", end=' ')



class Subshell(object):
    """ aziumuthal quantum number (l) """
    """ represents a subshell within a shell """

    # t => type of subshell (s,p,d,f)
    def __init__(self, t: str):

        if t not in subshell_types:
            error_exit("Subshell", "__init__", f"invalid subshell type {t}", 1)

        self.type = t
        self.orbitals = Orbital(t)

    
    def print_subshell(self, n=''):
        print(f"    {n}{self.type}: ", end='')
        self.orbitals.print_orbitals()


class Shell(object):
    """ principal quantum number (n) """
    """ represents a shell of an atom """

    # n => the principal quantum number
    def __init__(self, n: int):

        # just to be safe, exit gracefully
        if len(subshell_types) != 4:
            error_exit("Shell", "__init__", f"subshell types are invalid {subshell_types}, check code", 1)

        # although theoretically this number can go to infinity
        # there are only 7 periods on the periodic table
        if n > 7:
            error_exit("Shell", "__init__", f"invalid principal quantum number {n}", 1)

        self.n = n
        self.subshells = {}

        # each shell has s subshell
        self.add_subshell(subshell_types[0])

        # shells 2 and up have p subshell
        if n > 1:
            self.add_subshell(subshell_types[1])

        # shells 4 and above have d subshell
        if n > 3:
            self.add_subshell(subshell_types[2])

        # shells 6 and above have  f subshell
        if n > 5:
            self.add_subshell(subshell_types[3])

                        
    
    # t => subshell type
    def add_subshell(self, t: str):

        if t not in subshell_types:
            error_exit("Shell", "add_subshell", f"invalid subshell type {t}", 1)

        self.subshells[t] = Subshell(t)
        

    def print_shell(self):

        print(f"shell {self.n}\n")
        for s in self.subshells.values():
            s.print_subshell(self.n)

        print("")


class Element(object):
    """ object representing an element in the periodic table """

    #def __init__(self, info: list, protons: int, neutrons: int, electrons: int):
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

    def setGroup(self, g: str):
        self.group = g

    def setPeriod(self, p: str):
        self.period = p

    def setOrbitalDiagram(self, n: int, l: int, ml: int, ms: float):
        self.pqm = n    # principal quantum number
        self.aqm = l    # azimuthal quantum number
        self.mqm = ml   # magnetic quantum number
        self.sqm = ms   # spin quantum number

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
        # store elements in various dictionaries to make it easy
        # to search by name/symbol/number/weight
        self.elementsByName = {}
        self.elementsBySymbol = {} 
        self.elementsByNumber = {}
        self.elementsByWeight = {}

        self.loadPeriodicTable()
        self.resetData()
        self.prompt()

    def resetData(self):
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
                self.elementsByName[row[0]] = Element(row)
                self.elementsBySymbol[row[1]] = Element(row)
                self.elementsByNumber[row[2]] = Element(row)
                self.elementsByWeight[row[3]] = Element(row)


    def displayMenu(self, showFullMenu: bool):
        shortMenu = "entry: "
        fullMenu = """Enter a formula at any time, or choose from the following:

        d) display full menu
        g) grams to moles
        m) moles to grams
        M) moles to ML
        s) search
        x) exit, or type "exit"

entry: """

        return input(fullMenu) if showFullMenu else input(shortMenu)
    

    def prompt(self):
        """ this is the main menu the user interfaces with """

        fullMenu = True

        while True:

            entry = self.displayMenu(fullMenu)

            fullMenu = False
            print("")
            
            if entry == "exit" or entry == "x":
                break
            elif entry == "d":
                fullMenu = True
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
            elif entry == "s":
                self.search()
            else: # user entered a formula
                self.setMolecules(self.breakDownFormula(entry))

                if not self.getMolecules():
                    continue

                self.setFormula(entry)
                self.calculateWeight()

                if self.getWeight() == 0:
                    print(f"ERROR: could not calculate weight for {self.getFormula()}\n", file=sys.stderr)
                    self.resetData()
                else:
                    print(f"\tformula: {self.getFormula()}, weight: {self.getWeight()}\n")
                    self.calculatePercentageComposition(self.getMolecules())
                    print("")


    def elementExists(self, element: str):
        """ check if element exists in *our* periodic table, which is populated from the elements.csv file """

        if not element in self.elementsBySymbol:
            print(f"ERROR: {element} not found\n", file=sys.stderr)
            return 0

        self.elementsBySymbol[element].printElement()
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
                        molecule = [ element, self.elementsBySymbol[element].getWeight(), subscript ]
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
            molecule = [ element, self.elementsBySymbol[element].getWeight(), subscript ]
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


    def request(self, value: float, unit: str):
        """ used to check if user wants to use current value in moles/mL/grams or set a new value """

        req = ""

        # if value isn't empty, ask user if they want to use it
        if value != 0:
            while True:
                req = input(f"use {value} {unit}? (y or n) ")

                if req != "n" and req != "y":
                    print(f"\nERROR: invalid option '{req}'\n", file=sys.stderr)
                    continue
                break

        # user entered 'n', or value is empty
        if req == "n" or value == 0:
            while True:
                req = input(f"enter {unit}: ")

                try:
                    newValue = float(req)
                except ValueError:
                    print("\nERROR: not a float\n", file=sys.stderr)
                    continue
                return newValue

        # user entered 'y', so use current value
        return value


    def molesToGrams(self):
        """ converts a certain amount of moles to grams """
    
        self.setMoles(self.request(self.getMoles(), "mol"))
        self.setGrams(float(self.getWeight() * self.getMoles()))

        print(f"\n\t{self.getMoles()} mol {self.getFormula()} = {self.getGrams()} g\n")


    def gramsToMoles(self):
        """ converts a certain amount of grams to moles """

        self.setGrams(self.request(self.getGrams(), "g"))
        self.setMoles(float(self.getGrams() / self.getWeight()))

        print(f"\n\t{self.getGrams()} g {self.getFormula()} = {self.getMoles()} mol\n")


    def molesToML(self):
        """ converts given moles to a liquid molarity """

        self.setMoles(self.request(self.getMoles(), "mol"))

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


    def search(self):
        """ will search for an element by specified criteria and print its data """

        key = input("\nsearch by number, weight or symbol: ")

        print("")
        if key in self.elementsByName:
            self.elementsByName[key].printElement()
        elif key in self.elementsBySymbol:
            self.elementsBySymbol[key].printElement()
        elif key in self.elementsByNumber:
            self.elementsByNumber[key].printElement()
        elif key in self.elementsByWeight:
            self.elementsByWeight[key].printElement()
        else:
            print(f"ERROR: key '{key}' not found\n", file=sys.stderr)

        return
       


if __name__ == "__main__":
    #calc = StoichiometryCalculator()

    s = {}

    for i in range(1,9):
        s[i] = Shell(i)

        for ss in s[i].subshells.values():
            for j in range(0, ss.orbitals.count):
                ss.orbitals.update_electron(j, 0)
                ss.orbitals.update_electron(j, 1)

        s[i].print_shell()


