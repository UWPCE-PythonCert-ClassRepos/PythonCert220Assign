"""
Module for Furniture Items
"""
# Furniture class
from inventory_management.InventoryClass import Inventory


class Furniture(Inventory):
    """
    Class for Furniture Items
    """

    def __init__(self, **kwargs):
        Inventory.__init__(
            self, **kwargs
        )  # Creates common instance variables from the parent class

        self.material = kwargs["item_material"]
        self.size = kwargs["size"]

    def return_as_dictionary(self):
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict

    def check_for_big_screen(self):
        """
        Check if it's big enough for a big screen TV
        """
        return self.size == "XL"
