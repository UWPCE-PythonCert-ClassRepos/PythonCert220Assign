""" This is a module for furnitures """
# Furniture class
from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """
    Furniture class takes Inventory class as a parent class
    """

    # def __init__(self, productCode, description, marketPrice, rentalPrice,
    #              material, size):
    # Use super().__init__(args) to solve the too many arguments error
    def __init__(self, info):
        Inventory.__init__(self, info)
        # Creates common instance variables from the parent class

        self.material = info['material']
        self.size = info['size']

    def return_as_dictionary(self):
        """
        parameter: self object
        return type: a dictionary of product information
        """
        output_dict =Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
