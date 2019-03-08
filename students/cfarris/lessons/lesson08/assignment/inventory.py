#!/usr/bin/env Python3


############
#lesson 8 
#######

from functools import partial
import os.path
import csv


def add_furniture(item_code, item_desc, item_monthly_price,invoice_file, customer_name, ):
    """
    add_furniture creates an invoice file (or appends if exists)
    File name is parameter, the rest of the parameters go into invoice_file

    use the add_furniture from before...
    so, from one file, get the code, description and item monthly price
    """
    #if os.path.exists(file_name): # open, and append a new line with the customer name and item code.
    with open(invoice_file, 'a+') as invoice_file:
        invoice_file.write(f'{customer_name}, {item_code}, {item_desc}, {item_monthly_price}\n')
    print("completed")
   
    #pass



def single_customer(customer_name, invoice_file):
    """
    single_customer returns a function that takes one parameter(rental_items)
    Single customer returns a function that will iterate through rental_items
    and add each item to the invoice_file.
    """
    def add_cust_rentals_to_invoice(client_items):
        with open(client_items, 'r') as client_items:
            csv_reader = csv.reader(client_items, delimiter=',')
            store_increment = 0
            for row in csv_reader:
                store_increment = store_increment +1
                partial(add_furniture,row[0], row[1],row[2],invoice_file=invoice_file, customer_name=customer_name,)
    return add_cust_rentals_to_invoice


if __name__ == '__main__':
    invoice_file = "invoice_file.csv"
    add_furniture('LR04','Leather Sofa', 25.00,invoice_file, 'Elisa Miles')
    add_furniture('KT78','Kitchen Table',10.00,invoice_file, 'Edward Data')
    add_furniture('BR02','Queen Mattress',17.00,invoice_file, 'Alex Gonzales')
    rentals_to_invoice = single_customer('Elisa Miles', invoice_file)
    rentals_to_invoice('client_items.csv')
