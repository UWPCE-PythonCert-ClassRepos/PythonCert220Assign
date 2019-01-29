"""
Integration tests for inventory management
"""

from unittest import TestCase
from unittest.mock import patch
import sys
from io import StringIO
from contextlib import redirect_stdout
import main
from main import main_menu


class IntegrationTests(TestCase):

    def test_add_and_get_new_item_furniture(self):
        text_trap = StringIO()
        user_input = ["1", "abc", "funky chair", "500", "Y", "leather", "S", "", '2', 'abc']
        with patch('main.input', side_effect=user_input):
            with redirect_stdout(text_trap):
                for i in range(2):
                    main_menu()()
        result = text_trap.getvalue()
        self.assertIn("New inventory item added", result)
        self.assertIn("funky chair", result)
        self.assertNotIn("Item not found in inventory", result)
