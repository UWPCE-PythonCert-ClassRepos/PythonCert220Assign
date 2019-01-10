from unittest.mock import patch
from unittest import TestCase

from main import mainMenu, addNewItem, itemInfo, exitProgram
from main import getPrice, itemInfo
import main

class test_main(TestCase):

    @patch('main.get_input', return_value='1')
    def test_main_addNewItem(self, mock_mainMenu):
        self.assertEqual(mainMenu(), addNewItem)

    @patch('main.get_input', return_value='2')
    def test_main_itemInfo(self, mock_mainMenu):
        self.assertEqual(mainMenu(), itemInfo)

    @patch('main.get_input', return_value='q')
    def test_main_exitProgram(self, mock_mainMenu):
        self.assertEqual(mainMenu(), exitProgram)

class test_getPrice(TestCase):

    def test_getPrice(self):
        output = getPrice(1)
        self.assertEqual(output, 'Get price')

class test_addNewItem(TestCase):

    @patch('main.get_input')
    def test_addNewItem_furniture(self, mock_get_input):
        mock_get_input.side_effect = [101, 'item 101 desc', 100, 'y', 'item 101 matl', 'S', ""]
        addNewItem()
        self.assertTrue(101 in main.fullInventory)
        self.assertFalse(102 in main.fullInventory)
        self.assertTrue(main.fullInventory[101]['description'] == 'item 101 desc')

    @patch('main.get_input')
    def test_addNewItem_Electrical(self, mock_get_input):
        mock_get_input.side_effect = [105, 'item 105 desc', 100, 'n', 'y', 'item 101 brand', 120, ""]
        addNewItem()
        self.assertTrue(105 in main.fullInventory)
        self.assertFalse(102 in main.fullInventory)
        self.assertTrue(main.fullInventory[105]['description'] == 'item 105 desc')

    @patch('main.get_input')
    def test_addNewItem_NA(self, mock_get_input):
        mock_get_input.side_effect = [110, 'item 110 desc', 100, 'n', 'n']
        addNewItem()
        self.assertTrue(110 in main.fullInventory)
        self.assertFalse(102 in main.fullInventory)
        self.assertTrue(main.fullInventory[110]['description'] == 'item 110 desc')

class test_itemInfo(TestCase):

    @patch('main.get_input', return_value='100')
    def test_itemInfo_not_in_inventory(self, mock_itemInfo):
        self.assertEqual(itemInfo(), "Item not found in inventory")


    @patch('main.get_input')
    def test_itemInfo(self, mock_get_input):
        mock_get_input.side_effect = [101, 'item 101 desc', 100, 'y', 'item 101 matl', 'S', ""]
        addNewItem()
        mock_get_input.side_effect = [101]
        item_output = itemInfo()
        self.assertTrue(item_output.startswith('productCode:101'))
        self.assertIn('item 101 desc', item_output)
