"""
this if for integration test
"""

import pdb
import unittest
from unittest.mock import patch
from unittest import TestCase
from unittest.mock import MagicMock

import numpy as mp

from inventory_management.market_prices import get_latest_price
from inventory_management.inventoryclass import Inventory
from inventory_management.furnitureclass import Furniture
from inventory_management.electricappliancesclass import ElectricAppliances

from inventory_management.development import *

def test_all():
    assert get_latest_price() == 10

    user_input = [3]

    with patch('builtins.input', side_effect=user_input):
        item_info()

    try:
        exit_program()
    except SystemExit:
        pass

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


