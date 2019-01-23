"""
This file contains all the code necessary to run the main menu
"""


import sys
import inventory_management.market_prices
import inventory_management.inventory_class
import inventory_management.furniture_class
import inventory_management.electric_appliances_class


def main_menu(user_prompt=None):
    """
    runs main menu
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program
                     }
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options ({}):".format(options_str))
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

def get_price(item_code):
    """
    looks up prices
    """
    #need code to look up the price of an item here
    print("Get price")


def add_new_item():
    """
    adds new item to inventory
    """
    global FULL_INVENTORY
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = furniture_class.Furniture(item_code,
                                             item_description,
                                             item_price,
                                             item_rental_price,
                                             item_material,
                                             item_size)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = electric_appliances_class.ElectricAppliances(item_brand,
                                                                    item_voltage,
                                                                    item_code,
                                                                    item_description,
                                                                    item_price,
                                                                    item_rental_price)
        else:
            new_item = inventory_class.Inventory(item_code,
                                                 item_description,
                                                 item_price,
                                                 item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """
    looks up information about an item, returns if exists
    """
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for key, value in print_dict.items():
            print("{}:{}".format(key, value))
    else:
        print("Item not found in inventory")

def exit_program():
    """
    exits program
    """
    sys.exit()
