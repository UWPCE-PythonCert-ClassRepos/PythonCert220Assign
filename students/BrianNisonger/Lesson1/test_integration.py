from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
import sys
import io

from inventory_management.market_prices import get_latest_price
from inventory_management.InventoryClass import Inventory
from inventory_management.ElectricAppliancesClass import ElectricAppliances
from inventory_management.FurnitureClass import Furniture
from inventory_management.Main import main_menu
from inventory_management.Main import generate_menu
from inventory_management.Main import get_price
from inventory_management.Main import add_new_item
from inventory_management.Main import input_item_info
from inventory_management.Main import return_item_info
from inventory_management.Main import exit_program
from inventory_management.Main import item_info

class Test_Main(TestCase):
    
    def add_new_item_furniture(self,f_inventory):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        user_input = ["1", "a", "1.0", "y", "a", "S"]
        with patch('builtins.input', side_effect=user_input):
            f_inventory = add_new_item(f_inventory)
        sys.stdout = sys.__stdout__
        return f_inventory
        
    def item_info(self,f_inventory):
        f_inventory={}
        text_trap = io.StringIO()
        sys.stdout = text_trap
        user_input=["1"]
        with patch('builtins.input', side_effect=user_input):
            f_inventory=item_info(f_inventory)
        return f_inventory 
        
    def test_main_menu(self):
        f_inventory={}
        user_input = ["1"]
        text_trap = io.StringIO()
        sys.stdout = text_trap
        with patch('builtins.input', side_effect=user_input):
            function = main_menu()
        if function.__name__=="add_new_item":
            f_inventory=self.add_new_item_furniture(f_inventory)
        user_input = ["2"]
        with patch('builtins.input', side_effect=user_input):
            function = main_menu()
        if function.__name__=="item_info":
            f_inventory=item_info(f_inventory)
        user_input = ["q"]
        with patch('builtins.input', side_effect=user_input):
            function = main_menu()
        if function.__name__=="exit_program":
            self.assertRaises(SystemExit, exit_program, f_inventory)
            
