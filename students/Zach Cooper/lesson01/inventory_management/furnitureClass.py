"""Furniture class"""

# Furniture class
# from inventory_management.inventoryClass import Inventory
from inventoryClass import Inventory


class Furniture(Inventory):
    """
    This is a class furniture information
    """

    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict


# class Furniture(Inventory):

#     def __init__(self, productCode, description, rentalPrice,
#                  marketPrice, material, size):
#         Inventory.__init__(self, productCode, description,
#                            rentalPrice, marketPrice)
#         #### Call SUPER() ####
#         # super().___init__(args)
#         # Creates common instance variables from the parent class

#         self.material = material
#         self.size = size

#     def returnAsDictionary(self):
#         outputDict = super(Furniture, self).returnAsDictionary()
#         # outputDict = {}
#         # outputDict['productCode'] = self.productCode
#         # outputDict['description'] = self.description
#         # outputDict['rentalPrice'] = self.rentalPrice
#         # outputDict['marketPrice'] = self.marketPrice
#         outputDict['material'] = self.material
#         outputDict['size'] = self.size

#         return outputDict
