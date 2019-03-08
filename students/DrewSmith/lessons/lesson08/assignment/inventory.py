'''
Add funiture to inventory files
'''

from functools import partial
import csv

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''
    Add a single entry for a customer inventory item
    :param invoice_file: path to invoice file
    :param customer_name: customer name for rental
    :param item_code: furniture item code
    :parm item_description: furniture item description
    :param item_monthly_price: rental price
    '''
    with open(invoice_file, 'a') as file:
        file.write(f"{customer_name},{item_code},{item_description},{item_monthly_price}\n")


def single_customer(invoice_file, customer_name):
    '''
    Closure for a single customer and file
    :param invoice_file: File path for the invoice storage location
    :param customer_name: customer name
    '''
    add_customer_furniture = partial(add_furniture,
                                     invoice_file=invoice_file, customer_name=customer_name)

    def add_rental_items(rental_items):
        '''
        Adds the rental_items for the customer
        :param rental_items: path to a file with the rental information for this customer
        '''
        with open(rental_items, 'r') as file:
            csv_file = csv.DictReader(file, fieldnames=('item_code',
                                                        'item_description',
                                                        'item_monthly_price'))
            for record in csv_file:
                add_customer_furniture(**record)

    return add_rental_items
