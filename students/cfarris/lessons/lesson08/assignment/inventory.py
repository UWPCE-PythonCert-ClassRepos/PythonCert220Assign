#!/usr/bin/env Python3

'''
lesson 8 work with closures

Pylint is complaining about passing invoice and customer-name in partial.
From my brief research, this appears to be a bug with pylint. 
'''

from functools import partial
import csv





def add_furniture(item_code="", item_desc="",
                  item_monthly_price="",
                  invoice_file="",
                  customer_name=""):
    """
    add_furniture creates an invoice file (or appends if exists)
    File name is parameter,the rest of the parameters go into invoice_file
    """
    with open(invoice_file, 'a+') as i_file:
        i_file.write(f'{customer_name}, {item_code}, {item_desc}, {item_monthly_price}\n')
    print("completed")


def single_customer(customer_name, invoice_file):
    """
    single_customer returns a function that takes one parameter(rental_items)
    it returns a function that will iterate through rental_items
    and add each item to the invoice_file.
    """
    def add_cust_rentals_to_invoice(client_items):
        with open(client_items, 'r') as client_i:
            csv_reader = csv.reader(client_i, delimiter=',')
            store_increment = 0
            add_rentals = partial(add_furniture,
                                  invoice_file=invoice_file,
                                  customer_name=customer_name,)

            for row in csv_reader:
                store_increment = store_increment + 1
                add_rentals(row[0],
                            row[1],
                            row[2])

    return add_cust_rentals_to_invoice


if __name__ == '__main__':
    add_furniture('LR04', 'Leather Sofa', 25.00, "invoice_file.csv", 'Elisa Miles')
    add_furniture('KT78', 'Kitchen Table', 10.00, "invoice_file.csv", 'Edward Data')
    add_furniture('BR02', 'Queen Mattress', 17.00, "invoice_file.csv", 'Alex Gonzales')
    rentals_to_invoice = single_customer('Elisa Miles', "invoice_file.csv")
    rentals_to_invoice('client_items.csv')
