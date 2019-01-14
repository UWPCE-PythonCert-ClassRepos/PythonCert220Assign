""" Launches the user interface for the inventory management system """
import sys
from inventory_management import market_prices
from inventory_management.inventoryclass import Inventory
from inventory_management.furnitureclass import Furniture
from inventory_management.electricappliancesclass import ElectricAppliances


def get_price(item_code):
    """ a methond to finds item price """

    print("Get price")


def add_new_item(FULLINVENTORY):
    """ add_new_item """
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rentalprice = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = Furniture(
            item_code,
            item_description,
            item_price,
            item_rentalprice,
            item_material,
            item_size
        )
    else:

        is_electricappliance = input(
            "Is this item an electric appliance? (Y/N): ")
        if is_electricappliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = ElectricAppliances(
                item_code,
                item_description,
                item_price,
                item_rentalprice,
                item_brand,
                item_voltage
            )
        else:
            new_item = Inventory(
                item_code,
                item_description,
                item_price,
                item_rentalprice
            )
    FULLINVENTORY[item_code] = new_item.returnas_dictionary()
    print("New inventory item added")
    return FULLINVENTORY


def item_info(FULLINVENTORY):
    """ item_info """

    item_code = input("Enter item code: ")
    if item_code in FULLINVENTORY:
        print_dict = FULLINVENTORY[item_code]
        for k, value in print_dict.items():
            print("{}:{}".format(k, value))
    else:
        print("Item not found in inventory")
    return FULLINVENTORY


def exit_program():
    """ exit_program """

    sys.exit()
