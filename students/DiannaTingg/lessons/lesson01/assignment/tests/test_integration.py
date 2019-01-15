"""
Integration Tests
"""

from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliances import ElectricAppliances
from inventory_management.market_prices import get_latest_price

