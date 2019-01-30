'''
Manages inventory functionalities
'''


import inventory_management.inventory as inventory
import inventory_management.furniture as furniture
import inventory_management.electric_appliances as electric_appliances

FULL_INVENTORY = {}

def add_inventory(properties, pricing):
    '''
    Add new inventory item

    :param properties: inventory properties
    '''
    inventory_item = inventory.Inventory(
        properties["product_code"], properties["description"],
        pricing.get_latest_price(properties["product_code"]), properties["rental_price"])
    FULL_INVENTORY[properties["product_code"]] = inventory_item

def add_furniture(properties, pricing):
    '''
    Add new furniture item

    :param properties: furniture properties
    '''
    inventory_item = furniture.Furniture(
        properties["product_code"], properties["description"],
        pricing.get_latest_price(properties["product_code"]), properties["rental_price"],
        properties["material"], properties["size"])
    FULL_INVENTORY[properties["product_code"]] = inventory_item

def add_electric_appliance(properties, pricing):
    '''
    Add new Electric Appliance item

    :param properties: electric appliance properties
    :param get_price: function to get latest price
    '''
    inventory_item = electric_appliances.ElectricAppliance(
        properties["product_code"], properties["description"],
        pricing.get_latest_price(properties["product_code"]), properties["rental_price"],
        properties["brand"], properties["voltage"])
    FULL_INVENTORY[properties["product_code"]] = inventory_item

def get_item(item_code):
    '''
    Get item from the inventory list
    '''
    return FULL_INVENTORY.get(item_code)
