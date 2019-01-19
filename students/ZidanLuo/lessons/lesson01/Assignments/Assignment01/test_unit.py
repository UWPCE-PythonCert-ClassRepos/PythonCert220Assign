"""
This is a unit test for all classes in the inventory management system
"""
from unittest import TestCase
from unittest.mock import patch

import sys

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from main import main_menu, add_new_item, get_price, item_info, exit_program, get_input
import main
 



class FurnitureTests(TestCase):
    """
    This class tests all the methods in the furniture_class
    """
    def test_furniture(self):
        info = {}
        info['product_code'] = '1001'
        info['description'] = 'chair'
        info['market_price'] = '80'
        info['rental_price'] = '20'
        info['material'] = 'wood'
        info['size'] = 'S'
        furniture = Furniture(info)

        result = furniture.return_as_dictionary()
        self.assertEqual(result['product_code'], "1001")
        self.assertEqual(result['description'], 'chair')
        self.assertEqual(result['market_price'], '80')
        self.assertEqual(result['rental_price'] , '20')
        self.assertEqual(result['material'], 'wood')
        self.assertEqual(result['size'], 'S')
 


class InventoryTests(TestCase):
    """
    This class tests all the methods in the inventory_class
    """

    def test_output_dict(self):
        info = {}
        info['product_code'] = '1001'
        info['description'] = 'chair'
        info['market_price'] = '80'
        info['rental_price'] = '20'
        inventory = Inventory(info)

        result = inventory.return_as_dictionary()
        self.assertEqual(result['product_code'], "1001")
        self.assertEqual(result['description'], 'chair')
        self.assertEqual(result['market_price'], '80')
        self.assertEqual(result['rental_price'] , '20')
        


class ElectricAppliancesTests(TestCase):
    """
    This class tests the electric appliances methods
    """

    def test_output(self):
        info = {}
        info['product_code'] = '1002'
        info['description'] = 'heater'
        info['market_price'] = '500'
        info['rental_price'] = '100'
        info['brand'] = 'GE'
        info['voltage'] = '110v'
        heater = ElectricAppliances(info)

        result = heater.return_as_dictionary()
        self.assertEqual(result['product_code'], "1002")
        self.assertEqual(result['description'], 'heater')
        self.assertEqual(result['market_price'], '500')
        self.assertEqual(result['rental_price'] , '100')
        self.assertEqual(result['brand'], 'GE')
        self.assertEqual(result['voltage'], '110v')


class MainMenuTests(TestCase):
    """
    This class tests the methods in the Main module
    """
    @patch('main.main_menu',return_value=add_new_item)
    def test_get_price(self, main_menu):
        self.assertEqual(main_menu(1), add_new_item)

    @patch('main.main_menu',return_value=item_info)
    def test_item_info(self, main_menu):
        self.assertEqual(main_menu(2), item_info)

    @patch('main.main_menu',return_value=exit_program)
    def test_exit_program(self, main_menu):
        self.assertEqual(main_menu('q'), exit_program)

    @patch('main.add_new_item')
    def test_add_inventory(self, mock_add_inventory):
        add_new_item()
        self.assertTrue(main.FULL_INVENTORY)
    