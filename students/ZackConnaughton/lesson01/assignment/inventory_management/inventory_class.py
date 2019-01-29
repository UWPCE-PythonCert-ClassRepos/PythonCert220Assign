"""
handles the inventory
"""

class Inventory:
    """
    Inventory basic class for handling all the standard inventory properties
    """

    def __init__(self, product_code, description, market_price, rental_price):
        """
        initializes the inventory with the basic properties needed
        """
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        returns the inventory item as a dictionary
        """

        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
