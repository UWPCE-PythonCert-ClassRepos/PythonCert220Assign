''' Calculator functions '''
from .exceptions import InsufficientOperands


class Calculator:
    ''' Represents 4 basic math functions in calculator '''

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        '''
        Enter a number into stack

        :param number: number to add
        '''
        self.stack.append(number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        ''' Add numbers '''
        return self._do_calc(self.adder)

    def subtract(self):
        ''' Subtract numbers '''
        return self._do_calc(self.subtracter)

    def multiply(self):
        ''' Multiply numbers numbers '''
        return self._do_calc(self.multiplier)

    def divide(self):
        ''' Divide numbers '''
        return self._do_calc(self.divider)
