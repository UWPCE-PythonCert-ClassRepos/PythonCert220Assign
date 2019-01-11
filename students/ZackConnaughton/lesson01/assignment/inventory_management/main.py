# Launches the user interface for the inventory management system
import sys
import market_prices
import inventoryClass
import furnitureClass
import electricAppliancesClass

FULL_INVENTORY = {}

def main_menu(user_prompt=None):
    valid_prompts = {"1": add_new_item,
                     "2": itemInfo,
                     "q": exitProgram}
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
    return input(prompt)

def get_price(item_code):
    output = "Get price"
    print(output)
    return output


def add_new_item():
    global FULL_INVENTORY
    item_code = get_input("Enter item code: ")
    item_desc = get_input("Enter item description: ")
    item_rental_price = get_input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = get_input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = get_input("Enter item material: ")
        item_size = get_input("Enter item size (S,M,L,XL): ")
        new_item = furnitureClass.furniture(item_code, item_desc, item_price,
                                            item_rental_price, item_material, item_size)
    else:
        is_electrical_appliance = get_input("Is this item an electric appliance? (Y/N): ")
        if is_electrical_appliance.lower() == "y":
            item_brand = get_input("Enter item brand: ")
            item_voltage = get_input("Enter item voltage: ")
            new_item = electricAppliancesClass.electricAppliances(item_code, item_desc, item_price, item_rental_price,
                                                                  item_brand, item_voltage)
        else:
            new_item = inventoryClass.inventory(item_code, item_desc, item_price, item_rental_price)
    FULL_INVENTORY[item_code] = new_item.returnAsDictionary()
    print("New inventory item added")
    return new_item.returnAsDictionary


def itemInfo():
    item_code = get_input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        printDict = FULL_INVENTORY[item_code]
        output = ""
        for k, v in printDict.items():
            output += ("{}:{}{}".format(k, v, "\n"))
    else:
        output="Item not found in inventory"
    print(output)
    return output


def exitProgram():
    sys.exit()

if __name__ == '__main__':
    #FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
