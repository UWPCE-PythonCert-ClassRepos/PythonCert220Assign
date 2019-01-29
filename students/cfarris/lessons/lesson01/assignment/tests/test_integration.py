#!/usr/bin/env Python 3

"""test integration of Inventory management testing"""

from unittest import TestCase
#from unittest.mock import MagicMock
from unittest.mock import patch
import unittest


from main import main_menu, add_new_item, get_latest_price, get_input, exit_program, item_info
from inventory_management import market_prices
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory


class ModuleTests(TestCase):

    def test_main_adding_furniture(self):
        """tests I can add a furniture and electrical item using main"""
        user_input =['1',
                     '222',
                     'awesome sofa',
                     '$250',
                     'Y',  #yes, its a piece of furniture
                     'fake suede',
                     'S',
                     '',
                     '2',
                     '222',
                     '',                   
                     'q'
                     ]         

        with patch('builtins.input', side_effect=user_input):
            stacks = main_menu()
            stacks2 = stacks()
            print('stacks2', stacks2)
        assert stacks == add_new_item
        assert stacks2 == {'333': {'product_code': '333', 'description': 'refigerator', 'market_price': 24, 'rental_price': '$1250', 'brand': 'amana', 'voltage': '125v'}, '222': {'product_code': '222', 'description': 'awesome sofa', 'market_price': 24, 'rental_price': '$250', 'material': 'fake suede', 'size': 'S'}}

    def test_main_adding_electrical_appliance(self):
        """tests I can add an electrical item using main"""
        electrical_input =['1',
                     '333',
                     'refigerator',
                     '$1250',
                     'N',  #No, its not a piece of furniture
                     'Y',  #yes it is an electrical_appliance
                     'amana',
                     '125v',
                     '',
                     '2',
                     '333',
                     '',
                     'q'
                     ]

        with patch('builtins.input', side_effect=electrical_input):
            A = main_menu()
            B = A()
            print('B', B)
        assert A == add_new_item
        assert B == {'333': {'product_code': '333', 'description': 'refigerator', 'market_price': 24, 'rental_price': '$1250', 'brand': 'amana', 'voltage': '125v'}}
