#Tim Pauley
#Date: Jan 12 2019
#Assignment 01 
#Update Assignment 01
#Jan 20 2018
#Note: due to a new workload at my day job, i needed additional
#time to work on updates.

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
'''
added addiontional namespaces
'''
from unittest.mock import patch
import sys
import io

from inventory_management.market_prices import get_latest_price
from inventory_management.InventoryClass import Inventory
from inventory_management.ElectricAppliancesClass import ElectricAppliances
from inventory_management.FurnitureClass import Furniture
'''
import additional methods
'''

from inventory_management.Main import main_menu
from inventory_management.Main import generate_menu
from inventory_management.Main import get_price
from inventory_management.Main import add_new_item
from inventory_management.Main import input_item_info
from inventory_management.Main import return_item_info
from inventory_management.Main import exit_program
from inventory_management.Main import item_info

class ModuleTests(TestCase):

    def test_module(self):
        