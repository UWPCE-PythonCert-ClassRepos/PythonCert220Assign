#Tim Pauley
#Date: Jan 12 2019
#Assignment 01
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


class Test_market_prices(TestCase):
    def test_market_price(self):
        market_price = get_latest_price()
        self.assertEqual(market_price, 24)


class Test_ElectricApplianceClass(TestCase):
    def test_init(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        item_dict["brand"] = "b"
        item_dict["voltage"] = 2
        e = ElectricAppliances(**item_dict)
        self.assertEqual(e.product_code, 2)
        self.assertEqual(e.description, "b")
        self.assertEqual(e.rental_price, 2.0)
        self.assertEqual(e.market_price, 2.0)
        self.assertEqual(e.brand, "b")
        self.assertEqual(e.voltage, 2)

    def test_return_as_dictionary(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        item_dict["brand"] = "b"
        item_dict["voltage"] = 2
        e = ElectricAppliances(**item_dict)
        new_dict = e.return_as_dictionary()
        self.assertEqual(e.product_code, new_dict["product_code"])
        self.assertEqual(e.description, new_dict["description"])
        self.assertEqual(e.brand, new_dict["brand"])
        self.assertEqual(e.voltage, new_dict["voltage"])

    def test_check_wattage(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        item_dict["brand"] = "b"
        item_dict["voltage"] = 10
        e = ElectricAppliances(**item_dict)
        wattage = e.check_wattage(10)
        self.assertEqual(wattage, 250)


class Test_FurnitureClass(TestCase):
    def test_init(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        item_dict["item_material"] = "b"
        item_dict["size"] = "D"
        f = Furniture(**item_dict)
        self.assertEqual(f.product_code, 2)
        self.assertEqual(f.description, "b")
        self.assertEqual(f.rental_price, 2.0)
        self.assertEqual(f.market_price, 2.0)
        self.assertEqual(f.material, "b")
        self.assertEqual(f.size, "D")

    def test_return_as_dictionary(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        item_dict["item_material"] = "a"
        item_dict["size"] = "S"
        f = Furniture(**item_dict)
        new_dict = f.return_as_dictionary()
        self.assertEqual(f.product_code, new_dict["product_code"])
        self.assertEqual(f.description, new_dict["description"])
        self.assertEqual(f.rental_price, new_dict["rental_price"])
        self.assertEqual(f.material, new_dict["material"])
        self.assertEqual(f.size, new_dict["size"])

    def test_check_for_big_screen(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        item_dict["item_material"] = "a"
        item_dict["size"] = "S"
        f = Furniture(**item_dict)
        self.assertEqual(f.check_for_big_screen(), False)
        f.size = "XL"
        self.assertEqual(f.check_for_big_screen(), True)


class Test_InventoryClass(TestCase):
    def test_init(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        i = Inventory(**item_dict)
        self.assertEqual(i.product_code, 2)
        self.assertEqual(i.description, "b")
        self.assertEqual(i.rental_price, 2.0)
        self.assertEqual(i.market_price, 2.0)

    def test_return_as_dictionary(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        i = Inventory(**item_dict)
        new_dict = i.return_as_dictionary()
        self.assertEqual(i.product_code, new_dict["product_code"])
        self.assertEqual(i.description, new_dict["description"])
        self.assertEqual(i.rental_price, new_dict["rental_price"])

    def test_check_market_price(self):
        item_dict = {}
          item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        i = Inventory(**item_dict)
        self.assertEqual(i.check_market_price(), False)
        i.market_price = get_latest_price()
        self.assertEqual(i.check_market_price(), True)


class Test_Main(TestCase):
    def test_generate_menu(self):
        self.assertEqual(generate_menu("Z"), False)
        self.assertEqual(generate_menu("1").__name__, "add_new_item")
        self.assertEqual(generate_menu("2").__name__, "item_info")
        self.assertEqual(generate_menu("q").__name__, "exit_program")

    def test_get_price(self):
        self.assertEqual(get_price(), get_latest_price())

    def test_return_item_info(self):
        item_dict = {}
        item_dict["item_code"] = 2
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = 2.0
        item_dict["item_price"] = 2.0
        i1 = Inventory(**item_dict)
        item_dict1 = {}
        item_dict1["item_code"] = 2
        item_dict1["item_description"] = "b"
        item_dict1["item_rental_price"] = 2.0
        item_dict1["item_price"] = 2.0
        i2 = Inventory(**item_dict1)
        f_inventory = {}
        f_inventory["1"] = i1.return_as_dictionary()
        f_inventory["2"] = i2.return_as_dictionary()
        self.assertEqual(
            return_item_info(f_inventory, "2"),
            "product_code:1\ndescription:a\nmarket_price:1.0\nrental_price:1.0\n"
        )
        self.assertEqual(
            return_item_info(f_inventory, "2"),
            "product_code:2\ndescription:b\nmarket_price:2.0\nrental_price:2.0\n"
        )
        self.assertEqual(
            return_item_info(f_inventory, "z"), "Item not found in inventory")

    def test_add_new_item_furniture(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        item_dict = {}
        item_dict["item_code"] = "1"
        item_dict["item_description"] = "a"
        item_dict["item_rental_price"] = "1.0"
        item_dict["item_price"] = "1.0"
        item_dict["item_material"] = "a"
        item_dict["size"] = "S"
        item_dict["style"] = "furniture"
        user_input = ["1", "a", "1.0", "y", "a", "S"]
        f_inventory = {}
        f = Furniture(**item_dict)
        f_inventory = {}
        with patch('builtins.input', side_effect=user_input):
            f_inventory = add_new_item(f_inventory)
        new_dict = f_inventory["1"]
        f = Furniture(**item_dict)
        new_dict1 = f.return_as_dictionary()
        self.assertEqual(new_dict["product_code"], new_dict1["product_code"])
        self.assertEqual(new_dict["description"], new_dict1["description"])
        self.assertEqual(new_dict["rental_price"], new_dict1["rental_price"])
        self.assertEqual(new_dict["material"], new_dict1["material"])
        self.assertEqual(new_dict["size"], new_dict1["size"])
        sys.stdout = sys.__stdout__

    def test_add_new_item_electrical(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        user_input = ["2", "b", "2.0", "n", "y", "b", "2.0"]
        f_inventory = {}
        with patch('builtins.input', side_effect=user_input):
            f_inventory = add_new_item(f_inventory)
        new_dict = f_inventory["2"]
        item_dict = {}
        item_dict["item_code"] = "2"
        item_dict["item_description"] = "b"
        item_dict["item_rental_price"] = "2.0"
        item_dict["item_price"] = "2.0"
        item_dict["brand"] = "b"
        item_dict["voltage"] = "2.0"
        e = ElectricAppliances(**item_dict)
        new_dict1 = e.return_as_dictionary()
        self.assertEqual(new_dict["product_code"], new_dict1["product_code"])
        self.assertEqual(new_dict["description"], new_dict1["description"])
        self.assertEqual(new_dict["brand"], new_dict1["brand"])
        self.assertEqual(new_dict["voltage"], new_dict1["voltage"])
        sys.stdout = sys.__stdout__

    def test_add_new_item_inventory(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        user_input = ["3", "c", "3.0", "n", "n"]
        f_inventory = {}
        with patch('builtins.input', side_effect=user_input):
            f_inventory = add_new_item(f_inventory)
        new_dict = f_inventory["3"]
        item_dict = {}
        item_dict["item_code"] = "3"
        item_dict["item_description"] = "c"
        item_dict["item_rental_price"] = "3.0"
        item_dict["item_price"] = get_latest_price()
        i = Inventory(**item_dict)
        new_dict1 = i.return_as_dictionary()
        self.assertEqual(new_dict["product_code"], new_dict1["product_code"])
        self.assertEqual(new_dict["description"], new_dict1["description"])
        self.assertEqual(new_dict["rental_price"], new_dict1["rental_price"])
        self.assertEqual(new_dict["market_price"], new_dict1["market_price"])
        sys.stdout = sys.__stdout__

    def test_exit_program(self):
        f_inventory = {}
        self.assertRaises(SystemExit, exit_program, f_inventory)

    def test_main_menu(self):
        user_input = ["1"]
        text_trap = io.StringIO()
        sys.stdout = text_trap
        with patch('builtins.input', side_effect=user_input):
            function = main_menu()
        self.assertEqual(function.__name__, "add_new_item")
        sys.stdout = sys.__stdout__
    
    def test_item_info(self):
        f_inventory={}
        text_trap = io.StringIO()
        sys.stdout = text_trap
        user_input=["1"]
        with patch('builtins.input', side_effect=user_input):
            check_f_inventory=item_info(f_inventory)
        self.assertEqual(f_inventory,check_f_inventory)  




 