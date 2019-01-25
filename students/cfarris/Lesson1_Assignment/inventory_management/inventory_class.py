""" Inventory class """


class Inventory:
    """Inventory Superclass inherited by furniture and electric appliances"""

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price
        self.output_dict = {}
        self.output_dict['product_code'] = self.product_code
        self.output_dict['description'] = self.description
        self.output_dict['market_price'] = self.market_price
        self.output_dict['rental_price'] = self.rental_price

    def return_as_dictionary(self):
        """return inventory items as a dictionary with contents therein """

        return self.output_dict
