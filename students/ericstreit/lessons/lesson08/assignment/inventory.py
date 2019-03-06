"""
#Lesson08
#Functional Technique Assignment ##
"""

#!/usr/bin/env python3
#import stuff here
from functools import partial
import logging
import csv
import unittest
#global variables here
logging.basicConfig(level=logging.DEBUG)
#define function
def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """
    This function will create invoice_file if it doesn’t exist or append a
    new line to it if it does.

    :param arg1: invoice file to create or append
    :param arg2: the customer name
    :param arg2: the item code
    :param arg2: the item description
    :param arg2: the monthly price of the item
    """

    func_input = [[customer_name, item_code, item_description,
                  item_monthly_price]]

    with open(invoice_file, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerows(func_input)
        # OK this works just add notes and stuff

def single_customer(customer_name):
    """
    This function works with closures.

    :param arg1: the customer name
    """

    def single_customer_lookup(new_invoice_file):
    # creates new invoice for specific customer
        with open('invoice01.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if customer_name in row:
                    # convert the iteration into a list object in order to send
                    # back into a csv
                    data = [row]
                    with open(new_invoice_file, 'a') as csvfile2:
                        writer = csv.writer(csvfile2, delimiter=',', quotechar='"')
                        writer.writerows(data)
        return(f'Invoice {new_invoice_file} created for {customer_name}.')
        
    return single_customer_lookup

# create closure with functools partial
def single_customer_partial(customer_name, new_invoice_file = 'generic_invoice.csv'):
        """
        This function is for working with a partial closure

        :param arg1: the customer name
        :param arg2: the invoice file to create, defaults to generic_invoice.csv
        """

        with open('invoice01.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if customer_name in row:
                    # convert the iteration into a list object in order to send
                    # back into a csv
                    data = [row]
                    with open(new_invoice_file, 'a') as csvfile2:
                        writer = csv.writer(csvfile2, delimiter=',', quotechar='"')
                        writer.writerows(data)
        # I think I need to return something here?
        return(f'Invoice {new_invoice_file} created for {customer_name}.')


#for testing
if __name__=="__main__":
    add_furniture('invoice01.csv', 'King Kong', 'L504', 'Leather Sofa', 25.00)
    add_furniture('invoice01.csv', 'Godzilla', 'KT78', 'Kitchen Table', 10.00)
    add_furniture('invoice01.csv', 'Mothra', 'BZ06', 'Bug Zapper', 17.00)
    add_furniture('invoice01.csv', 'Mechazilla', 'OC66', 'Oil Can', 5.00)
    add_furniture('invoice01.csv', 'Monster X', 'FS99', 'Fondue Set', 8.00)
    add_furniture('invoice01.csv', 'King Kong', 'FB04', 'Fruit Basket', 100.00)
    add_furniture('invoice01.csv', 'Godzilla', 'AA48', 'Antacid Basket', 25.00)
    add_furniture('invoice01.csv', 'Mothra', 'CB10', 'Clothes Basket', 33.00)
    add_furniture('invoice01.csv', 'Mechazilla', 'SP55', 'Spare Parts Basket', 147.00)
    add_furniture('invoice01.csv', 'Monster X', 'HB94', 'Hat Basket', 16.00)

    #assertions
    king_kong = partial(single_customer_partial, new_invoice_file =
                        'king_kong_invoice.csv')
    assert king_kong('King Kong') == 'Invoice king_kong_invoice.csv created for King Kong.'
