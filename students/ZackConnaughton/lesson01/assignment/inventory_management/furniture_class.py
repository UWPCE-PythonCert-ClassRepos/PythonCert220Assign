"""
creates an inventory item that has properties of Furniture
"""

from inventory_management.inventory_class import Inventory

class Furniture(Inventory):
    """
    Furniture extends inventory
    creates n inventory item that has furniture properties
    """

    def __init__(self, inventory_item, material, size):

        Inventory.__init__(self, inventory_item.product_code, inventory_item.description,
                           inventory_item.market_price, inventory_item.rental_price)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
