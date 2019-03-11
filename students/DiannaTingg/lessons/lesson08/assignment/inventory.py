"""
Lesson 08 Assignment
Functional Programming
"""

import csv
from functools import partial

# pylint: disable-msg=line-too-long
# pylint: disable-msg=invalid-name


def add_furniture(invoice_file="", customer_name="", item_code="", item_description="", item_monthly_price=""):
    """
    Updates the master invoice file which lists which furniture is rented to which customer.
    Will create a new file if one doesn't already exist.
    :param invoice_file: master csv file
    :param customer_name: customer name
    :param item_code: item code
    :param item_description: item description
    :param item_monthly_price: item monthly price
    """

    with open(invoice_file, "a+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(row)


def add_test_data():
    """
    Adds test data to the master invoice file.
    """
    add_furniture("invoice_file.csv", "Elisa Miles", "LR04", "Leather Sofa", "25.00")
    add_furniture("invoice_file.csv", "Edward Data", "KT78", "Kitchen Table", "10.00")
    add_furniture("invoice_file.csv", "Alex Gonzales", "BR02", "Queen Mattress", "17.00")


def single_customer(customer_name, invoice_file):
    """
    Bulk processes a list of items that have been rented to a single customer.
    :param customer_name: customer name
    :param invoice_file: master invoice csv file
    :return: function that iterates through rental_items and adds each item to the master invoice_file.
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

    test_customer = single_customer("Susan Wong", "invoice_file.csv")
    test_customer("test_items.csv")
