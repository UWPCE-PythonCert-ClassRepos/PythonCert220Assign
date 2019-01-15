from unittest import TestCase
from unittest.mock import MagicMock

from furniture_class import Furniture
from market_prices import get_latest_price
from inventory_class import Inventory
from electric_appliances_class import ElectricAppliances
from main import *

class InventoryTests(TestCase):
    
    def test_inventory(self):
        inventory = Inventory(10, "thing", 24, 1000)

        out_dict = {"product_code": 10, "description": "thing",
        "market_price": 24, "rental_price": 1000}

        self.assertEqual(out_dict, inventory.return_as_dictionary())

class FurnitureTests(TestCase):

    def test_furniture(self):
        furniture = Furniture(10, "thing", 24, 1000, "feathers", 100)

        out_dict = {"product_code": 10, "description": "thing",
        "market_price": 24, "rental_price": 1000, "material": "feathers",
        "size": 100}

        self.assertEqual(out_dict, furniture.return_as_dictionary())

class ElectricAppliancesTests(TestCase):

    def test_electric_appliances(self):
        electric = ElectricAppliances(10, "thing", 24, 1000, "Mine", 60)

        out_dict = {"product_code": 10, "description": "thing",
        "market_price": 24, "rental_price": 1000, "brand": "Mine", "voltage": 60}

        self.assertEqual(out_dict, electric.return_as_dictionary())

class MarketPriceTests(TestCase):

    def test_market_price(self):
        result = get_latest_price("")

        self.assertEqual(24, result)

class MainTests(TestCase):

    # Really not seeing how to use Mock to generate input value
    # The examples seem to be asserting that a function was called
    # with certain arguments, but that's not applicable here.


    # def test_get_price(self):
    #     result = get_price("")

    #     self.assertEqual(24, result)



