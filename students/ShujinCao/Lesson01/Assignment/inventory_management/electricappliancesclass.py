"""
Electric appliances class
"""
from inventoryclass import Inventory


class ElectricAppliances(Inventory):
    """
    class electric appliances
    """

    def __init__(self, product_code, description,
                 market_price, rental_price, brand, voltage):
        super().__init__()
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
