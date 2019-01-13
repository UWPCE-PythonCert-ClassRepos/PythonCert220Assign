""" This is an inventory module """


class Inventory:
    'This is a Parent class'

    def __init__(self, productcode, description, marketprice, rentalprice):
        'This is initializer method for class Inventory'
        self.productcode = productcode
        self.description = description
        self.marketprice = marketprice
        self.rentalprice = rentalprice

    def returnas_dictionary(self):
        'This method assigns dictionary key and values to dict outputdict'
        outputdict = {}
        outputdict['productcode'] = self.productcode
        outputdict['description'] = self.description
        outputdict['marketprice'] = self.marketprice
        outputdict['rentalprice'] = self.rentalprice

        return outputdict
