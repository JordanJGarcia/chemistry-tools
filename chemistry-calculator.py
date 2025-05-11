#! /usr/bin/python3

import csv
import sys
import math


#####################################
#                                   #
#             globals               #
#                                   #
#####################################

# c => class
# f => function 
# m => message
def error(c: str, f: str, m: str):
    print(f"ERROR - {c}.{f}(): {m}\n", file=sys.stderr)

# code => exit code
def error_exit(c: str, f: str, m: str, code: int):
    print(f"ERROR - {c}.{f}(): {m}\n", file=sys.stderr)
    sys.exit(code)


electron_spins = {0: "\u2191", 1: "\u2193"}
subshell_types = ['s', 'p', 'd', 'f']
orbital_amount = {}

amount = 1
for t in subshell_types:
    orbital_amount[t] = amount
    amount += 2



#####################################
#                                   #
#             classes               #
#                                   #
#####################################

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
    """ represents an orbital within a subshell """

    def __init__(self):

        # each orbital has up to 2 electrons
        # None will be no electron
        # 0 will be one spin
        # 1 will be the other
        self.electrons = [None, None]

   
    def set_electron(self, spin: int):
        if spin not in electron_spins:
            error_exit("Orbital", "set_electron", f"invalid spin {spin}", 1)

        self.electrons[spin] = Electron(spin)


    def unset_electron(self, spin: int):
        if spin not in electron_spins:
            error_exit("Orbital", "set_electron", f"invalid spin {spin}", 1)

        self.electrons[spin] = None


    def print_orbital(self):
        print(self.electrons, end=' ')


class Subshell(object):
    """ aziumuthal quantum number (l) """
    """ represents a subshell within a shell """

    # t => type of subshell (s,p,d,f)
    def __init__(self, t: str):

        if t not in subshell_types:
            error_exit("Subshell", "__init__", f"invalid subshell type {t}", 1)

        self.type = t
        self.orbitals = []
        self.add_orbitals()

    
    def add_orbitals(self):
        count = orbital_amount[self.type]

        # add as many empty orbitals as needed for subshell type
        for i in range(0, count):
            self.orbitals.append(Orbital())


    # orbital => magnetic quantum number (ml)
    # spin    => spin quantum number (ms)
    def update_electron(self, orbital: int, spin: int):

        max_orbital = orbital_amount[self.type]

        # valid ml is 0 to l-1
        if orbital >= max_orbital or orbital < 0:
            error_exit("Orbital", "update_electron", f"invalid orbital {orbital}, valid values are 0 to {max_orbital - 1}", 1)

        # valid ms is 0 or 1
        if spin not in electron_spins:
            error_exit("Orbital", "update_electron", f"invalid electron spin {spin} valid values are {list(electron_spins.keys())}", 1)

        self.orbitals[orbital].set_electron(spin)

    
    def print_subshell(self, n=''):
        print(f"    {n}{self.type}: ", end='')

        for o in self.orbitals:
            o.print_orbital()

        print("")


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

    def __init__(self, info: list):
        assert len(info) == 4

        self.set_name(str(info[0]))
        self.set_symbol(str(info[1]))
        self.set_weight(str(info[3]))

        self.set_protons(int(info[2]))
        self.set_neutrons(round(self.get_weight()) - self.get_protons())
        self.set_electrons(self.get_protons())


    def set_name(self, n: str):
        self.name = n

    def set_symbol(self, s: str):
        self.symbol = s

    def set_weight(self, w: str):
        self.weight = float(w)

    def set_protons(self, n: int):
        self.protons = n

    def set_neutrons(self, n: int):
        self.neutrons = n

    def set_electrons(self, n: int):
        self.electrons = n

    def set_group(self, g: str):
        self.group = g

    def set_period(self, p: str):
        self.period = p

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol

    def get_weight(self):
        return self.weight

    def get_protons(self):
        return self.protons

    def get_neutrons(self):
        return self.neutrons

    def get_electrons(self):
        return self.electrons

    def print_element(self):
        info = [
            f"\tElement:    {self.get_name()}",
            f"\tSymbol:     {self.get_symbol()}",
            f"\tWeight:     {self.get_weight()}",
            f"\tP:          {self.get_protons()}",
            f"\tN:          {self.get_neutrons()}",
            f"\tE:          {self.get_electrons()}\n"
        ]

        for s in info:
            print(s)


