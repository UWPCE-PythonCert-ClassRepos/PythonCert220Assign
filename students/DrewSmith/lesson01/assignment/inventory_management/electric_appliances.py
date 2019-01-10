'''
Electric appliances class
'''


from .inventory import Inventory

# pylint: disable=R0903
class ElectricAppliance(Inventory):
    ''' Represent an electric appliance '''

    def __init__(self, productCode, description, marketPrice, rentalPrice, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, productCode, description, marketPrice, rentalPrice)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        output = Inventory.return_as_dictionary(self)
        output['brand'] = self.brand
        output['voltage'] = self.voltage

        return output
