'''
Represents furniture for inventory
'''


from inventory_management.inventory import Inventory

# pylint: disable=R0913
class Furniture(Inventory):
    ''' Represent an furniture '''

    inventory_type = "Furniture"

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

    @staticmethod
    def sort_key(item):
        '''
        Standard sort key
        '''
        return (item.description, item.product_code)
