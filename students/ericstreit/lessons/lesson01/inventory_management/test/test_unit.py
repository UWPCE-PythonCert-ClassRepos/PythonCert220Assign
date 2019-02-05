import unittest
from unittest import TestCase
from unittest.mock import MagicMock

# from inventory_management.electricAppliancesClass import electricAppliances
# from inventory_management.furnitureClass import furniture
# from inventory_management.inventoryClass import inventory
import inventory_management
from inventory_management import electricAppliancesClass
from inventory_management import furnitureClass
from inventory_management import inventoryClass
from inventory_management import market_prices
import main


class ApplianceTests(TestCase):

    def test_appliance(self):
        thing = electricAppliancesClass.electricAppliances(55, 'a thing', 24, 99, 'Whirlpool', 120)
        assert thing.productCode == 55
        assert thing.description == 'a thing'
        assert thing.marketPrice == 24
        assert thing.rentalPrice == 99
        assert thing.brand == 'Whirlpool'
        assert thing.voltage == 120
        assert thing.returnAsDictionary() == {'productCode': 55,
                                            'description': 'a thing',
                                            'marketPrice': 24,
                                            'rentalPrice': 99,
                                            'brand': 'Whirlpool',
                                            'voltage': 120}


class FurnitureTests(TestCase):

    def test_furniture(self):
        thing = furnitureClass.furniture(55, 'a thing', 24, 99, 'wood', 4)
        assert thing.productCode == 55
        assert thing.description == 'a thing'
        assert thing.marketPrice == 24
        assert thing.rentalPrice == 99
        assert thing.material == 'wood'
        assert thing.size == 4
        assert thing.returnAsDictionary() == {'productCode': 55,
                                            'description': 'a thing',
                                            'marketPrice': 24,
                                            'rentalPrice': 99,
                                            'material': 'wood',
                                            'size': 4}




class InventoryTests(TestCase):

    def test_inventory(self):
        thing = inventoryClass.inventory(55, 'a thing', 24, 99)
        assert thing.productCode == 55
        assert thing.description == 'a thing'
        assert thing.marketPrice == 24
        assert thing.rentalPrice == 99
        assert thing.returnAsDictionary() == {'productCode': 55,
                                            'description': 'a thing',
                                            'marketPrice': 24,
                                            'rentalPrice': 99}



class MarketPriceTests(TestCase):

    def test_marketprice(self):
        assert market_prices.get_latest_price('mock') == 24

class MainTest(TestCase):
    assert market_prices.get_latest_price('itemCode') == 24
