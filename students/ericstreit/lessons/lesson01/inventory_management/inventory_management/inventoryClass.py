"""
# Inventory class
"""


class inventory:
    """
    The inventory class
    """

    def __init__(self, productCode, description, marketPrice, rentalPrice):
        """
        set the attributes for this
        """

        self.productCode = productCode
        self.description = description
        self.marketPrice = marketPrice
        self.rentalPrice = rentalPrice

    def return_as_dictionary(self):
        """
        Create a dict, add each instance attribute to the dict and return it
        """

        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice

        return output_dict
