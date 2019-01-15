#Tim Pauley
#Date: Jan 12 2019
#Assignment 01

#Steps to complete

"""
Download the code for the inventory management system and place it 
in a folder called inventory_management.

Evaluate the code using Pylint by running the following command 
from outside of the inventory_management folder. 
Use this command: python -m pylint ./inventory_management

Fix all of the issues reported by Pylint up to the point where 
Pylint gives the code a grade of 10.

Create a file called test_unit.py that will be outside of the 
inventory_management directory. You will need to add unit tests 
for all classes in the inventory management system to this file.

Run coverage analysis on the inventory_management code using 
test_unit.py. Coverage must be 90% or higher for each individual 
file. Use the following commands.

Coverage run:
python -m coverage run --source=inventory_management -m unittest test_unit.py
Coverage report:
python -m coverage report
Update test_unit.py as required to attain 90% coverage.

Create a file called test_integration.py.
"""

from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.electricManagement import electricAppliances
from inventory_management.exceptions import InsufficientOperands
from inventory_management.furnitureClass import furniture
from inventory_management.marketprices import get_latest_price

class AdderTests(TestCase):

    def test_adding(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))



class SubtracterTests(TestCase):

    def test_subtracting(self):
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)



    def test_subtracter_call(self):
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiplier()

        self.subtracter.calc.assert_called_with(1, 2)

 
    def test_divider_call(self):
        self.divider.calc = MagicMock(return_value=0)

        self.divider.enter_number(1)
        self.divider.enter_number(2)
        self.divider.divider()

        self.divider.calc.assert_called_with(1, 2)