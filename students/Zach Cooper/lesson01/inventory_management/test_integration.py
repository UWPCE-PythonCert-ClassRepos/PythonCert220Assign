from unittest import TestCase
from unittest.mock import MagicMock

from main.inventoryClass import Inventory
from main.electricAppliances import ElectricAppliances
from main.furntireClass import Furniture
from main.market_prices import get_latest_price


class ModuleTests(TestCase):

    def test_module(self):

        main = main(Inventory(), Furniture(), ElectricAppliances(),
                    get_latest_price())

        main.itemCode('c555')
        main.itemDescription('an item')
        main.rentalPrice(100)
        main.itemPrice(24)

        main.Furniture(main.itemCode, main.itemDescription,
                       main.itemPrice, main.itemRentalPrice)

        main.itemMaterial('Leather')
        main.itemSize('M')

        main.Furniture(main.itemCode, main.itemDescription,
                       main.itemPrice, main.itemRentalPrice,
                       main.itemMaterial, main.itemSize)

        main.itemBrand('Kenmore')
        main.itemVoltage(150)

        main.ElectricAppliances(main.itemCode, main.itemDescription,
                                main.itemPrice, main.itemRentalPrice,
                                main.itemBrand, main.itemVoltage


        """LOTS OF LINTER ERRORS but this is temporary code as I am
        still unsure on this"""
        furniture_result=main.Furniture(
            main.itemCode, main.itemDescription,
            main.itemPrice, main.itemRentalPrice,
            main.itemMaterial, main.itemSize)

        self.assertEqual({'productCode': 'c555', 'description': 'an item',
                          'marketPrice': ('c555', 24), 'rentalPrice': '100',
                          'material': 'Leather', 'size': 'M'},
                          furniture_result)

        electricAppliances_result=main.ElectricAppliances(main.itemCode,
                                                          main.itemDescription,
                                                          main.itemPrice,
                                                          main.itemRentalPrice,
                                                          main.itemBrand,
                                                          main.itemVoltage)

        self.assertEqual({'productCode': 'c55', 'description': 'Couch',
                          'marketPrice': ('c55', 24), 'rentalPrice': '100',
                          'brand': 'Kenmore', 'voltage': '150'},
                          electricAppliances_result)

