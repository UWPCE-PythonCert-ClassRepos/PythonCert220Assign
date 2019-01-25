"""Import insufficientOperands to catch this exception"""
from .exceptions import InsufficientOperands


class Calculator():
    """Simple calculator that performs basic arethmetic functions
    Params: adder, subtractor, multiplier, divider, numbers to perform operation
    Return: results from operation"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """represents the number added to calculator and appends to stack
        Params: number  """
        self.stack.append(number)

    def _do_calc(self, operator):
        """executes the operation with teh provided numbers stored in stack  """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Calls the adder operation"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Calls the subtract operation"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Calls the multiplier operation"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Calls the divide operation"""
        return self._do_calc(self.divider)