class Molecule(object):
    """ represents a Molecule """

    def __init__(self):
        self.elements = {} # this will be a dict of dicts


    # formula => molecular formula to use
    # elmenents => dict of elements with their symbols as keys
    def build_molecule(self, formula: str, elements: dict):
        """ this will build the Molecule object based on the supplied formula """

        if not elements or not isinstance(list(elements.values())[0], Element):
            error("Molecule", "__init__", f"expected dict of Element objects, got {type(elements)}")
            return 0

        self.elements.clear()

        symbol = ""
        subscript = "1"
        i = 0

        # iterate through formula
        while i < len(formula):
            # start of element
            if formula[i].isupper():
                # store previous molecule
                if symbol:
                    if not symbol in elements:
                        error("StoichiometryCalculator", "build_molecule", f"{symbol} not found")
                        return 0

                    elements[symbol].print_element()
                    self.add_element(elements[symbol], subscript)

                # new molecule
                symbol = formula[i]
                subscript = "1"

            # 2 character element name
            if formula[i].islower():
                symbol += formula[i]

            # subscript
            if i != 0 and formula[i].isdigit():
                subscript = formula[i]

                while i + 1 < len(formula) and formula[i + 1].isdigit():
                    subscript += formula[i + 1]
                    i += 1

            i += 1

        # store last molecule
        if symbol:
            if not symbol in elements:
                error("StoichiometryCalculator", "build_molecule", f"{symbol} not found")
                return 0
                
            elements[symbol].print_element()
            self.add_element(elements[symbol], subscript)

        return 1


    def add_element(self, element: Element, count: int):
        # elements[<Element object>] = { count, percentage }
        self.elements[element] = {'count': count, 'percentage': 0}

        self.calculate_formula()
        self.calculate_weight()
        self.calculate_percentage_compositions()


    def get_weight(self):
        return self.weight


    def calculate_weight(self):
        self.weight = 0

        for e, d in self.elements.items():
            self.weight += (e.get_weight() * int(d['count']))


    def calculate_percentage_compositions(self):
        """ calculate the percentage composition of an element in the formula """

        for e, d in self.elements.items():
            weight = float(e.get_weight() * int(d['count']))
            d['percentage'] = weight / self.get_weight() * 100


    def calculate_formula(self):
        f = ""
        for e, d in self.elements.items():
            f += e.get_symbol()
            f += d['count'] if int(d['count']) > 1 else ""

        self.formula = f


    def __repr__(self):
        s = f"formula:    {self.formula}"
        s += "\n\tweight:     {:<10} g".format(self.get_weight())

        percentage = {}
        grams = {}

        for e, d in self.elements.items():
            count = d['count'] if int(d['count']) > 1 else ""
            percentage[e.get_symbol() + str(count)] = str(d['percentage']) + " %"
            grams[e.get_symbol() + str(count)] = "{:<10} g".format(e.get_weight() * int(d['count']))

        for k, v in percentage.items():
            s += "\n\t{:<12}{:<12}".format(k, grams[k])
            t = f"({v})"
            s += " {:<17}".format(t)

        return s


