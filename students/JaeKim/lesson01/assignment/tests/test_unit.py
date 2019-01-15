from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from inventory.furniture import Furniture
from inventory.inventory import Inventory
from inventory.electric_appliance import ElectricAppliance
from inventory.market_prices import get_latest_price
from main import main_menu, get_price, exit_program, item_info, add_new_item


class FurnitureTest(TestCase):
    def test_furniture(self):
        fur = Furniture("1", "one", "2.99", "rentalprice", "leather", "S")
        self.assertEqual("leather", fur.return_as_dictionary()["material"])


class InventoryTests(TestCase):
    def test_inventory(self):
        inv = Inventory("1", "one", "2.99", "rentalprice")
        self.assertEqual("1", inv.return_as_dictionary()["product_code"])


class ElectricAppliances(TestCase):
    def test_electricAppliances(self):
        electric_app = ElectricAppliance("1", "description", "599.99", "99.99", "LG", "240")
        self.assertEqual("description", electric_app.return_as_dictionary()["description"])


class MarketPrices(TestCase):
    def test_market_prices(self):
        market_price = get_latest_price(1)
        self.assertEqual(24, market_price)


class MainTests(TestCase):
    def test_get_price(self):
        price = get_price(1)
        self.assertEqual(1, price)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            exit_program()

    # @patch('inventory.main.iteminfo', return_value='1')
    # def test_what_happens_when_answering_yes(self, mock):
    #     """
    #     Test what happens when user input is 'y'
    #     """
    #     print(iteminfo())

    def test_item_info(self):
        user_input = [1, 2]

        with patch('builtins.input', side_effect=user_input):
            item = item_info()
            self.assertNotEqual(item, "Item not found in inventory")

    def test_main_menu(self):
        user_input = ["q"]
        with patch('builtins.input', side_effect=user_input):
            menu = main_menu()
            with self.assertRaises(SystemExit):
                exit_program()

    def test_add_new_item(self):
        user_input = ["1",
                      "Eames Chair",
                      "99.99",
                      "Y",
                      "Plastic",
                      "S"]
        with patch('builtins.input', side_effect=user_input):
            item = add_new_item()
            print(item)
            self.assertEquals(item, "New inventory item added")