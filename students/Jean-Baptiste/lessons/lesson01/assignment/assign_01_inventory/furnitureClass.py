"""
Module for Furniture Items
"""
from inventoryClass import Inventory

class Furniture(Inventory):
    def __init__(self, **kwargs):
        Inventory.__init__(self, **kwargs)  #
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
        return self.size == "XL"