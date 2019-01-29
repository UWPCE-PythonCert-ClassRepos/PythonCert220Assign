#!/usr/bin/env Python3

"""Unit Test for Inventory Management Module"""
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from inventory_management import market_prices
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.main import *


def get_input(text):
    """attempt using mock patch"""
    return input(text)


class main_test(TestCase):
    """Test Main.py"""

    def test_main_menu(self):
        mock = MagicMock()
        mock[1] = "Enter item code: "
        mock.__setitem__.assert_called_with(1, "Enter item code: ")
        mock['Anything'] = "Enter item description: "
        mock.__setitem__.assert_called_with('Anything', "Enter item description: ")

class Inventory_test(TestCase):
    """Test Inventory module"""

    def test_return_as_dictionary(self):
        new_rug = Inventory('25',
                            'floor rug',
                            '$1000',
                            '$100')
        assert new_rug.rental_price == "$100"
        assert new_rug.rental_price == "$100"


class ElectricAppliances_test(TestCase):
    """"Test Electric Appliances Module"""

    def test_return_as_dictionary(self):
        new_refer = ElectricAppliances('333',
                                       'Stainless Steel Refigerator',
                                       '$800',
                                       '$100',
                                       'Maytag',
                                       '25')
        assert new_refer.product_code == '333'
        assert new_refer.voltage == '25'


class Furniture_test(TestCase):
    """Test Furniture module"""

    def test_return_as_dictionary(self):
        new_sofa = Furniture("222",
                             "awesome sofa",
                             '$250',
                             "$25",
                             "fake suede",
                             'S')
        assert new_sofa.product_code == '222'


class Market_Prices_test(TestCase):
    """Test Market Prices"""

    def test_get_latest_price(self):
        assert market_prices.get_latest_price("Useless module") == 24
