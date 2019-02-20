"""
Electric appliances class
"""
from inventory import Inventory


def return_inventory(self, product_code, description, market_price, rental_price, brand):
    """
    Return product information in a dictionary
    """
    product_dict = {}
    product_dict['product_code'] = product_code
    product_dict['description'] = description
    product_dict['market_price'] = market_price
    product_dict['rental_price'] = rental_price
    product_dict['brand'] = brand
    product_dict['voltage'] = voltage

    return product_dict
