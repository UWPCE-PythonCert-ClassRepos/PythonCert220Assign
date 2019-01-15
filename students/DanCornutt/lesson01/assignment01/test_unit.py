"""Test module for inventory mangement dir.
    All classes have unit tests for test driven dev."""

from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
# from inventory_management.main import run_main
# from inventory_management.market_prices import get_latest_price


class TestElectricAppliancesClass(TestCase):
    """Test case for inventory management Electritc Appliance Class"""

    def test_init_elec_app(self):
        """Tests instance creation of electric appliance"""
        elec_app = ElectricAppliances(1, "Blender", 50, 5)


class TestFurniture(TestCase):
    """Test case for inventory management Furniture Class"""

    def test_init_furniture(self):
        """Tests instance creation of Furniture"""
        furniture = Furniture(2, "Chair", 25, 2, "Blentec", 120)


class TestInventory(TestCase):
    """Test case for inventory management Inventory Class"""

    def test_init_inventory(self):
        """Tests instance creation of Inventory"""
        inventory = Inventory(3, "Rope", 50, 1)
