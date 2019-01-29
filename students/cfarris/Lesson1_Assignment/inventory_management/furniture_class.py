""" Furniture class """

from inventory_management.inventory_class import Inventory  # for testing

# from inventory_class import Inventory


class Furniture(Inventory):
    """Furniture class to store information about furniture object"""

    def __init__(self,
                 product_code,
                 description,
                 market_price,
                 rental_price,
                 material,
                 size):
        self.material = material
        self.size = size
        # Creates common instance variables from the parent class
        Inventory.__init__(self,
                           product_code,
                           description,
                           market_price,
                           rental_price)
        self.output_dict['material'] = self.material
        self.output_dict['size'] = self.size

    def return_as_dictionary(self):
        """return dictionary describing furniture object"""

        return self.output_dict
