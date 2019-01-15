'''
Contains tests for the inventory management package
'''

import sys
from unittest import TestCase
from unittest.mock import MagicMock
from unittest import mock
from contextlib import contextmanager
from io import StringIO

from inventory_management import inventory
from inventory_management.electric_appliances import ElectricAppliance
from inventory_management.furniture import Furniture
import inventory_management.market_prices as market_prices
import main
import inventory_management.management as management

@contextmanager
def mockRawInput(mock):
    original_raw_input = __builtins__.raw_input
    __builtins__.raw_input = lambda _: mock
    yield
    __builtins__.raw_input = original_raw_input

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class MarketPricesTests(TestCase):

    def test_get_latest_price(self):
        self.assertEqual(market_prices.get_latest_price("test"), 24)

class ElectronicAppliancesTests(TestCase):

    def setUp(self):
        self.data = {}
        self.data["product_code"] = "25"
        self.data["description"] = "Dishwasher"
        self.data["market_price"] = 200.00
        self.data["rental_price"] = 12.00
        self.data["brand"] = "GE"
        self.data["voltage"] = 28

    def test_electronic_appliance_create(self):
        item = ElectricAppliance(
            self.data["product_code"], self.data["description"], self.data["market_price"],
            self.data["rental_price"], self.data["brand"], self.data["voltage"])

        self.assertEqual(self.data["product_code"], item.product_code)
        self.assertEqual(self.data["description"], item.description)
        self.assertEqual(self.data["market_price"], item.market_price)
        self.assertEqual(self.data["rental_price"], item.rental_price)
        self.assertEqual(self.data["brand"], item.brand)
        self.assertEqual(self.data["voltage"], item.voltage)

    def test_electronic_appliance_return_as_dict(self):
        item = ElectricAppliance(**self.data)
        result = item.return_as_dictionary()
        self.assertEqual(len(self.data), len(result))

        for name, value in self.data.items():
            self.assertEqual(value, result[name])

class FurnitureTests(TestCase):

    def setUp(self):
        self.data = {}
        self.data["product_code"] = "25"
        self.data["description"] = "Dishwasher"
        self.data["market_price"] = 200.00
        self.data["rental_price"] = 12.00
        self.data["material"] = "Cherry"
        self.data["size"] = 13.2

    def test_furniture_create(self):
        item = Furniture(
            self.data["product_code"], self.data["description"], self.data["market_price"],
            self.data["rental_price"], self.data["material"], self.data["size"])

        self.assertEqual(self.data["product_code"], item.product_code)
        self.assertEqual(self.data["description"], item.description)
        self.assertEqual(self.data["market_price"], item.market_price)
        self.assertEqual(self.data["rental_price"], item.rental_price)
        self.assertEqual(self.data["material"], item.material)
        self.assertEqual(self.data["size"], item.size)

    def test_furniture_return_as_dict(self):
        item = Furniture(**self.data)
        result = item.return_as_dictionary()
        self.assertEqual(len(self.data), len(result))

        for name, value in self.data.items():
            self.assertEqual(value, result[name])

class InventoryTests(TestCase):

    def setUp(self):
        self.data = {}
        self.data["product_code"] = "25"
        self.data["description"] = "Dishwasher"
        self.data["market_price"] = 200.00
        self.data["rental_price"] = 12.00

    def test_inventory_create(self):
        item = inventory.Inventory(
            self.data["product_code"], self.data["description"], self.data["market_price"],
            self.data["rental_price"])

        self.assertEqual(self.data["product_code"], item.product_code)
        self.assertEqual(self.data["description"], item.description)
        self.assertEqual(self.data["market_price"], item.market_price)
        self.assertEqual(self.data["rental_price"], item.rental_price)

    def test_inventory_return_as_dict(self):
        item = inventory.Inventory(**self.data)
        result = item.return_as_dictionary()
        self.assertEqual(len(self.data), len(result))
        
        for name, value in self.data.items():
            self.assertEqual(value, result[name])

