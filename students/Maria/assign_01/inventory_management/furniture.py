"""
Furniture class
"""
from inventory import Inventory

class Furniture(Inventory):
    """
    Furntiture Class
    """
    def __init__(self, product_code, description, market_price, rental_price, material,
                 size):
        # Creates common instance variables from the parent class
        super().__init__(self, product_code, description, market_price, rental_price)
        self.material = material
        self.size = size

    def return_dictionary(self):
        """
        Return product info as dictionary
        """
        product_dict = {}
        product_dict['product_code'] = self.product_code
        product_dict['description'] = self.description
        product_dict['market_price'] = self.market_price
        product_dict['rental_price'] = self.rental_price
        product_dict['material'] = self.material
        product_dict['size'] = self.size

        return product_dict
