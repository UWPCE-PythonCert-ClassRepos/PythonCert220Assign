#Tim Pauley
#Python 220a Assignment 08
#Date March 02 2019

#Functional Techniques

'''
Assignment
HP Norton has been using comma-separated files (.CSV extension) to keep 
track of which furniture they have rented out to which customer. 
This is currently generated from a spreadsheet.

Your Project Manager wants you to get the spreadsheet program out of 
the equation by creating a Python function that will create and update 
an inventory CSV file with all the information that is currently entered 
through the spreadsheet program. You have decided to use closures and 
currying to develop the necessary functionality.

You will also develop functionality to to bulk-process a list of items, 
coming from a separate CSV file, that have been rented out to a 
single customer. This functionality will thus update the inventory list 
by adding that customer’s rentals.

To summarize: 

1. You will create a program to initially create, and subsequently update
, a CSV file that lists which furniture is rented to which customer 
(to replace use of the spreadsheet mentioned above). 

2. You will create additionally functionality that will load individual 
ustomers rentals.

TO DO:

1 Create a python module called inventory.py. This file will contain 
all the functions used for this assignment.

Create a function called add_furniture that takes the following input 
parameters:
invoice_file
customer_name
item_code
item_description
item_monthly_price

*This function will create invoice_file if it doesn’t exist or append a 
ew line to it if it does. After adding a few items to the same file
, the file created by add_furniture should look something like this:

Elisa Miles,LR04,Leather Sofa,25.00
Edward Data,KT78,Kitchen Table,10.00
Alex Gonzales,BR02,Queen Mattress,17.00
You can create a starter file in this format for testing, or you can 
have your add function do it.

Create a function called single_customer:
Input parameters: customer_name, invoice_file.
Output: Returns a function that takes one parameter, rental_items.
single_customer needs to use functools.partial and closures, in order
 to return a function that will iterate through rental_items and add 
 each item to invoice_file.
'''

import csv
from functools import partial



def add_furniture(invoice_file="", customer_name="", item_code="", item_description="", item_monthly_price=""):
    """
    Master invoice update
    """

    with open(invoice_file, "a+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(row)


def add_test_data():
    """
    Test 
    """
    add_furniture("invoice_file.csv", "Tim Pauley", "7000", "Surfboard", "50.00")
    add_furniture("invoice_file.csv", "Mary Kelly", "DG32", "Skateboard", "100.00")
    add_furniture("invoice_file.csv", "Ryan Pauley", "G692", "Snowboard", "7000")


def single_customer(customer_name, invoice_file):
    """
    This is my bulk process function
    """

    def add_rentals(rental_items):
        with open(rental_items) as rental_csv:
            reader = csv.reader(rental_csv)

            add_item = partial(add_furniture, invoice_file=invoice_file, customer_name=customer_name)

            for row in reader:
                add_item(item_code=row[0], item_description=row[1], item_monthly_price=row[2])

    return add_rentals


if __name__ == "__main__":
    add_test_data()

    test_customer = single_customer("Tim Pauley", "invoice_file.csv")
    test_customer("test_items.csv")
