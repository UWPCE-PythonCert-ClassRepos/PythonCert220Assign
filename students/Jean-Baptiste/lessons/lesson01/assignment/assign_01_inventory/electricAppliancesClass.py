"""
Module for Electric Appliances
"""
from inventoryClass import Inventory

class ElectricAppliances(Inventory):
    def __init__(self, **kwargs):
        Inventory.__init__(self, **kwargs)
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