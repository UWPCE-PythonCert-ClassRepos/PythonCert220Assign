class Inventory:
    """Class to hold inventory details"""
    def __init__(self, product_code, description, market_price, rental_price):
        """Establish variables for inventory"""
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """Return dictionary with inventory class variables"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict

    def extra_method(self):
        """Nonsene method for class"""
