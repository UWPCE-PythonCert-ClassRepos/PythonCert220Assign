""" This module integrates all of the other classes in the inventory
management system """
# Launches the user interface for the inventory management system
import sys
import market_prices
import inventory_class
import furniture_class
import electric_appliances_class


def main_menu(user_prompt=None):
    """
    Main menu for the users to enter requests
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
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
    returns the price of the product
    """
    print("Get price")

def add_new_item():
    """
    This is a method to add new items to the inventory
    """
    global FULL_INVENTORY
    product_info = {}
    product_info['product_code'] = input("Enter item code: ")
    product_info['description'] = input("Enter item description: ")
    product_info['rental_price'] = input("Enter item rental price: ")

    # Get price from the market prices module
    product_info['market_price'] = market_prices.get_latest_price(product_info['product_code'])

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        product_info['material'] = input("Enter item material: ")
        product_info['size'] = input("Enter item size (S,M,L,XL): ")
        new_item = furniture_class.Furniture(product_info)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            product_info['brand'] = input("Enter item brand: ")
            product_info['voltage'] = input("Enter item voltage: ")
            new_item = electric_appliances_class.ElectricAppliances(product_info)
        else:
            new_item = inventory_class.Inventory(product_info)
    FULL_INVENTORY[product_info['product_code']] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """
    This method prints the information of the item
    """
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for k, val in print_dict.items():
            print("{}:{}".format(k, val))
    else:
        print("Item not found in inventory")

def exit_program():
    """
    Exit the program
    """
    sys.exit()

if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
