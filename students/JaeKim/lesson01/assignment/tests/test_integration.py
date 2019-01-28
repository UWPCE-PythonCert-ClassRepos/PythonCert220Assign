from unittest import TestCase
from unittest.mock import MagicMock

from inventory.furniture import Furniture
from inventory.inventory import Inventory
from inventory.electric_appliance import ElectricAppliance
from inventory.market_prices import get_latest_price
from main import main_menu, get_price, exit_program, item_info, add_new_item


import main

class MainTests(TestCase):
    def test_integration_main(self):
        blanket = Inventory(100, "blanket", 300, 100)
        blanket_details = blanket.return_as_dictionary()

        chair = Furniture(200, "chair", 200, 50, "Plastic", "S")
        chair_details = chair.return_as_dictionary()

        monitor = ElectricAppliance(300, "IPS Monitor", 500, 50, "Asus", 220)
        monitor_details = monitor.return_as_dictionary()

        self.assertEqual(100, blanket_details["product_code"])
        self.assertEqual(200, chair_details["product_code"])
        self.assertEqual(300, monitor_details["product_code"])