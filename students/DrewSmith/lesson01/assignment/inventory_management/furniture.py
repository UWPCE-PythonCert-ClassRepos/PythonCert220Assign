'''
Represents furniture for inventory
'''


from .inventory import Inventory

class Furniture(Inventory):
    ''' Represent an furniture '''

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        ''' Output furniture as a dictionary '''

        output = Inventory.return_as_dictionary(self)
        output['material'] = self.material
        output['size'] = self.size

        return output
