"""
electrical appliance class with electrical appliance items
"""

from inventory_management.inventory_class import Inventory

class ElecAppliances(Inventory):
    """
    electrical appliance class
    """

    def __init__(self, inventory_item, brand, voltage):
        """
        initializes electrical appliance item
        """
        Inventory.__init__(self, inventory_item.product_code, inventory_item.description,
                           inventory_item.market_price, inventory_item.rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        returns electrical appliances as a dictionary
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
