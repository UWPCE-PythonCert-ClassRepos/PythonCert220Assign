"""
Unit Tests
"""

from unittest import TestCase

from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliances import ElectricAppliances
from inventory_management.market_prices import get_latest_price


class InventoryTests(TestCase):
    def test_init_inventory(self):
        chair = Inventory(1, "lawn_chair", 5, 2)
        self.assertEqual(1, chair.product_code)
        self.assertEqual("lawn_chair", chair.description)
        self.assertEqual(5, chair.market_price)
        self.assertEqual(2, chair.rental_price)

    def test_return_as_dict_inventory(self):
        chair = Inventory(1, "lawn_chair", 5, 2)
        my_dict = {"product_code": 1, "description": "lawn_chair", "market_price": 5, "rental_price": 2}
        self.assertEqual(my_dict, chair.return_as_dictionary())


class FurnitureTests(TestCase):
    def test_init_furniture(self):
        table = Furniture(2, "poker_table", 10, 4, "plastic", "small")
        self.assertEqual(2, table.product_code)
        self.assertEqual("poker_table", table.description)
        self.assertEqual(10, table.market_price)
        self.assertEqual(4, table.rental_price)
        self.assertEqual("plastic", table.material)
        self.assertEqual("small", table.size)

    def test_return_as_dict_furniture(self):
        table = Furniture(2, "poker_table", 10, 4, "plastic", "small")
        my_dict = {"product_code": 2, "description": "poker_table", "market_price": 10, "rental_price": 4,
                   "material": "plastic", "size": "small"}
        self.assertEqual(my_dict, table.return_as_dictionary())


class ElectricAppliancesTests(TestCase):
    def test_init_electric(self):
        microwave = ElectricAppliances(3, "silver_microwave", 50, 10, "Samsung", 110)
        self.assertEqual(3, microwave.product_code)
        self.assertEqual("silver_microwave", microwave.description)
        self.assertEqual(50, microwave.market_price)
        self.assertEqual(10, microwave.rental_price)
        self.assertEqual("Samsung", microwave.brand)
        self.assertEqual(110, microwave.voltage)

    def test_return_as_dict_electric(self):
        microwave = ElectricAppliances(3, "silver_microwave", 50, 10, "Samsung", 110)
        my_dict = {"product_code": 3, "description": "silver_microwave", "market_price": 50, "rental_price": 10,
                   "brand": "Samsung", "voltage": 110}
        self.assertEqual(my_dict, microwave.return_as_dictionary())


class MarketPricesTests(TestCase):
    def test_get_latest_price(self):
        self.assertEqual(24, get_latest_price(100))
