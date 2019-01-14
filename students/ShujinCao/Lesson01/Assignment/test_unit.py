"""
this is for testing classes in the inventory management system
"""

from unittest.mock import patch
from unittest import TestCase

import numpy as mp
import pytest

from inventory_management import main
from inventory_management.market_prices import get_latest_price


class TestMarketprices(TestCase):

    def test_get_latest_price(self):
        assert get_latest_price() == 10


