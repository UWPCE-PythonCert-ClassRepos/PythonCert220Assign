'''
Launches the user interface for the inventory management system
'''


import sys
import inventory_management.market_prices as market_prices
from inventory_management import management

def main_menu(user_prompt=None):
    '''
    Initial entry menu for this application
    '''

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
        user_prompt = safe_input(">")
    return valid_prompts.get(user_prompt)

def safe_input(prompt, values_dict=None, property_key=None):
    """
    Return user input or None if error occurs

    :param prompt: User prompt to display
    :param values_dict: dictionary of values to use instead of asking user
    :param property_key: dictionary key to get value from values_dict
    """
    while True:
        try:
            if values_dict is not None and property_key is not None:
                if property_key in values_dict:
                    return values_dict[property_key]
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("Error! Please try again.")

def add_new_item(properties=None):
    '''
    Add new item to inventory list

    :param properties: property dict of values to enter.
        Any missing will be asked to the user
    '''
    properties = properties or {}

    properties["product_code"] = safe_input(
        "Enter item product code: ", properties, "product_code")
    properties["description"] = safe_input(
        "Enter item description: ", properties, "description")
    properties["rental_price"] = safe_input(
        "Enter item rental price: ", properties, "rental_price")

    properties["is_furniture"] = safe_input(
        "Is this item a piece of furniture? (Y/N): ", properties, "is_furniture")

    if properties["is_furniture"].lower() == "y":
        properties["material"] = safe_input("Enter material: ", properties, "material")
        properties["size"] = safe_input("Enter item size (S,M,L,XL): ", properties, "size")

        management.add_furniture(properties, market_prices)
    else:
        properties["is_electric_appliance"] = safe_input(
            "Is this item a piece of electric appliance? (Y/N): ",
            properties, "is_electric_appliance")

        if properties["is_electric_appliance"].lower() == "y":
            properties["brand"] = safe_input("Enter item brand: ", properties, "brand")
            properties["voltage"] = safe_input("Enter item voltage: ", properties, "voltage")

            management.add_electric_appliance(properties, market_prices)
        else:
            management.add_inventory(properties, market_prices)
    print("New inventory item added")

def item_info(product_code=None):
    '''
    Display a given product details
    '''
    if product_code is None:
        product_code = safe_input("Enter item code: ")
    item = management.get_item(product_code)

    if item is not None:
        for key, value in item.items():
            print("{}:{}".format(key, value))
    else:
        print("Item not found in inventory")

def exit_program():
    '''
    Exits the program
    '''
    sys.exit()

if __name__ == '__main__':
    while True:
        main_menu()()
