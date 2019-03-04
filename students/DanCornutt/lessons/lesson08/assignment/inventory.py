#!/usr/bin/env python3
"""HW8 Functional Methods"""
import os.path
import csv
from functools import partial


def add_furniture(
    invoice_file, customer_name, item_code, item_description,
    item_monthly_price
):
    """
    This function will create invoice_file if it doesn’t\
    exist or append a new line to it if it does.
        param1: invoice file
        param2: customer name
        param3: item code
        param4: item description
        param5: item monthly price
    """
    if os.path.isfile(invoice_file):
        open_type = 'a'
    else:
        open_type = 'w'
    with open(invoice_file, open_type, newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([customer_name, item_code, item_description,
                         item_monthly_price])


def single_customer(customer_name, invoice_file):
    """
    Returns a function that takes one parameter, rental_items
    param1: customer name
    param2: invoice file
    """

    # customer_func = partial(add_furniture, invoice_file=file,
    #                         customer_name=name)
    def cust_load_func(rentals):
        with open(rentals, 'r') as csv_f:
            reader = csv.reader(csv_f, delimiter=',')
            for row in reader:
                add_furniture(invoice_file, customer_name, row[0], row[1],
                              row[2])
    return cust_load_func
