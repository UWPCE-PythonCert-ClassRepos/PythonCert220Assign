"""
Integration Tests
"""

from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliances import ElectricAppliances
from inventory_management.market_prices import get_latest_price


class ModuleTests(TestCase):

    def test_module(self):
        rug = Inventory(7, "oriental_rug", 30, 5)
        rug_info = rug.return_as_dictionary()

        sofa = Furniture(5, "brown_sofa", 100, 20, "leather", "large")
        sofa_info = sofa.return_as_dictionary()

        tv = ElectricAppliances(6, "4k_tv", 2000, 50, "Panasonic", 220)
        tv_info = tv.return_as_dictionary()

        price = get_latest_price(8)

        self.assertEqual(7, rug.product_code)
        self.assertEqual("oriental_rug", rug_info["description"])

        self.assertEqual("brown_sofa", sofa.description)
        self.assertEqual(100, sofa_info["market_price"])

        self.assertEqual(2000, tv.market_price)
        self.assertEqual(50, tv_info["rental_price"])

        self.assertEqual(24, get_latest_price(1))
