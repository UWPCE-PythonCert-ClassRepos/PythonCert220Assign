"""Electric Appliances Class"""
from inventoryClass import Inventory


class ElectricAppliances(Inventory):

    def __init__(self, productCode, description, rentalPrice,
                 marketPrice, brand, voltage):

        Inventory.__init__(self, productCode, description,
                           rentalPrice, marketPrice)
    # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def returnAsDictionary(self):
        outputDict = super(ElectricAppliances, self).returnAsDictionary()
        # outputDict = {}
        # outputDict['productCode'] = self.productCode
        # outputDict['description'] = self.description
        # outputDict['rentalPrice'] = self.rentalPrice
        # outputDict['marketPrice'] = self.marketPrice
        outputDict['brand'] = self.brand
        outputDict['voltage'] = self.voltage

        return outputDict
