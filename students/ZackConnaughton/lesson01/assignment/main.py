"""
Launches the user interface for the inventory management system
"""
import sys
# import inventory_management.market_prices as market_prices
# import inventory_management.inventory_class as inventory_class
# import inventory_management.furniture_class as furniture_class
# import inventory_management.elec_appliances_class as elec_appliances_class
from inventory_management import market_prices
from inventory_management import inventory_class
from inventory_management import furniture_class
from inventory_management import elec_appliances_class

FULL_INVENTORY = {}

def main_menu(user_prompt=None):
    """
    main user entry menues
    returns a function name to run
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = get_input(">")
    return valid_prompts.get(user_prompt)

def get_input(prompt):
    """
    shows user the provided prompt
    returns the user input provided
    """
    return input(prompt)

def get_price(item_code):
    """
    gets the price of an item based on the item code provided
    returns "Get price" currently
    """
    output = "Get price for item {}.".format(item_code)
    print(output)
    return output


def add_new_item():
    """
    add a new item to the inventory based on user inputs
    """
    #global FULL_INVENTORY
    item_code = get_input("Enter item code: ")
    item_desc = get_input("Enter item description: ")
    item_rental_price = get_input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)
    new_inventory_item = inventory_class.Inventory(item_code, item_desc,
                                                   item_price, item_rental_price)
    is_furniture = get_input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = get_input("Enter item material: ")
        item_size = get_input("Enter item size (S,M,L,XL): ")
        new_item = furniture_class.Furniture(new_inventory_item, item_material, item_size)
    else:
        is_electrical_appliance = get_input("Is this item an electric appliance? (Y/N): ")
        if is_electrical_appliance.lower() == "y":
            item_brand = get_input("Enter item brand: ")
            item_voltage = get_input("Enter item voltage: ")
            new_item = elec_appliances_class.ElecAppliances(new_inventory_item,
                                                            item_brand, item_voltage)
        else:
            new_item = new_inventory_item
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")
    return new_item.return_as_dictionary


def item_info():
    """
    gets item info based on user input
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
    exits the program
    """
    sys.exit()

if __name__ == '__main__':
    #FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
