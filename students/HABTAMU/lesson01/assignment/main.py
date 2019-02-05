""" Launches the user interface for the inventory management system """
from inventory_management.management import add_new_item, exit_program, item_info


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


if __name__ == '__main__':
    FULLINVENTORY = {}
    while True:
        print(FULLINVENTORY)
        FULLINVENTORY = main_menu()(FULLINVENTORY)
        input("Press Enter to continue...........")
