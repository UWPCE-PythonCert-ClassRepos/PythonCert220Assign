#!/usr/bin/env Python3

"""Unit Test for Inventory Management Module"""
from unittest import TestCase
from unittest.mock import patch

from main import main_menu, add_new_item, get_latest_price, get_input, exit_program, item_info
from inventory_management import market_prices
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory


class main_test(TestCase):
    """Test Main.py to ensure it can route to and call the main"""

    def test_main_menu_1_adds(self):
        """test main menu will add when option 1 is entered"""
        with patch("builtins.input", return_value='1'):
            step_1 = main_menu()

        assert step_1 == add_new_item

    def test_main_menu_2_gets_inventory(self):
        """test main menu will add when option 1 is entered"""
        with patch("builtins.input", return_value='2'):
            step_2 = main_menu()

        assert step_2 == item_info

    def test_main_menu_q_exits(self):
        """test main menu will add when option 1 is entered"""
        with patch("builtins.input", return_value='q'):
            step_3 = main_menu()

        assert step_3 == exit_program

    def test_get_latest_price(self):
        """verify function will return 24"""
        assert get_latest_price("random") == 24


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
        assert get_latest_price("Useless module") == 24
