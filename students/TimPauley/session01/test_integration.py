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

from inventory_management.main  import main_menu
from inventory_management.electricManagement import electricAppliances
from inventory_management.exceptions import InsufficientOperands
from inventory_management.furnitureClass import furniture
from inventory_management.marketprices import get_latest_price


class ModuleTests(TestCase):

    def test_module(self):
        