"""Electric Appliances Class"""

# from inventory_management.inventoryClass import Inventory
from inventoryClass import Inventory


class ElectricAppliances(Inventory):
    """
    Contains all information about electronic appliances
    """

    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        """
        Initializes class
        """
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)
        # Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        Returns dict with Electric App information
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict




# class ElectricAppliances(Inventory):

#     def __init__(self, productCode, description, rentalPrice,
#                  marketPrice, brand, voltage):

#         Inventory.__init__(self, productCode, description,
#                            rentalPrice, marketPrice)
#         #### Call Super()####
#     # Creates common instance variables from the parent class

#         self.brand = brand
#         self.voltage = voltage

#     def returnAsDictionary(self):
#         outputDict = super(ElectricAppliances, self).returnAsDictionary()
#         # outputDict = {}
#         # outputDict['productCode'] = self.productCode
#         # outputDict['description'] = self.description
#         # outputDict['rentalPrice'] = self.rentalPrice
#         # outputDict['marketPrice'] = self.marketPrice
#         outputDict['brand'] = self.brand
#         outputDict['voltage'] = self.voltage

#         return outputDict
