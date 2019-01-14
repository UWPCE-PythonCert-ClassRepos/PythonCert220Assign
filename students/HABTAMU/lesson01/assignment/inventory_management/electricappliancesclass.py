""" Electric appliances class """

from inventory_management.inventoryclass import Inventory


class ElectricAppliances(Inventory):
    """electricAppliances __doc__str here"""


    def __init__(self, productcode, description, marketprice, rentalprice, brand, voltage):
        Inventory.__init__(self, productcode, description, marketprice, rentalprice)
        # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def returnas_dictionary(self):
        outputdict = super(ElectricAppliances, self).returnas_dictionary()
    #     outputdict['productcode'] = self.productcode
    #     outputdict['description'] = self.description
    #     outputdict['marketprice'] = self.marketprice
    #     outputdict['rentalprice'] = self.rentalprice
        outputdict['brand'] = self.brand
        outputdict['voltage'] = self.voltage

        return outputdict
