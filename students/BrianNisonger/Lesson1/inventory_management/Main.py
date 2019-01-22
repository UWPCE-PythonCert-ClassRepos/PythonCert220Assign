"""
Launches the user interface for the inventory management system
"""
import sys

from inventory_management.market_prices import get_latest_price
from inventory_management.InventoryClass import Inventory
from inventory_management.ElectricAppliancesClass import ElectricAppliances
from inventory_management.FurnitureClass import Furniture


def generate_menu(user_prompt=None):
    """
    Generate menu
    """
    valid_prompts = {"1": add_new_item, "2": item_info, "q": exit_program}
    if user_prompt not in valid_prompts:
        return False
    return valid_prompts.get(user_prompt)


def main_menu():
    """
    Request user input for Menu
    """
    function = None
    while not function:
        print("Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
        function = generate_menu(user_prompt)
    return function


def get_price():
    """
    Should get the price of the object
    """
    return get_latest_price()


def input_item_info():
    """
    I/O operations for entering new item
    """
    item_dict = {}
    item_dict["item_code"] = input("Enter item code: ")
    item_dict["item_description"] = input("Enter item description: ")
    item_dict["item_rental_price"] = input("Enter item rental price: ")
    is_furniture_string = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture_string.lower() == "y":
        item_dict = input_furniture(item_dict)
    else:
        is_electric_appliance = input(
            "Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_dict = input_electric(item_dict)
    return item_dict


def input_furniture(item_dict):
    """
    I/O for furniture
    """
    item_dict["item_material"] = input("Enter item material: ")
    item_dict["size"] = input("Enter item size (S,M,L,XL): ")
    item_dict["style"] = "furniture"
    return item_dict


def input_electric(item_dict):
    """
    I/O for electic Appliances
    """
    item_dict["brand"] = input("Enter item brand: ")
    item_dict["voltage"] = input("Enter item voltage: ")
    item_dict["style"] = "electric"
    return item_dict


def add_new_item(f_inventory):
    """
    Function to add an additional item to Inventory
    """
    # Get price from the market prices module
    item_price = get_price()
    item_dict = input_item_info()
    item_dict["item_price"] = item_price
    if item_dict.get("style") == "furniture":
        new_item = Furniture(**item_dict)
    elif item_dict.get("style") == "electric":
        new_item = ElectricAppliances(**item_dict)
    else:
        new_item = Inventory(**item_dict)
    f_inventory[item_dict["item_code"]] = new_item.return_as_dictionary()
    print("New inventory item added")
    return f_inventory


def return_item_info(f_inventory, item_code):
    """
    Returns item info if found, otherwise returns not found
    """
    item_string = ""
    if item_code in f_inventory:
        print_dict = f_inventory[item_code]
        for key, value in print_dict.items():
            item_string += "{}:{}\n".format(key, value)
    else:
        item_string = "Item not found in inventory"
    return item_string


def item_info(f_inventory):
    """
    Prints info about the items
    """
    item_code = input("Enter item code: ")
    print(return_item_info(f_inventory, item_code))
    return f_inventory


def exit_program(f_inventory):
    """
    Exits the loop
    """
    sys.exit()
    return f_inventory


if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        FULL_INVENTORY = main_menu()(FULL_INVENTORY)
        input("Press Enter to continue...........")
