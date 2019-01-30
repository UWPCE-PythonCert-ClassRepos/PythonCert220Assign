""" This is a module for inventory """
# Inventory class
class Inventory:
    """
    Inventory class includes methods which return the information of the inventories
    """

    def __init__(self, product_info):
        self.product_code = product_info['product_code']
        self.description = product_info['description']
        self.market_price = product_info['market_price']
        self.rental_price = product_info['rental_price']

    def return_as_dictionary(self):
        """
        parameter: self object
        return type: a dictionary of product information
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
