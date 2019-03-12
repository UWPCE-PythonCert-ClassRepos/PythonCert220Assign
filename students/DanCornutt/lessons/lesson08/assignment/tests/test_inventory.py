#!/usr/bin/env python3

"""Testing code for inventory.py from HW8"""

import pytest
import os.path
from inventory import add_furniture, single_customer


def test_add_furniture():
    """Tests file is created in local directory from add_furniture().
    Test removes file after check"""
    add_furniture("invoice01.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    assert os.path.isfile("invoice01.csv")
    os.remove("invoice01.csv")


def test_single_customer():
    """Tests single customer function returns function."""
    test_func = single_customer("Susan Wong", "SW_invoice.csv")
    assert type(test_func) == "function"
