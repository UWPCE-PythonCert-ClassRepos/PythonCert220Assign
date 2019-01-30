"""
Integration tests for inventory management
"""

from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized
import sys
from io import StringIO
from contextlib import redirect_stdout
import main
from main import main_menu


class IntegrationTests(TestCase):
    """
    Test that we can put stuff in inventory and then get it back out
    """

    def test_add_and_get_new_item_furniture(self):
        """
        Add furniture and get it back
        """
        text_trap = StringIO()
        item_added = "funky chair"
        user_input = ["1", "abc", item_added, "500", "Y", "leather", "S", "", '2', 'abc']
        with patch('main.input', side_effect=user_input):
            with redirect_stdout(text_trap):
                for i in range(2):
                    main_menu()()
        result = text_trap.getvalue()
        self.assertIn("New inventory item added", result)
        self.assertIn(item_added, result)
        self.assertNotIn("Item not found in inventory", result)


    @parameterized.expand([
        (["1", "def", "washer", "400", "N", "Y", "FastFurious", "50", "", '2', 'def'], 'FastFurious'),
        (["1", "ghi", "rug", "400", "N", "N", "", '2', 'ghi'], 'rug'),
        ])
    def test_add_and_get_new_item_appliance(self, user_input, item):
        """
        Add appliance and get it back
        """
        text_trap = StringIO()
        with patch('main.input', side_effect=user_input):
            with redirect_stdout(text_trap):
                for i in range(2):
                    main_menu()()
        result = text_trap.getvalue()
        self.assertIn("New inventory item added", result)
        self.assertIn(item, result)
        self.assertNotIn("Item not found in inventory", result)


    def test_not_added_not_found(self):
        text_trap = StringIO()
        item_test = 'red chair'
        user_input = ["1", "abc", "funky chair", "500", "Y", "leather", "S", "", '2', item_test]
        with patch('main.input', side_effect=user_input):
            with redirect_stdout(text_trap):
                for i in range(2):
                    main_menu()()
        result = text_trap.getvalue()
        self.assertIn("New inventory item added", result)
        self.assertNotIn(item_test, result)
        self.assertIn("Item not found in inventory", result)
