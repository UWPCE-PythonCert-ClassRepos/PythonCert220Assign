'''
Integration tests for inventory_management
'''


from unittest import TestCase
from unittest.mock import MagicMock

import main
from inventory_management.furniture import Furniture
import inventory_management.management as management

class IntegrationTests(TestCase):
    def test_add_new_furniture_item(self):
        properties = {
            "product_code": "25",
            "description": "Dishwasher",
            "market_price": 200.00,
            "rental_price": 12.00,
            "material": "Cherry",
            "size": 13.2,
            "is_furniture": "y"
        }
        item_count = len(management.FULL_INVENTORY)
        main.add_new_item(properties)
        self.assertEqual(item_count + 1, len(management.FULL_INVENTORY), "New furniture item not added")
        result = management.get_item(properties["product_code"])
        self.assertIsNotNone(result, "New furniture item now found")