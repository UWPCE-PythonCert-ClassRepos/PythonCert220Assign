# from unittest import TestCase
# from unittest.mock import patch

from inventoryClass import Inventory
from electricAppliancesClass import ElectricAppliances
from furnitureClass import Furniture
from market_prices import get_latest_price
# import main



def test_electric_appliance():
    """
    Tests Electric Appliances Init Function
    """

    electric_stove = ElectricAppliances("C555", "electric stove", 300.00, 175.00,
                                        "Kenmore", "150 V")

    assert electric_stove.product_code == "C555"
    assert electric_stove.description == "electric stove"
    assert electric_stove.market_price == 300.00
    assert electric_stove.rental_price == 175.00
    assert electric_stove.brand == "Kenmore"
    assert electric_stove.voltage == "150 V"


def test_electric_appliance_return_as_dictionary():
    """
    Test whether ElectricAppliances Class ruturns information
    about ElectricAppliances stored in Inventory in a dict
    """
    electric_stove = ElectricAppliances("C555", "electric stove", 300.00, 175.00,
                                        "Kenmore", "150 V")

    assert electric_stove.return_as_dictionary() == {"product_code": "C555",
                                                     "description": "electric stove",
                                                     "market_price": 300.00,
                                                     "rental_price": 175.00,
                                                     "brand": "Kenmore",
                                                     "voltage": "150 V"}


def test_furniture():
    """
    Test Furniture Init Function
    """

    couch = Furniture("C777", "reclining couch", 20.00, 10.00, "leather", "M")

    assert couch.product_code == "C777"
    assert couch.description == "reclining couch"
    assert couch.market_price == 20.00
    assert couch.rental_price == 10.00
    assert couch.material == "leather"
    assert couch.size == "M"


def test_furniture_return_to_dictionary():

    couch = Furniture("C777", "reclining couch", 20.00, 10.00, "leather", "M")

    assert couch.return_as_dictionary() == {"product_code": "C777",
                                            "description": "reclining couch",
                                            "market_price": 20.00,
                                            "rental_price": 10.00,
                                            "material": "leather",
                                            "size": "M"}


def test_inventory():
    """
    Test for Inventory Init
    """

    couch = Inventory("C777", "reclining couch", 20.00, 10.00)

    assert couch.product_code == "C777"
    assert couch.description == "reclining couch"
    assert couch.market_price == 20.00
    assert couch.rental_price == 10.00


def test_inventory_return_to_dictionary():
    """
    Tests InventoryClass returning a dic of information about all
    the items in the dictionary
    """

    couch = Inventory("C777", "reclining couch", 20.00, 10.00)

    assert couch.return_as_dictionary() == {"product_code": "C777",
                                            "description": "reclining couch",
                                            "market_price": 20.00,
                                            "rental_price": 10.00
                                            }



# class FurnitureTests(TestCase):

#     def test_furniture(self):
#         item = Furniture()
#         item = furnitureClass.Furniture('c555', 'an item', 24, 90,
#                                         'leather', 'M')

#         assert item.productCode == 'c555'
#         assert item.description == 'an item'
#         assert item.marketPrice == 24
#         assert item.rentalPrice == 90
#         assert item.material == 'Leather'
#         assert item.size == 'M'
#         assert item.returnAsDictionary() == {'productCode': 'c555',
#                                              'description': 'an item',
#                                              'marketPrice': 24,
#                                              'rentalPrice': 90,
#                                              'size': 'M',
#                                              'material': 'Leather',
#                                              }


# class InvetoryTests(TesCase):

#     def test_inventory(self):
#         item = Inventory()
#         item = inventoryClass.Inventory('c555', 'an item', 24, 90)

#         assert item.productCode == 'c555'
#         assert item.desciprtion == 'an item'
#         assert item.marketPrice == 24
#         assert item.rentalPrice == 90
#         assert item.returnAsDictionary() == {'productCode': 'c555',
#                                              'description': 'an item',
#                                              'marketPrice': 24,
#                                              'rentalPrice': 90,
#                                              }


# class MainTests(TestCase):

#     """Can I do multiple input patches for the same
#     function being teste???"""
#     # Mocks input value for itemCode
#     @patch('main.itemCode', return_value='c555')
#     # Mock input itemDescription
#     @patch('main.itemDescription', return_value='an item')
#     # Mock input rentalPrice
#     @patch('main.itemRentalPrice', return_value=90)
#     def test_add_new_item_input(self, mock_mainMenu):
#         self.assertEqual(itemCode, return_value)
#         self.assertEqual(itemDescription, return_value)
#         self.assertEqual(itemRentalPrice, return_value)

    # # Mock input item description
    # @patch('main.itemDescription', return_value='an item')
    # def test_add_new_item_input(self, mock_addNewItemInput):
    #     self.assertEqual(itemDescription, return_value)



