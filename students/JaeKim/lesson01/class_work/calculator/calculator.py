"""Calculator"""

from .exceptions import InsufficientOperands

class Calculator():
    """Class for Calculator"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Class to subtract"""
        self.stack.append(number)

    def _do_calc(self, operator):
        """Class to subtract"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Class to subtract"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Class to subtract"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Class to subtract"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Class to subtract"""
        return self._do_calc(self.divider)
