from unittest.mock import patch
from unittest import TestCase

from main import main_menu, get_price, add_new_item, item_info, exit_program
import main
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.market_prices import get_latest_price
from inventory_management.elec_appliances_class import ElecAppliances

class TestMain(TestCase):
    """
    test for the main.py file
    """
    @patch('main.get_input', return_value='1')
    def test_main_add_new_item(self, mock_main_menu):
        self.assertEqual(main_menu(), add_new_item)

    @patch('main.get_input', return_value='2')
    def test_main_item_info(self, mock_main_menu):
        self.assertEqual(main_menu(), item_info)

    @patch('main.get_input', return_value='q')
    def test_main_exit_program(self, mock_main_menu):
        self.assertEqual(main_menu(), exit_program)

    def test_get_price(self):
        output = get_price(1)
        self.assertEqual(output, 'Get price for item 1.')

    @patch('main.get_input')
    def test_add_new_item_furniture(self, mock_get_input):
        mock_get_input.side_effect = [101, 'item 101 desc', 100, 'y', 'item 101 matl', 'S', ""]
        add_new_item()
        self.assertTrue(101 in main.FULL_INVENTORY)
        self.assertFalse(102 in main.FULL_INVENTORY)
        self.assertTrue(main.FULL_INVENTORY[101]['description'] == 'item 101 desc')

    @patch('main.get_input')
    def test_add_new_item_electrical(self, mock_get_input):
        mock_get_input.side_effect = [105, 'item 105 desc', 100, 'n', 'y', 'item 101 brand', 120, ""]
        add_new_item()
        self.assertTrue(105 in main.FULL_INVENTORY)
        self.assertFalse(102 in main.FULL_INVENTORY)
        self.assertTrue(main.FULL_INVENTORY[105]['description'] == 'item 105 desc')

    @patch('main.get_input')
    def test_add_new_item_NA(self, mock_get_input):
        mock_get_input.side_effect = [110, 'item 110 desc', 100, 'n', 'n']
        add_new_item()
        self.assertTrue(110 in main.FULL_INVENTORY)
        self.assertFalse(102 in main.FULL_INVENTORY)
        self.assertTrue(main.FULL_INVENTORY[110]['description'] == 'item 110 desc')

    @patch('main.get_input', return_value='100')
    def test_item_info_not_in_inventory(self, mock_item_info):
        self.assertEqual(item_info(), "Item not found in inventory")

    @patch('main.get_input')
    def test_item_info(self, mock_get_input):
        mock_get_input.side_effect = [101, 'item 101 desc', 100, 'y', 'item 101 matl', 'S', ""]
        add_new_item()
        mock_get_input.side_effect = [101]
        item_output = item_info()
        self.assertTrue(item_output.startswith('product_code:101'))
        self.assertIn('item 101 desc', item_output)

class TestInventoryClass(TestCase):
    """
    test for inventory_class
    """
    def setUp(self):
        self.new_inventory = Inventory(100, '100 description', 100, 200)

    def test_inventory_class(self):
        # new_inventory = Inventory(100, '100 description', 100, 200)
        # self.assertTrue(new_inventory)
        self.assertEqual(self.new_inventory.product_code, 100)
        self.assertEqual(self.new_inventory.description, '100 description')
        self.assertEqual(self.new_inventory.market_price, 100)
        self.assertEqual(self.new_inventory.rental_price, 200)

    def test_inventory_class_dict(self):
        # new_inventory = Inventory(100, '100 description', 100, 200)
        new_inventory_dict = self.new_inventory.return_as_dictionary()
        self.assertEqual(new_inventory_dict['product_code'], 100)
        self.assertEqual(new_inventory_dict['description'], '100 description')
        self.assertEqual(new_inventory_dict['market_price'], 100)
        self.assertEqual(new_inventory_dict['rental_price'], 200)

class TestFurnitureClass(TestCase):

    def setUp(self):

        self.new_furniture = Furniture(Inventory(100, '100 description', 100, 200), '101 material', 'S')

    def test_furniture_class(self):
        # new_furniture = Furniture(100, '100 description', 100, 200, '101 material', 'S')
        # self.assertTrue(new_furniture)
        self.assertEqual(self.new_furniture.product_code, 100)
        self.assertEqual(self.new_furniture.description, '100 description')
        self.assertEqual(self.new_furniture.market_price, 100)
        self.assertEqual(self.new_furniture.rental_price, 200)

    def test_furniture_class_dict(self):
        # new_furniture = Furniture(100, '100 description', 100, 200, '101 material', 'S')
        new_furniture_dict = self.new_furniture.return_as_dictionary()
        self.assertEqual(new_furniture_dict['product_code'], 100)
        self.assertEqual(new_furniture_dict['description'], '100 description')
        self.assertEqual(new_furniture_dict['market_price'], 100)
        self.assertEqual(new_furniture_dict['rental_price'], 200)
        self.assertEqual(new_furniture_dict['material'], '101 material')
        self.assertEqual(new_furniture_dict['size'], 'S')

class TestMarketPrices(TestCase):

    def test_market_prices(self):
        self.assertEqual(get_latest_price("anything"), 24)


class TestElecAppliances(TestCase):

    def setUp(self):
        self.new_electrical_appliance = ElecAppliances(Inventory(100, '100 desc', 100, 200), '100 brand', 120)

    def test_elec_appliances(self):
        # new_electrical_appliance = ElecAppliances(100, '100 desc', 100, 200, '100 brand', 120)
        # self.assertTrue(new_electrical_appliance)
        self.assertEqual(self.new_electrical_appliance.product_code, 100)
        self.assertEqual(self.new_electrical_appliance.description, '100 desc')
        self.assertEqual(self.new_electrical_appliance.market_price, 100)
        self.assertEqual(self.new_electrical_appliance.rental_price, 200)
        self.assertEqual(self.new_electrical_appliance.brand, '100 brand')
        self.assertEqual(self.new_electrical_appliance.voltage, 120)

    def test_elec_appliances_dict(self):
        # new_electrical_appliance = ElecAppliances(100, '100 desc', 100, 200, '100 brand', 120)
        new_electrical_appliance_dict = self.new_electrical_appliance.return_as_dictionary()
        self.assertEqual(new_electrical_appliance_dict['product_code'], 100)
        self.assertEqual(new_electrical_appliance_dict['description'], '100 desc')
        self.assertEqual(new_electrical_appliance_dict['market_price'], 100)
        self.assertEqual(new_electrical_appliance_dict['rental_price'], 200)
        self.assertEqual(new_electrical_appliance_dict['brand'], '100 brand')
        self.assertEqual(new_electrical_appliance_dict['voltage'], 120)
