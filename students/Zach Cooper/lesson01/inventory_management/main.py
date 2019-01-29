"""
This file contains all the code necessary to run the main menu
"""


import sys
from inventory_management.market_prices import get_latest_price
from inventory_management.inventoryClass import Inventory
from inventory_management.furnitureClass import Furniture
from inventory_management.electricAppliancesClass import ElectricAppliances
# import sys
# import market_prices
# import inventoryClass
# import furnitureClass
# import electricAppliancesClass


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
        options_str = ("{}" + (", {}") * (len(options) - 1)).format(*options)
        print("Please choose from the following options ({}):".format(options_str))
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = get_input(">")
    return valid_prompts.get(user_prompt)


def get_input(prompt):
    """
    shows user the provided prompt
    returns the user input
    """
    return input(prompt)


def get_price(item_code):
    """
    looks up prices
    """
    output = "Get price for item {}.".format(item_code)
    print(output)
    return output


def add_new_item():
    """
    adds new item to inventory
    """
    global FULL_INVENTORY
    item_code = get_input("Enter item code: ")
    item_description = get_input("Enter item description: ")
    item_rental_price = get_input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = get_input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = get_input("Enter item material: ")
        item_size = get_input("Enter item size (S,M,L,XL): ")
        new_item = furnitureClass.Furniture(item_code,
                                            item_description,
                                            item_price,
                                            item_rental_price,
                                            item_material,
                                            item_size)
    else:
        is_electric_appliance = get_input("Is this item an electric"
                                          "appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = get_input("Enter item brand: ")
            item_voltage = get_input("Enter item voltage: ")
            new_item = electricAppliancesClass.ElectricAppliances(item_brand,
                                                                  item_voltage,
                                                                  item_code,
                                                                  item_description,
                                                                  item_price,
                                                                  item_rental_price)
        else:
            new_item = inventoryClass.Inventory(item_code,
                                                item_description,
                                                item_price,
                                                item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """
    looks up information about an item, returns if exists
    """
    item_code = get_input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        output = ""
        for key, value in print_dict.items():
            output += ("{}:{}{}".format(key, value, "\n"))
    else:
        output = "Item not found in inventory"
    print(output)
    return output


def exit_program():
    """
    exits program
    """
    sys.exit()


if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
