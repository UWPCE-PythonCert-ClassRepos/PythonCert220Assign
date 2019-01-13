"""
Docstring
"""
# Inventory class


class inventory:
    """
    Docstring
    """

    def __init__(self, productcode, description, marketprice, rentalprice):
        """
        Docstring
        """
        self.productCode = productcode
        self.description = description
        self.marketPrice = marketprice
        self.rentalPrice = rentalprice

    def returnAsDictionary(self):
        """
        Docstring
        """
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice

        return output_dict
