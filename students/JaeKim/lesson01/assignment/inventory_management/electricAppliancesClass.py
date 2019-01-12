"""
Docstring
"""
# Electric appliances class
from inventoryClass import inventory

class electricAppliances(inventory):
    """
    Docstring
    """
    def __init__(self, productCode, description, marketPrice, rentalPrice, brand, voltage):
        """
        Docstring
        """
        inventory.__init__(self, productCode, description,
                           marketPrice, rentalPrice)
        self.brand = brand
        self.voltage = voltage

    def returnAsDictionary(self):
        """
        Docstring
        """
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
