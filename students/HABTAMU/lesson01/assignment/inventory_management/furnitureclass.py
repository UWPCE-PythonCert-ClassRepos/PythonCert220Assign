""" Furniture class """
from inventory_management.inventoryclass import Inventory


class Furniture(Inventory):
    """ Furniture class """


    def __init__(self, productcode, description, marketprice, rentalprice, material, size):
        Inventory.__init__(self, productcode, description, marketprice, rentalprice)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def returnas_dictionary(self):
        outputdict = super(Furniture, self).returnas_dictionary()
        outputdict['material'] = self.material
        outputdict['size'] = self.size

        return outputdict
