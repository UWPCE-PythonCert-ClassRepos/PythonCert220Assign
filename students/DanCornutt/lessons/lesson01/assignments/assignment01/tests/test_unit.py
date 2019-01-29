
"""Test module for inventory mangement dir.
    All classes have unit tests for test driven dev."""

from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price
from main import main_menu, get_price, add_new_item, item_info, exit_program


class TestMain(TestCase):
    """Test class for main script of inventory management script"""

    def test_main_menu(self):
        """Test main menu function"""
        pass

    def test_get_price(self):
        """Test get price function"""
        pass

    def test_add_new_item(self):
        """Test adding of new item function"""
        pass

    def test_item_info(self):
        """Test looking up item information function"""
        pass

    def test_exit_program(self):
        """Test exiting script function"""
        pass


class TestElectricAppliancesClass(TestCase):
    """Test case for inventory management Electritc Appliance Class"""

    def test_init_elec_app(self):
        """Tests instance creation of electric appliance"""
        elec_app = ElectricAppliances(
            "1", "Blender", "50", "5", "Blentec", "240")
        self.assertTrue(elec_app)
        self.assertEqual(elec_app.product_code, "1")
        self.assertEqual(elec_app.description, "Blender")
        self.assertEqual(elec_app.market_price, "50")
        self.assertEqual(elec_app.rental_price, "5")
        self.assertEqual(elec_app.brand, "Blentec")
        self.assertEqual(elec_app.voltage, "240")


class TestFurniture(TestCase):
    """Test case for inventory management Furniture Class"""

    def test_init_furniture(self):
        """Tests instance creation of Furniture"""
        furniture = Furniture("2", "Chair", "25", "2", "Wood", "L")
        self.assertTrue(furniture)
        self.assertEqual(furniture.product_code, "2")
        self.assertEqual(furniture.description, "Chair")
        self.assertEqual(furniture.market_price, "25")
        self.assertEqual(furniture.rental_price, "2")
        self.assertEqual(furniture.material, "Wood")
        self.assertEqual(furniture.size, "L")


class TestInventory(TestCase):
    """Test case for inventory management Inventory Class"""

    def test_init_inventory(self):
        """Tests instance creation of Inventory"""
        inventory = Inventory("3", "Rope", "50", "1")
        self.assertTrue(inventory)
        self.assertEqual(inventory.product_code, "3")
        self.assertEqual(inventory.description, "Rope")
        self.assertEqual(inventory.market_price, "50")
        self.assertEqual(inventory.rental_price, "1")
