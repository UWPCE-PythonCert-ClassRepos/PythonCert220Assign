from unittest import TestCase
from unittest.mock import patch

from main import main_menu, get_price, add_new_item, item_info, exit_program
import main


# See test_unit for class tests
# from inventoryClass import Inventory
# from electricAppliancesClass import ElectricAppliances
# from furnitureClass import Furniture
# from market_prices import get_latest_price


class TestMain(TestCase):

    """
    Tests the main.py file
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


# Test add_new_item function 
class test_add_new_item(TestCase):

    # Mock Furniture input scenario
    @patch('main.get_input')
    def test_add_new_item_furniture(self, mock_get_input):
        mock_get_input.side_effect = ["C777", "reclining couch", 20.00, "y",
                                      "leather", "M", ""]
        add_new_item()
        self.assertTrue(20.00 in main.FULL_INVENTORY)
        self.assertFalse(30.00 in main.FULL_INVENTORY)
        self.assertTrue(main.FULL_INVENTORY["C777"]['description'] == 'reclining couch')

    # Mock Electrical input scenario
    @patch('main.get_input')
    def test_add_new_item_electric_appliances(self, mock_get_input):
        mock_get_input.side_effect = ["C555", "electric stove", 300.00, "n",
                                      "y", "Kenmore", "150 V", ""]
        add_new_item()
        self.assertTrue(20.00 in main.FULL_INVENTORY)
        self.assertFalse(30.00 in main.FULL_INVENTORY)
        self.assertTrue(main.FULL_INVENTORY["C555"]['description'] == 'electric stove')

    # Mock an input situation where input furn = no and elec = no
    @patch('main.get_input')
    def test_add_new_item_electric_appliances_not_available(self, mock_get_input):
        mock_get_input.side_effect = ["C555", "electric stove", 300.00, "n", "n"]
        add_new_item()
        self.assertTrue(20.00 in main.FULL_INVENTORY)
        self.assertFalse(30.00 in main.FULL_INVENTORY)
        self.assertTrue(main.FULL_INVENTORY["C555"]['description'] == 'electric stove')


# Test Item Info function

# Test item_info for an item that is not in dict
class test_item_info(TestCase):
    """
    Returns false if item is not in dict
    """

    @patch('main.get_input', return_value=1000)
    def test_intem_info_not_in_dict(self, mock_item_info):
        self.assertEqual(item_info(), "Item not found in inventory")

    @patch('main.get_input')
    def test_item_info(self, mock_get_input):
        mock_get_input.side_effect = ["C555", "electric stove", 300.00, "n",
                                      "y", "Kenmore", "150 V", ""]
        add_new_item()
        mock_get_input.side_effect = ["C555"]
        item_output = item_info()
        self.assertTrue(item_output.startswith('product_code: C555'))
        self.assertIn('electric stove', item_output)


# # Tests get_price function
# class test_get_price(TestCase):

#     def test_get_price(self):
#         output = get_price(1)
#         # Returns value of 24
#         self.assertEqual(output, 'Get price for item 1.')
