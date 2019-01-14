# Inventory class
"""
Module for Inventory Object
"""
from inventory_management.market_prices import get_latest_price


class Inventory:
    """
    Class for Inventory Object
    """

    def __init__(self, **kwargs):
        self.product_code = kwargs["item_code"]
        self.description = kwargs["item_description"]
        self.market_price = kwargs["item_price"]
        self.rental_price = kwargs["item_rental_price"]

    def return_as_dictionary(self):
        """
        Method for taking values and putting them in a dictionary
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict

    def check_market_price(self):
        """
        Checks the market price
        """
        return self.market_price == get_latest_price()
