"""
# Inventory class
"""


class inventory:
    """
    docstring
    """

    def __init__(self, productCode, description, marketPrice, rentalPrice):
        """
        doc docstring
        """

        self.productCode = productCode
        self.description = description
        self.marketPrice = marketPrice
        self.rentalPrice = rentalPrice

    def return_as_dictionary(self):
        """
        docstring
        """

        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice

        return output_dict
