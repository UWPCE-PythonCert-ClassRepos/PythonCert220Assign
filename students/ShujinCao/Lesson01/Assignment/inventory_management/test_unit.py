"""
this is for testing classes in the inventory management system
"""
import pdb
import unittest
from unittest.mock import patch
from unittest import TestCase
from unittest.mock import MagicMock

import numpy as mp
import pytest

from inventory_management.market_prices import get_latest_price
from inventory_management.inventoryclass import Inventory
from inventory_management.furnitureclass import Furniture
from inventory_management.electricappliancesclass import ElectricAppliances

from inventory_management.development import *


class TestMarketprices(TestCase):

    def test_get_latest_price(self):
        assert get_latest_price() == 10


class TestInventory(TestCase):

    def setUp(self):
        self.product_code = 1
        self.description = "House"
        self.market_price = 4
        self.rental_price = 2

        self.inventory = Inventory(self.product_code, self.description, self.market_price, self.rental_price)

    def test_inventory_return_as_dictionay(self):
        assert self.inventory.return_as_dictionary() == {'product_code': 1, 'description': 'House', 'market_price': 4, 'rental_price': 2}


class TestFurniture(TestCase):

    def setUp(self):
        self.product_code = 1
        self.description = "Sofa"
        self.market_price = 4
        self.rental_price = 2
        self.material = "wood"
        self.size = 5

        self.furniture= Furniture(self.product_code, self.description,
                                  self.market_price, self.rental_price,
                                  self.material, self.size)

    def test_furniture_return_as_dictionay(self):
        assert self.furniture.return_as_dictionary() == {'product_code': 1,
                                                         'description':
                                                         'Sofa',
                                                         'market_price': 4,
                                                         'rental_price': 2,
                                                         'material':'wood',
                                                         'size': 5}


class TestElectricAppliances(TestCase):

    def setUp(self):
        self.product_code = 1
        self.description = "Sofa"
        self.market_price = 4
        self.rental_price = 2
        self.brand = "wood"
        self.voltage = 5

        self.electricappliances = ElectricAppliances(self.product_code,
                                                     self.description,
                                                     self.market_price,
                                                     self.rental_price,
                                                     self.brand,
                                                     self.voltage)

    def test_electric_return_as_dictionay(self):
        assert self.electricappliances.return_as_dictionary() == {'product_code': 1,
                                                                  'description':
                                                                  'Sofa',
                                                                  'market_price': 4,
                                                                  'rental_price': 2,
                                                                  'brand':'wood',
                                                                  'voltage': 5}

class TestMain(TestCase):

    def test_add_items(self):
        user_input = [2, "oven", 2, "N", "Y", "wood", 5]

        with patch('builtins.input', side_effect=user_input):
            add_new_item()
        print(FULLINVENTORY)
        assert FULLINVENTORY == {2: {'product_code': 2, 'description': 'oven',
                                     'market_price': 10, 'rental_price': 2,
                                     'brand': 'wood', 'voltage': 5}}

        user_input = [7, "bread", 2, "N", "N", "Y"]

        with patch('builtins.input', side_effect=user_input):
            add_new_item()
        print(FULLINVENTORY)
        assert FULLINVENTORY == {2: {'product_code': 2, 'description': 'oven',
                                     'market_price': 10, 'rental_price': 2,
                                     'brand': 'wood', 'voltage': 5},
                                 7: {'product_code': 7, 'description': 'bread',
                                     'market_price': 10, 'rental_price': 2}}

        user_input = [1, "House", 2, "Y", "wood", "X"]

        with patch('builtins.input', side_effect=user_input):
            add_new_item()
        print(FULLINVENTORY)
        assert FULLINVENTORY == {1: {'product_code': 1, 'description': 'House',
                                     'market_price': 10, 'rental_price': 2,
                                     'material': 'wood', 'size': 'X'},
                                 2: {'product_code': 2, 'description': 'oven',
                                     'market_price': 10, 'rental_price': 2,
                                     'brand': 'wood', 'voltage': 5},
                                 7: {'product_code': 7, 'description': 'bread',
                                     'market_price': 10, 'rental_price': 2}}

    def test_item_info(self):
        user_input = [3]

        with patch('builtins.input', side_effect=user_input):
            item_info()

    def test_exit_program(self):
        try:
            exit_program()
        except SystemExit:
            pass


