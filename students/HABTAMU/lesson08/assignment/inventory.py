"""
Assignment 8 Norton Furniture Assignment
Inventory Management System
"""
import csv
from functools import partial

def add_furniture(invoice_file,
                  customer_name,
                  item_code,
                  item_description,
                  item_monthly_price):
    """
    This will create invoice_file if it doesn’t exist or append a new line to it if it does. 
    :param invoice_file
    :param customer_name
    :param item_code
    :parm item_description
    :param item_monthly_price
    """

    with open(invoice_file, 'a+') as csvfile:
        csvfile.write(f'{customer_name}, {item_code}, {item_description}, {float(item_monthly_price):.2f}\n')


def single_customer(customer_name, invoice_file):
    """
    This will load individual customers rental.
    :param invoice_file
    :param customer_name
    """
    customer_furniture = partial(add_furniture, invoice_file=invoice_file, customer_name=customer_name)

    FIELD_NAME = ['customer_name', 'item_code', 'item_description', 'item_monthly_price']

    def add_rentals(rental_items):
        ''' 
        Add rentals info file for individual customer 
        :param rental_items customer rental item information
        '''
        nonlocal FIELD_NAME

        with open(rental_items, 'r') as rental_file:
            reader = csv.DictReader(rental_file, fieldnames=('item_code', 'item_description', 'item_monthly_price'))
            for item in reader:
                customer_furniture(**item)

    return add_rentals

if __name__ == '__main__':
    filename = 'invoice_file.csv'
    rental_items = 'rental_items.csv'
    FIELD_NAME = ['customer_name', 'item_code',
                  'item_description', 'item_monthly_price']
    
    add_furniture(filename, "Lisa Miles", "PLR04", "Leather", "125.00")
    add_furniture("invoice_file.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("invoice_file.csv", "Alex Gonzales", "QM90", "Queen Mattress", 17)

    create_invoice = single_customer("Cho Wong", "Cho_invoice.csv")
    create_invoice(rental_items)

