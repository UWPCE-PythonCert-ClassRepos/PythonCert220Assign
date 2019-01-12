"""
Docstring
"""
# Furniture class
from .inventoryClass import inventory


class furniture(inventory):
    """
    Docstring
    """
    def __init__(self, productCode, description, marketPrice, rentalPrice, material, size):
        """
        Docstring
        """
        inventory.__init__(self,
                           productCode,
                           description,
                           marketPrice,
                           rentalPrice) # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def returnAsDictionary(self):
        """
        Docstring
        """
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
