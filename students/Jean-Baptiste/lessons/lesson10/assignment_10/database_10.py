"""
Metaclass method use with MongoDB Assignment 10
Author Jean-Baptiste, created on 03-14-2019, Seattle, WA
"""
import os
from timeit import time
import types
import csv
import logging
from pymongo import MongoClient
"""Function that times execution of a passed in function, returns a new function
encapsulating the behavior of the original function"""
class Timer:
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

def timefunc(fn, *args, **kwargs):

    def fncomposite(*args, **kwargs):
        timer = Timer()
        timer.start()
        if 'log_time' in kwargs:
            rt = fn(*args, **kwargs)
            with open("timing.csv", "a") as file:
                file.write(name)
        else:
            logging.error("Errors in time")
        timer.stop()
        print("Executing %s took %s seconds." % (fn.__name__, timer.elapsed))
        return rt
    return fncomposite
"""The 'Timed' metaclass that replaces methods of its classes
with new methods 'timed' by the behavior of the composite function transformer
"""
class Timed(type):

    def __new__(cls, name, bases, attr):
        # replace each function with
        # a new function that is timed
        # run the computation with the provided args and return the computation result
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = timefunc(value)
        return super(Timed, cls).__new__(cls, name, bases, attr)

""" Creates a MongoDB Connection """
#@Timed
class MongoDBConnection():
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None
    def __enter__(self):
        self.connection = pymongo.MongoClient(self.host, self.port)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

""" This is collection class"""
def import_csv(filename):
    with open(filename, newline="") as csvfile:
        dict_list = []
        csv_data = csv.reader(csvfile)
        headers = next(csv_data, None)
        if headers[0].startswith("\ufeff"):
            headers[0] = headers[0][3:]
            for row in csv_data:
                row_dict = {}
                for index, column in enumerate(headers):
                    row_dict[column] = row[index]
                    dict_list.append(row_dict)
    return dict_list
#@Timed
def add_bulk_data(directory_name, filename):
    file_path = os.path.join(directory_name, filename)
    try:
        collection.insert_many(import_csv(file_path), ordered=False)
        return 0
    except pymongo.errors.BulkWriteError as bwe:
        print(bwe.details)
    return len(bwe.details["writeErrors"])

def import_data(db, directory_name, products_file, customers_file, rentals_file):
    products = db["products"]
    products.insert(import_csv(product_file))
    products_errors = add_bulk_data(products, directory_name, products_file)
    customers = db["customers"]
    customers.insert(import_csv(customer_file))
    customers_errors = add_bulk_data(customers, directory_name, customers_file)
    rentals = db["rentals"]
    rentals.insert(import_csv(rentals_file))
    rentals_errors = add_bulk_data(rentals, directory_name, rentals_file)
    record_count = (db.products.count_documents({}), db.customers.count_documents({}), db.rentals.count_documents({}))
    error_count = (products_errors, customers_errors, rentals_errors)
    return record_count, error_count

def show_available_products(db):
    available_products = {}
    for product in db.products.find():
        if int(product["quantity_available"]) > 0:
            product_dict = {"description": product["description"],
                            "product_type": product["product_type"],
                            "quantity_available": product["quantity_available"]}
            available_products[product["product_id"]] = product_dict
    return available_products

def show_rentals(db, product_id):
    customer_info = {}
    for rental in db.rentals.find():
        if rental["product_id"] == product_id:
            customer_id = rental["user_id"]
            customer_record = db.customers.find_one({"user_id": customer_id})
            customer_dict = {"name": customer_record["name"],
                             "address": customer_record["address"],
                             "phone_number": customer_record["phone_number"],
                             "email": customer_record["email"]}
            customer_info[customer_id] = customer_dict
    return customer_info

def clear_data(db):
    db.products.drop()
    db.customers.drop()
    db.rentals.drop()

mongo = MongoDBConnection()
#foo = mdb_collectionClass()

# More tests,
if __name__ == "__main__":
    mongo = MongoDBConnection()
    with mongo:
        print("Opening a MongoDB.\n")
        db = mongo.connection.media
        print("Importing data for products, customers, and rentals.\n")
        import_data(db, "", "products.csv", "customers.csv", "rentals.csv")
        print("Showing available products:")
        print(show_available_products(db))
        print("\nShowing rental information for prd005:")
        print(show_rentals(db, "prd005"))
        print("\nClearing data from database.")
        clear_data(db)
        mdb_collectionClass(collection_name=Timed)
print('products,customers and rentals are loaded in MongoDB, instantiate a mdb_collectionClss instance now')