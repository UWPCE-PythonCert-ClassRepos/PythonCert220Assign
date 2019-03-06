"""
    - Create funciton that reads individual csv file
"""

import csv
from functools import partial


def add_furniture(invoice_file='', customer_name='', item_code='', item_description='', item_monthly_price=0.00):
    """
        Create a blank csv file called invoice_file if does not exist
    """
    with open(invoice_file, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        row = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(row)


def add_test_data():
    """
        Adds test data to blank csv file using add_furniture function
    """
    add_furniture('invoice_file.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25.00)
    add_furniture('invoice_file.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10.00)
    add_furniture('invoice_file.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)


def single_customer(customer_name, customer_file):
    """
        Input parameters: Can use a partial using customer_name, invoice_file..
    """

    def add_rentals(rental_file):
        with open(customer_file) as rental_csv:
            reader = csv.reader(rental_csv)

            add_item = partial(add_furniture, customer_name=customer_name, invoice_file=rental_file)

            for row in reader:
                add_item(customer_name=row[0], item_code=row[1], item_description=row[2], item_monthly_price=row[3])

    return add_rentals


def add_susan_test():
    """
        Creates csv file with just Susans furniture using add_susan_test function
    """
    add_furniture("susans_furniture.csv", "Susan Wong", "ZU8L", "Coffee Table", 444.44)
    add_furniture("susans_furniture.csv", "Susan Wong", "RS11L", "King Size Bed", 2000.00)
    add_furniture("susans_furniture.csv", "Susan Wong", "23RS", "Lamp", 50.00)


if __name__ == "__main__":
    add_test_data()
    add_susan_test()

    susans_stuff = single_customer("Susan Wong", "susans_furniture.csv")
    # Adds Susans stuff to invoice_file
    susans_stuff("invoice_file.csv")
