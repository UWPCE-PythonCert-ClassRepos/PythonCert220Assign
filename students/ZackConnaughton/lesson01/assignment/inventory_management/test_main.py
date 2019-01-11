from unittest.mock import patch
from unittest import TestCase

from main import main_menu, get_price, add_new_item, item_info, exit_program
import main

class test_main(TestCase):

    @patch('main.get_input', return_value='1')
    def test_main_add_new_item(self, mock_main_menu):
        self.assertEqual(main_menu(), add_new_item)

    @patch('main.get_input', return_value='2')
    def test_main_item_info(self, mock_main_menu):
        self.assertEqual(main_menu(), item_info)

    @patch('main.get_input', return_value='q')
    def test_main_exit_program(self, mock_main_menu):
        self.assertEqual(main_menu(), exit_program)

class test_get_price(TestCase):

    def test_get_price(self):
        output = get_price(1)
        self.assertEqual(output, 'Get price for item 1.')

class test_add_new_item(TestCase):

    @patch('main.get_input')
    def test_add_new_item_furniture(self, mock_get_input):
        mock_get_input.side_effect = [101, 'item 101 desc', 100, 'y', 'item 101 matl', 'S', ""]
        add_new_item()
        self.assertTrue(101 in main.FULL_INVENTORY)
        self.assertFalse(102 in main.FULL_INVENTORY)
        self.assertTrue(main.FULL_INVENTORY[101]['description'] == 'item 101 desc')

    @patch('main.get_input')
    def test_add_new_item_Electrical(self, mock_get_input):
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

class test_item_info(TestCase):

    @patch('main.get_input', return_value='100')
    def test_item_info_not_in_inventory(self, mock_item_info):
        self.assertEqual(item_info(), "Item not found in inventory")


    @patch('main.get_input')
    def test_item_info(self, mock_get_input):
        mock_get_input.side_effect = [101, 'item 101 desc', 100, 'y', 'item 101 matl', 'S', ""]
        add_new_item()
        mock_get_input.side_effect = [101]
        item_output = item_info()
        self.assertTrue(item_output.startswith('productCode:101'))
        self.assertIn('item 101 desc', item_output)
