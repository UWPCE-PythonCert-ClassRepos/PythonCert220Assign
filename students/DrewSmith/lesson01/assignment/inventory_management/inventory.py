'''
Inventory class
'''


class Inventory:
    ''' Base inventory object '''
    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        ''' Return inventory object as a dictionary '''
        output = {}
        output['product_code'] = self.product_code
        output['description'] = self.description
        output['market_price'] = self.market_price
        output['rental_price'] = self.rental_price

        return output
