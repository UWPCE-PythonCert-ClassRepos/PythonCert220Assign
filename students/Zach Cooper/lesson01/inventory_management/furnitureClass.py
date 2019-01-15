"""Furniture class"""
from inventoryClass import Inventory


class Furniture(Inventory):

    def __init__(self, productCode, description, rentalPrice,
                 marketPrice, material, size):
        Inventory.__init__(self, productCode, description,
                           rentalPrice, marketPrice)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def returnAsDictionary(self):
        outputDict = super(Furniture, self).returnAsDictionary()
        # outputDict = {}
        # outputDict['productCode'] = self.productCode
        # outputDict['description'] = self.description
        # outputDict['rentalPrice'] = self.rentalPrice
        # outputDict['marketPrice'] = self.marketPrice
        outputDict['material'] = self.material
        outputDict['size'] = self.size

        return outputDict
