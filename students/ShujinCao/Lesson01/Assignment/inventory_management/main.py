"""
running main script
"""
from inventory_management.development import add_new_item
from inventory_management.development import item_info
from inventory_management.development import exit_program

def main_menu(user_prompt=None):
    """
    This is the main menu
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:

        options_str = ("{}" + (", {}") * (len(options) - 1)).format(*options)

        print(f"Please choose from the following options {options_str}:")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

if __name__ == '__main__':
    FULLINVENTORY = {}
    while True:
        print(FULLINVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
