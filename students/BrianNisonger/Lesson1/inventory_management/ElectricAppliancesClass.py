"""
Module for Electric Appliances
"""
from inventory_management.InventoryClass import Inventory


class ElectricAppliances(Inventory):
    """
    class for Electric Appliances
    """

    def __init__(self, **kwargs):
        Inventory.__init__(
            self, **kwargs
        )  # Creates common instance variables from the parent class

        self.brand = kwargs["brand"]
        self.voltage = kwargs["voltage"]

    def return_as_dictionary(self):
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage
        return output_dict

    def check_wattage(self, amp):
        """
        Calculate wattage
        """
        return self.voltage * amp
