""" Launches the user interface for the inventory management system """
import sys
import market_prices
import inventoryclass
import furnitureclass
import electricappliancesclass


def main_menu(user_prompt=None):
    """ menu switcher methond """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def get_price(item_code):
    """ a methond to finds item price """

    print("Get price")


def add_new_item():
    """ add_new_item """

    global FULLINVENTORY
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rentalprice = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = furnitureclass.Furniture(
            item_code,
            item_description,
            item_price,
            item_rentalprice,
            item_material,
            item_size
            )
    else:

        is_electricappliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electricappliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = electricappliancesclass.ElectricAppliances(
                item_code,
                item_description,
                item_price,
                item_rentalprice,
                item_brand,
                item_voltage
            )
        else:
            new_item = inventoryclass.Inventory(
                item_code,
                item_description,
                item_price,
                item_rentalprice
            )
    FULLINVENTORY[item_code] = new_item.returnas_dictionary()
    print("New inventory item added")


def item_info():
    """ item_info """

    item_code = input("Enter item code: ")
    if item_code in FULLINVENTORY:
        print_dict = FULLINVENTORY[item_code]
        for k, value in print_dict.items():
            print("{}:{}".format(k, value))
    else:
        print("Item not found in inventory")


def exit_program():
    """ exit_program """

    sys.exit()


if __name__ == '__main__':
    FULLINVENTORY = {}
    while True:
        print(FULLINVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
