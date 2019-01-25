"""
# Electric appliances class
"""

from inventory_management.inventoryClass import inventory


class ElectricAppliances(inventory):

    """
    docstring
    """

    def __init__(self, productCode, description, marketPrice, rentalPrice,
                 brand, voltage):

        """
        Creates common instance variables from the parent class
        """

        inventory.__init__(self, productCode, description, marketPrice,
                           rentalPrice)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):

        """
        docstring
        """

        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
