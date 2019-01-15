"""Electric appliances module."""
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """Electric Appliances class"""

    def __init__(
            self, product_code, description, market_price, rental_price,
            *args  # brand, voltage
    ):
        Inventory.__init__(
            self, product_code, description, market_price, rental_price
        )  # Creates common instance variables from the parent class

        self.brand = args[0]
        self.voltage = args[1]

    # def return_as_dictionary(self):
    #     output_dict = {}
    #     output_dict["product_code"] = self.product_code
    #     output_dict["description"] = self.description
    #     output_dict["market_price"] = self.market_price
    #     output_dict["rental_price"] = self.rental_price
    #     output_dict["brand"] = self.brand
    #     output_dict["voltage"] = self.voltage
    #
    #     return output_dict
