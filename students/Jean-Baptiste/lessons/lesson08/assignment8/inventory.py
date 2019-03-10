import csv
import os
from functools import partial


def add_furni(invoice_file="", customer_name="", item_code="", item_description="", item_monthly_price=0.00):
    with open(invoice_file, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        row = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(row)


def test_add_d():
    """
     function to add test data using add_furniture function
    """
    add_furni("invoice_file.csv", "Elisa Miles", "LR04", "Leather Sofa", 25.00)
    add_furni("invoice_file.csv", "Edward Data", "KT78", "Kitchen Table", 10.00)
    add_furni("invoice_file.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17.00)



def single_cust(customer_name, customer_file):
    """
     function to iterate through rental file and add a single customer to the inventory file
    """
    def add_rentals(rental_file):
        with open(customer_file) as rental_csv:
            reader = csv.reader(rental_csv)
            add_item = partial(add_furni, customer_name=customer_name, invoice_file=rental_file)

            for row in reader:
                add_item(item_code=row[1], item_description=row[2], item_monthly_price=row[3])

    return add_rentals


def test_add_susan():
    add_furni("susans_stuff.csv", "Susan Wong", "GH9S", "Lamp", 200.00)
    add_furni("susans_stuff.csv", "Susan Wong", "L4J9", "Table", 4000.00)


if __name__ == "__main__":
    test_add_d()
    test_add_susan()

    susans_result = single_cust("Susan Wong", "susans_stuff.csv")
    susans_result("invoice_file.csv")