"""This is the furnature class file."""

from .inventory_class import Inventory


class Furniture(Inventory):
    """Class of furniture with initializer and functions."""

    def __init__(
            self, product_code, description, market_price, rental_price,
            *args  # material, size
    ):

        Inventory.__init__(
            self, product_code, description, market_price, rental_price
        )  # Creates common instance variables from the parent class
        self.material = args[0]
        self.size = args[1]
