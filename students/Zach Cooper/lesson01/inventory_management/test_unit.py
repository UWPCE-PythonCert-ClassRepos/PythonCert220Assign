from unittest import TestCase, patch
from unittest.mock import MagicMock

from inventory_class import Inventory
from market_prices import get_latest_price
from electric_appliances import ElectricAppliances
from furntire_class import Furniture
from main import *


class ApplianceTests(TestCase):

    def test_appliance(self):
        item = ElectricAppliances()
        item = electric_appliances_class.ElectricAppliances(23, 'an item',
                                                            24, 90, 'Kenmore',
                                                            130)

        assert item.product_code == 23
        assert item.description == 'an item'
        assert item.market_price == 24
        assert item.rental_price == 90
        assert item.brand == 'kenmore'
        assert item.voltage == 130
        assert item.return_as_dictionary() == {'product_code': 23,
                                               'description': 'an item',
                                               'market_price': 24,
                                               'rental_price': 90,
                                               'brand': 'Kenmore',
                                               'voltage': 130,
                                               }


class FurnitureTests(TestCase):

    def test_furniture(self):
        item = Furniture()
        item = furnitrue_class.Furniture(23, 'an item', 24, 90, 'leather', 'M')

        assert item.product_code == 23
        assert item.description == 'an item'
        assert item.market_price == 24
        assert item.rental_price == 90
        assert item.material == 'Leather'
        assert item.size == 'M'
        assert item.return_as_dictionary() == {'product_code': 23,
                                               'description': 'an item',
                                               'market_price': 24,
                                               'rental_price': 90,
                                               'size': 'M',
                                               'material': 'Leather',
                                               }


class InvetoryTests(TesCase):

    def test_inventory(self):
        item = Inventory()
        item = inventory_class.Inventory(23, 'an item', 24, 90)

        assert item.product_code == 23
        assert item.desciprtion == 'an item'
        assert item.market_price == 24
        assert item.rental_price == 90
        assert item.return_as_dictionary() == {'product_code': 23,
                                               'description': 'an item',
                                               'market_price': 24,
                                               'rental_price': 90,
                                               }

class 

 self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price






class TestMain(TestCase):

    # @patch('main.get_input', return_value='1')
    # """Changed all of the input() functions in the main to
    # get_input() which goes to a seperate function for the input"""

    # def test_main_addNewItem(self, mock_mainMenu):

    #     self.assertEqual(mainMenu(), addNewItem)



    # # test add_new_item is_furniture
    # def test_main_is_furniture():
    #     with unittest.mock.patch('builtins.input', return_value='y'):
    #         assert input() == 'y'





    """item_info function"""
    @patch('builtins.input', return_value='1')
    def test_item_info(self):

        self.assertEqual(item_info(), '1')
