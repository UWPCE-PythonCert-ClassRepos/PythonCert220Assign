"""Electric appliances module."""

from .inventory_class import Inventory


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
