"""Electric appliances class"""
from inventory_management.inventory_class import Inventory  # for testing

# from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """creates an electrical appliance class"""

    def __init__(self, product_code,
                 description,
                 market_price,
                 rental_price,
                 brand,
                 voltage):
        # Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

        Inventory.__init__(self,
                           product_code,
                           description,
                           market_price,
                           rental_price
                           )
        self.output_dict['brand'] = self.brand
        self.output_dict['voltage'] = self.voltage

    def return_as_dictionary(self):
        """return output.dict """

        return self.output_dict