class ManagementTests(TestCase):

    def setUp(self):
        self.properties = {
            'product_code': '10',
            "description": "test desc",
            "rental_price": 10,
            "material": "cherry",
            "size": "L",
            "brand": "Samsung",
            "voltage": "2.4" }
        # self.market_prices = market_prices

    @mock.patch('inventory_management.market_prices')
    @mock.patch('inventory_management.management.inventory')
    def test_add_inventory(self, mock_inventory, mock_market_prices):
        mock_price = 10
        mock_market_prices.get_latest_price = MagicMock(return_value=mock_price)

        management.add_inventory(self.properties, mock_market_prices)

        mock_market_prices.get_latest_price.assert_called_with(self.properties["product_code"])
        mock_inventory.Inventory.assert_called_with(
            self.properties["product_code"], self.properties["description"],
            mock_price, self.properties["rental_price"])
        self.assertIn(self.properties["product_code"], management.FULL_INVENTORY)

    @mock.patch('inventory_management.market_prices')
    @mock.patch('inventory_management.management.furniture')
    def test_add_furniture(self, mock_furniture, mock_market_prices):
        mock_price = 10
        mock_market_prices.get_latest_price = MagicMock(return_value=mock_price)

        management.add_furniture(self.properties, mock_market_prices)

        mock_market_prices.get_latest_price.assert_called_with(self.properties["product_code"])
        mock_furniture.Furniture.assert_called_with(
            self.properties["product_code"], self.properties["description"],
            mock_price, self.properties["rental_price"],
            self.properties["material"], self.properties["size"])
        self.assertIn(self.properties["product_code"], management.FULL_INVENTORY)

    @mock.patch('inventory_management.market_prices')
    @mock.patch('inventory_management.management.electric_appliances')
    def test_add_electric_appliance(self, mock_electric_appliances, mock_market_prices):
        mock_price = 10
        mock_market_prices.get_latest_price = MagicMock(return_value=mock_price)

        management.add_electric_appliance(self.properties, mock_market_prices)

        mock_market_prices.get_latest_price.assert_called_with(self.properties["product_code"])
        mock_electric_appliances.ElectricAppliance.assert_called_with(
            self.properties["product_code"], self.properties["description"],
            mock_price, self.properties["rental_price"],
            self.properties["brand"], self.properties["voltage"])
        self.assertIn(self.properties["product_code"], management.FULL_INVENTORY)
    
    def test_add_get_item(self):
        management.FULL_INVENTORY["test"] = "test_value"
        result = management.get_item("test")
        self.assertEqual(result, "test_value", "get_item returned incorrect item")


class MainTests(TestCase):

    def setUp(self):
        self.properties = {
            "product_code": '10',
            "description": "test desc",
            "rental_price": 10,
            "material": "cherry",
            "size": "L",
            "brand": "Samsung",
            "voltage": "2.4",
            "is_electric_appliance": "n",
            "is_furniture": "n" }

    def test_main_menu_option_1(self):
        result = main.main_menu(user_prompt="1")
        self.assertEqual(result, main.add_new_item, "Invalid main menu result for option 1")
    
    def test_main_menu_option_2(self):
        result = main.main_menu(user_prompt="2")
        self.assertEqual(result, main.item_info, "Invalid main menu result for option 2")

    def test_main_menu_option_Q(self):
        result = main.main_menu(user_prompt="q")
        self.assertEqual(result, main.exit_program, "Invalid main menu result for option q")

    def test_main_menu_user_select(self):
        with mock.patch('main.safe_input', return_value='1'):
            result = main.main_menu()
        self.assertEqual(result, main.add_new_item, "Invalid main menu result for option 1")

    @mock.patch('main.market_prices')
    @mock.patch('main.management')
    def test_add_new_item_inventory(self, mock_mangement, mock_market_prices):
        main.add_new_item(properties=self.properties)
        mock_mangement.add_inventory.assert_called_with(self.properties, mock_market_prices)

    @mock.patch('main.market_prices')
    @mock.patch('main.management')
    def test_add_new_item_furniture(self, mock_mangement, mock_market_prices):
        self.properties["is_furniture"] = "y"
        main.add_new_item(properties=self.properties)
        mock_mangement.add_furniture.assert_called_with(self.properties, mock_market_prices)

    @mock.patch('main.market_prices')
    @mock.patch('main.management')
    def test_add_new_item_electric_appliance(self, mock_mangement, mock_market_prices):
        self.properties["is_electric_appliance"] = "y"
        main.add_new_item(properties=self.properties)
        mock_mangement.add_electric_appliance.assert_called_with(self.properties, mock_market_prices)


    def test_safe_input(self):
        with mock.patch('builtins.input', return_value='test_return_value') as _raw_input:
            self.assertEqual(main.safe_input("Enter a value: "), "test_return_value")
            _raw_input.assert_called_once_with('Enter a value: ')
            

    @mock.patch('main.management')
    def test_item_info_not_found(self, mock_management):
        mock_management.get_item = MagicMock(return_value=None)
        with captured_output() as (out, err):
            main.item_info("test")
        result = out.getvalue().strip()
        self.assertEqual(result, "Item not found in inventory")

    @mock.patch('main.management')
    def test_item_info_returned_value(self, mock_management):
        mock_management.get_item = MagicMock(return_value={"test_key": "test_val"})
        with captured_output() as (out, err):
            main.item_info("test")
        result = out.getvalue().strip()
        self.assertEqual(result, "test_key:test_val")
    
    @mock.patch('main.management')
    def test_item_info_no_input(self, mock_management):
        mock_management.get_item = MagicMock(return_value={"test_key": "test_val"})
        with mock.patch('main.safe_input', return_value='my_test_value'):
            with captured_output() as (out, err):
                main.item_info()
            result = out.getvalue().strip()
        self.assertEqual(result, "test_key:test_val")
