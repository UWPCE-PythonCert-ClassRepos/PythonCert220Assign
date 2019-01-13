from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from inventory.furnitureClass import furniture
from inventory.inventoryClass import inventory
from inventory.electricAppliancesClass import electricAppliances
from inventory.market_prices import get_latest_price
from inventory.main import mainmenu, getprice, exitprogram, iteminfo, addnewitem


class FurnitureTest(TestCase):
    def test_furniture(self):
        fur = furniture("1", "one", "2.99", "rentalprice", "leather", "S")
        self.assertEqual("leather", fur.returnAsDictionary()["material"])


class InventoryTests(TestCase):
    def test_inventory(self):
        inv = inventory("1", "one", "2.99", "rentalprice")
        self.assertEqual("1", inv.returnAsDictionary()["productCode"])


class ElectricAppliances(TestCase):
    def test_electricAppliances(self):
        electric_app = electricAppliances("1", "description", "10.99", "9.99", "LG", "240")
        self.assertEqual("description", electric_app.returnAsDictionary()["description"])


class MarketPrices(TestCase):
    def test_marketprices(self):
        market_price = get_latest_price(1)
        self.assertEqual(24, market_price)


class MainTests(TestCase):
    def test_getprice(self):
        price = getprice(1)
        self.assertEqual(1, price)

    def test_exitprogram(self):
        with self.assertRaises(SystemExit):
            exitprogram()

    # @patch('inventory.main.iteminfo', return_value='1')
    # def test_what_happens_when_answering_yes(self, mock):
    #     """
    #     Test what happens when user input is 'y'
    #     """
    #     print(iteminfo())

    def test_iteminfo(self):
        user_input = [1, 2]

        with patch('builtins.input', side_effect=user_input):
            item = iteminfo()
            self.assertNotEqual(item, "Item not found in inventory")

    def test_mainmenu(self):
        user_input = ["q"]
        with patch('builtins.input', side_effect=user_input):
            menu = mainmenu()
            with self.assertRaises(SystemExit):
                exitprogram()

    def test_addnewitem(self):
        user_input = ["1",
                      "Eames Chair",
                      "99.99",
                      "Y",
                      "Plastic",
                      "S"]
        with patch('builtins.input', side_effect=user_input):
            item = addnewitem()
            print(item)
            self.assertEquals(item, "New inventory item added")