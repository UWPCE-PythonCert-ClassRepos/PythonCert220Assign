from unittest.mock import MagicMock
from unittest.mock import patch
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.menu as menu


def test_inventory():
    """
    tests inventory initializing function
    """
    chair = Inventory(4000, "lawn chair", 5.00, 6.00)

    assert chair.product_code == 4000
    assert chair.description == "lawn chair"
    assert chair.market_price == 5.00
    assert chair.rental_price == 6.00


def test_inventory_return_as_dict():
    """
    tests inventory class returning a dict of all information about an item in the inventory
    """
    chair = Inventory(4000, "lawn chair", 5.00, 6.00)

    assert chair.return_as_dictionary() == {"product_code": 4000, "description": "lawn chair",
                                            "market_price": 5.00, "rental_price": 6.00}


def test_furniture():
    """
    tests initializing function of furniture class
    """
    chair = Furniture(4000, "lawn chair", 5.00, 6.00, "wood", "5' x 11'")

    assert chair.product_code == 4000
    assert chair.description == "lawn chair"
    assert chair.market_price == 5.00
    assert chair.rental_price == 6.00
    assert chair.material == "wood"
    assert chair.size == "5' x 11'"


def test_furniture_return_as_dict():
    """
    tests furniture class to return information about furniture items in the inventory class as a dict
    """
    chair = Furniture(4000, "lawn chair", 5.00, 6.00, "wood", "5' x 11'")

    assert chair.return_as_dictionary() == {"product_code": 4000, "description": "lawn chair",
                                            "market_price": 5.00, "rental_price": 6.00,
                                            "material": "wood", "size": "5' x 11'"}


def test_electric_appliances():
    """
    tests electric appliances initializing function
    """
    washing_machine = ElectricAppliances(4000, "washing machine", 5.00, 6.00, "GE", "200 V")

    assert washing_machine.product_code == 4000
    assert washing_machine.description == "washing machine"
    assert washing_machine.market_price == 5.00
    assert washing_machine.rental_price == 6.00
    assert washing_machine.brand == "GE"
    assert washing_machine.voltage == "200 V"


def test_electric_appliances_return_as_dict():
    """
    tests electric appliances class to return information about electric appliances in the inventory class as a dict
    """
    washing_machine = ElectricAppliances(4000, "washing machine", 5.00, 6.00, "GE", "200 V")

    assert washing_machine.return_as_dictionary() == {"product_code": 4000, "description": "washing machine",
                                                        "market_price": 5.00, "rental_price": 6.00,
                                                        "brand": "GE", "voltage": "200 V"}


def test_that_main_menu_returns_add_function_when_user_input_is_1():
    """tests that in main menu function, user input of 1 will return add_new_item"""
    with patch("builtins.input", return_value = "1"):
        func = menu.main_menu()

        assert func == menu.add_new_item


def test_that_main_menu_returns_item_info_when_user_input_is_2():
    """tests that in main menu function, user input of 2 will return item_info"""
    with patch("builtins.input", return_value = "2"):
        func = menu.main_menu()

        assert func == menu.item_info


def test_that_main_menu_returns_exit_program_when_user_input_is_q():
    """tests that in main menu function, user input of q will return exit_program"""
    with patch("builtins.input", return_value = "q"):
        func = menu.main_menu()

        assert func == menu.exit_program


