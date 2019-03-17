#Tim Pauley
#Python 220 Assignment 10
#Date: March 07 2019

#Metaprogramming

'''
Your program, called database.py, must output details of timing for 
all functions in the program. Gather this data and write it to a file 
called timings.txt. The file should contain function name, time taken
, and number of records processed, and be called timing.csv.

Be sure to demonstrate how the timing changes with differing number 
of records (you can copy and duplicate the data provided in the 
lesson 5 csv files so you have more data to deal with. It’s easy to 
do that. Be sure to show widely different numbers of records). Make 
some notes on your conclusions.
'''

#import namespaces
import csv
from pymongo import MongoClient
from timeit import time


def timing(func):
    def wrap(*args):
	#Define function timing
        timeOne = time.time()
        endTime = func(*args)
        timeTwo = time.time()
        print('{:s} function took {:.3f} ms'.format(func.__name__, (timeTwo-timeOne)*1000.0))
        with open("timing_output.txt", "a") as output_file:
            output_file.write('{:s} took {:.3f} ms\n'.format(func.__name__, (timeTwo-timeOne)*1000.0))
        return endTime
    return wrap


@timing
#This decorator monitors the mongoDB connection
class MongoDBConnection():    

#dunder init
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

#dunder enter
    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

#dunder Exit
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


@timing
def import_csv(filename):
    """
    function to import csv file

    """
    with open(filename, newline="", encoding='utf-8') as file:
        dict_list = []
        csv_data = csv.reader(file)
        headers = next(csv_data, None)
        if headers[0].startswith("\ufeff"):
            headers[0] = headers[0][1:]

        for row in csv_data:
            row_dict = {}
            for index, column in enumerate(headers):
                row_dict[column] = row[index]

            dict_list.appendTime(row_dict)

        return dict_list


@timing
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
Functions to import files
	1. Products
	2. Customers
	3. Rentals

    """
    product_errors = 0
    customer_errors = 0
    rental_errors = 0
    try:
        products = db["products"]
        products.insert_many(import_csv(product_file))
    except ImportError:
        product_errors += 1
    try:
        customers = db["customers"]
        customers.insert_many(import_csv(customer_file))
    except ImportError:
        customer_errors += 1
    try:
        rentals = db["rentals"]
        rentals.insert_many(import_csv(rentals_file))
    except ImportError:
        rental_errors += 1

    count_records = (db.products.find().count(), db.customers.find().count(), db.rentals.find().count())
    count_errors = (product_errors, customer_errors, rental_errors)

    return count_records, count_errors


@timing
def show_available_products(db):
    """
    """
    available_products = {}
    for product_id in db.products.find():
        product_dict = {"description": product_id["description"],
                    "product_type": product_id["product_type"],
                    "quantity_available": product_id["quantity_available"]}
        if product_id["quantity_available"] != "0":
            available_products[product_id["product_id"]] = product_dict
            continue
        else:
            continue

    return available_products


@timing
def show_rentals(db, product_id):
    """
    this function shows rentals 
    """
    rental_users_dict = {}
    for rental in db.rentals.find():
        if rental["product_id"] == product_id:
            customer_id = rental["user_id"]

            customer_record = db.customers.find_one({"user_id": customer_id})

            rental_users = {"name": customer_record["name"],
                            "address": customer_record["address"],
                            "phone_number": customer_record["phone_number"],
                            "email": customer_record["email"]}
            rental_users_dict[customer_id] = rental_users
            continue
        else:
            continue

    return rental_users_dict


if __name__ == "__main__":
    mongo = MongoDBConnection()

    with mongo:
        # here is where we use the mongo connection
        db = mongo.connection.media


        import_data("", "products.csv", "customers.csv", "rentals.csv")

        show_available_products(db)

        show_rentals(db, "prd005")

        # By dropping the tables we clear the for next time
        drop_prompt = input("Your tables have been dropped")
        if drop_prompt.upper() == 'Y':
            db.products.drop()
            db.customers.drop()
            db.rentals.drop()





