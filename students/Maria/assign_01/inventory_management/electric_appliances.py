"""
Electric appliances class
"""
from inventory import Inventory


class ElectricAppliances(Inventory):
    """
    Electric Appliances
    """
    def __init__(self, product_code, description, market_price, rental_price, brand,
                 voltage):
        # Creates common instance variables from the parent class
        super().__init__(self, product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_dictionary(self):
        """
        Return product information in a dictionary
        """
        product_dict = {}
        product_dict['product_code'] = self.product_code
        product_dict['description'] = self.description
        product_dict['market_price'] = self.market_price
        product_dict['rental_price'] = self.rental_price
        product_dict['brand'] = self.brand
        product_dict['voltage'] = self.voltage

        return product_dict
