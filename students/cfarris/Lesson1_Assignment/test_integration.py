#!/usr/bin/env Python 3

"""test integration of Inventory management testing"""

from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management import market_prices
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory


#class mainTests(TestCase)