class StoichiometryCalculator(object):
    """ object representing the periodic table of elements """

    def __init__(self):
        # store elements in various dictionaries to make it easy
        # to search by name/symbol/number/weight
        self.elements_by_name = {}
        self.elements_by_symbol = {} 
        self.elements_by_number = {}
        self.elements_by_weight = {}

        self.molecule = Molecule()

        self.load_elements()
        self.reset_data()
        self.prompt()

    def reset_data(self):
        self.set_formula("")
        self.set_grams(0.0)
        self.set_moles(0.0)
        self.set_mL(0.0)

    # setters
    def set_formula(self, f: str):
        self.formula = f

    def set_grams(self, g: float):
        self.grams = g

    def set_moles(self, m: float):
        self.moles = m

    def set_mL(self, m: float):
        self.mL = m

    # getters
    def get_molecules(self):
        return self.molecule

    def get_formula(self):
        return self.formula

    def get_weight(self):
        return self.molecule.get_weight()

    def get_grams(self):
        return self.grams

    def get_moles(self):
        return self.moles

    def get_mL(self):
        return self.mL


    # load elements from periodic table, as found in elements.csv file
    def load_elements(self):
        with open("elements.csv", encoding="utf-8") as file:
            for row in csv.reader(file):
                self.elements_by_name[row[0]] = Element(row)
                self.elements_by_symbol[row[1]] = Element(row)
                self.elements_by_number[row[2]] = Element(row)
                self.elements_by_weight[row[3]] = Element(row)


    def display_menu(self, show_full_menu: bool):
        short_menu = "entry (d) display menu, (s) search, (x) exit: "
        full_menu = """Enter a formula at any time, or choose from the following:

        d) display full menu
        g) grams to moles
        m) moles to grams
        M) moles to ML
        s) search
        x) exit, or type "exit"

entry: """

        return input(full_menu) if show_full_menu else input(short_menu)
    

    def prompt(self):
        """ this is the main menu the user interfaces with """

        full_menu = True

        while True:
            entry = self.display_menu(full_menu)
            full_menu = False
            print("")
            
            if entry == "exit" or entry == "x":
                break
            elif entry == "d":
                full_menu = True
            elif entry == "m":
                if not self.get_formula():
                    error("StoichiometryCalculator", "prompt", "formula not provided")
                    continue

                self.moles_to_grams()
            elif entry == "g":
                if not self.get_formula():
                    error("StoichiometryCalculator", "prompt", "formula not provided")
                    continue

                self.grams_to_moles()
            elif entry == "M":
                if not self.get_formula():
                    error("StoichiometryCalculator", "prompt", "formula not provided")
                    continue

                self.moles_to_mL()
            elif entry == "s":
                self.search()
            else: # user entered a formula
                if not self.molecule.build_molecule(entry, self.elements_by_symbol):
                    error("StoichiometryCalculator", "prompt", f"could not build molecule {entry}")
                    continue

                self.set_formula(entry)
                print(f"\t{self.molecule}\n")


    def request(self, value: float, unit: str):
        """ used to check if user wants to use current value in moles/mL/grams or set a new value """

        req = ""

        # if value isn't empty, ask user if they want to use it
        if value != 0:
            while True:
                req = input(f"use {value} {unit}? (y or n) ")

                if req != "n" and req != "y":
                    error("StoichiometryCalculator", "request", f"invalid option {req}")
                    continue
                break

        # user entered 'n', or value is empty
        if req == "n" or value == 0:
            while True:
                req = input(f"enter {unit}: ")

                try:
                    newValue = float(req)
                except ValueError:
                    error("StoichiometryCalculator", "request", f"not a float")
                    continue
                return newValue

        # user entered 'y', so use current value
        return value


    def moles_to_grams(self):
        """ converts a certain amount of moles to grams """
    
        self.set_moles(self.request(self.get_moles(), "mol"))
        self.set_grams(float(self.get_weight() * self.get_moles()))

        print(f"\n\t{self.get_moles()} mol {self.get_formula()} = {self.get_grams()} g\n")


    def grams_to_moles(self):
        """ converts a certain amount of grams to moles """

        self.set_grams(self.request(self.get_grams(), "g"))
        self.set_moles(float(self.get_grams() / self.get_weight()))

        print(f"\n\t{self.get_grams()} g {self.get_formula()} = {self.get_moles()} mol\n")


    def moles_to_mL(self):
        """ converts given moles to a liquid molarity """

        self.set_moles(self.request(self.get_moles(), "mol"))

        while True:
            req = input("M of solution (moles/1000mL): ")

            try:
                molarity = float(req)
            except ValueError:
                error("StoichiometryCalculator", "moles_to_mL", f"not a float")
                continue
            break


        self.set_mL(float(self.get_moles() * 1000 / molarity))
        print(f"\n\t{self.get_moles()} mol {self.get_formula()} of {molarity} M solution = {self.get_mL()} mL\n")


    def search(self):
        """ will search for an element by specified criteria and print its data """

        key = input("search by number, weight or symbol: ")

        print("")
        if key in self.elements_by_name:
            self.elements_by_name[key].print_element()
        elif key in self.elements_by_symbol:
            self.elements_by_symbol[key].print_element()
        elif key in self.elements_by_number:
            self.elements_by_number[key].print_element()
        elif key in self.elements_by_weight:
            self.elements_by_weight[key].print_element()
        else:
            error("StoichiometryCalculator", "search", f"key '{key}' not found")

        return
       


if __name__ == "__main__":
    calc = StoichiometryCalculator()

#    s = {}
#
#    for i in range(1,9):
#        s[i] = Shell(i)
#
#        for ss in s[i].subshells.values():
#            for j in range(0, len(ss.orbitals)):
#                ss.update_electron(j, 0)
#                ss.update_electron(j, 1)
#
#        s[i].print_shell()


