"""Inventory class"""


# Inventory class
class Inventory:
    """
    contains all information about each item in the inventory
    """

    def __init__(self, product_code, description, market_price, rental_price):
        """initializes class"""
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """returns Inventory information as a dictionary"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict


# class Inventory:

#     def __init__(self, productCode, description, marketPrice,
#                  rentalPrice):
#         self.productCode = productCode
#         self.description = description
#         self.marketPrice = marketPrice
#         self.rentalPrice = rentalPrice

#     def returnAsDictionary(self):
#         outputDict = {}
#         outputDict['productCode'] = self.productCode
#         outputDict['description'] = self.description
#         outputDict['marketPrice'] = self.marketPrice
#         outputDict['rentalPrice'] = self.rentalPrice

#         return outputDict
