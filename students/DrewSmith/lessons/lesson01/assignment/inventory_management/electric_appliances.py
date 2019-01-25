'''
Electric appliances class
'''


from inventory_management.inventory import Inventory

# pylint: disable=R0913
class ElectricAppliance(Inventory):
    ''' Represent an electric appliance '''

    inventory_type = "Electric Appliance"

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        output = Inventory.return_as_dictionary(self)
        output['brand'] = self.brand
        output['voltage'] = self.voltage

        return output

    @staticmethod
    def sort_key(item):
        '''
        Standard sort key
        '''
        return (item.description, item.product_code)
