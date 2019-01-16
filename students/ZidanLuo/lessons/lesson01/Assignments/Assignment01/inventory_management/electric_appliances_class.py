""" This is a module for the electric appliances products """
# Electric appliances class
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    ElectricAppliances class is a subclass of Inventory
    """

    # def __init__(self, productCode, description, marketPrice, rentalPrice,
    #              brand, voltage):
    # Solve the too many arguments error
    def __init__(self, info):
        Inventory.__init__(self, info)
        self.brand = info['brand']
        self.voltage = info['voltage']


    def return_as_dictionary(self):
        """
        parameter: self object
        return type: a dictionary of product information
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
