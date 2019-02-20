"""
Creates a virtual calculator
"""

from .exceptions import InsufficientOperands


class Calculator:
    """
    Can add, subtract, multiply, and divide numbers.
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Gets number from user
        :param number: number
        :return: stack
        """
        self.stack.append(number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Adds numbers
        :return: sum
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Subtracts numbers
        :return: difference
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Multiplies numbers
        :return: product
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Divides numbers
        :return: quotient
        """
        return self._do_calc(self.divider)
