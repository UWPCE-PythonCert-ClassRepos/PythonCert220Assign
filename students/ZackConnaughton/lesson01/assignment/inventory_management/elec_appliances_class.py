# Electric appliances class
from inventory_class import Inventory

class ElecAppliances(Inventory):

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class


        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        outputDict = {}
        outputDict['product_code'] = self.product_code
        outputDict['description'] = self.description
        outputDict['market_price'] = self.market_price
        outputDict['rental_price'] = self.rental_price
        outputDict['brand'] = self.brand
        outputDict['voltage'] = self.voltage

        return outputDict
