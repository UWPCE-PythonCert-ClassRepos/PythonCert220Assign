""" Unittest Module  """


from unittest import TestCase
from unittest.mock import MagicMock

# from inventory_management.electricappliancesclass import ElectricAppliances as elapp
import inventory_management.electricappliancesclass as e_app_mod
import inventory_management.furnitureclass as fur_mod
import inventory_management.inventoryclass as inv_mod
# from inventory_management.market_prices import market_prices as mp

class TestInventoryclass(TestCase):
    def test_returnas_dictionary_inventory(self):
        inventory = inv_mod.Inventory(
            productcode="TV",
            description="Television set",
            marketprice="1,200",
            rentalprice="150")

        result_dict = inventory.returnas_dictionary()

        expected_dict = {
            "productcode": "TV",
            "description": "Television set",
            "marketprice": "1,200",
            "rentalprice": "150"
        }

        for key in result_dict:
            self.assertEqual((key in expected_dict), True)
            self.assertEqual(result_dict[key], expected_dict[key])

        self.assertEqual(len(expected_dict[key]), len(result_dict[key]))

class TestElectricAppliances(TestCase):
    def test_returnas_dictionary_electricappliances(self):
        electricappliances = e_app_mod.ElectricAppliances(
            productcode="EC",
            description="Electronic Charger",
            marketprice="12",
            rentalprice="10",
            brand="Sony",
            voltage="4")

        result_dict = electricappliances.returnas_dictionary()

        expected_dict = {
            "productcode": "EC",
            "description": "Electronic Charger",
            "marketprice": "12",
            "rentalprice": "10",
            "brand": "Sony",
            "voltage": "4"
        }

        for key in result_dict:
            self.assertEqual((key in expected_dict), True)
            self.assertEqual(result_dict[key], expected_dict[key]) 

        self.assertEqual(len(expected_dict[key]), len(result_dict[key]))


class TestFurniture(TestCase):
    def test_returnas_dictionary_furniture(self):
        furniture = fur_mod.Furniture(
            productcode="DT",
            description="Dinner Table",
            marketprice="21",
            rentalprice="15",
            material="Wood",
            size="24"
        )

        result_dict = furniture.returnas_dictionary()

        expected_dict = {
            "productcode": "DT",
            "description": "Dinner Table",
            "marketprice": "21",
            "rentalprice": "15",
            "material": "Wood",
            "size": "24"
        }

        for key in result_dict:
            self.assertEqual((key in expected_dict), True)
            self.assertEqual(result_dict[key], expected_dict[key])

        self.assertEqual(len(expected_dict.keys()), len(result_dict.keys()))
