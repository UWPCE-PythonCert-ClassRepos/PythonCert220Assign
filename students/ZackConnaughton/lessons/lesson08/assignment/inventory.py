"""
Assignment 8 Norton Furniture Assignment
Inventory Management System
"""
import csv
from functools import partial

def add_furniture(output_file, *args):
    """
    creates or appends to an invoice file the arguments passed
    """
    with open(output_file, "a+") as file:
        str_args = [str(item) for item in args]
        file.write(",".join(str_args))
        file.write("\n")

def rental_items(rental_file, customer="", output_file=""):
    with open(rental_file) as file:
        reader = csv.reader(file)
        with open(output_file, "a+") as output_file:
            for row in reader:
                if row[0] == customer:
                    output_file.write(",".join(row))
                    output_file.write("\n")


def single_customer(customer, output_file):
    return partial(rental_items, customer=customer, output_file=output_file)
