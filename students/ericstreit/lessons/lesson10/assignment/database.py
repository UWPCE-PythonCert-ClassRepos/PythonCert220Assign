"""
#Lesson10
Metaprogramming Timing
Special Thanks to:
https://www.blog.pythonlibrary.org/2016/05/24/python-101-an-intro-to-benchmarking-your-code/
"""

#!/usr/bin/env python3
#import stuff here
from pymongo import MongoClient
import logging
import csv
import time


#global variables here
logging.basicConfig(level=logging.ERROR)
#define function and classes

def timerfunc(func):
    """ a timer decorator """

    def function_timer(*args, **kwargs):
        """ nested function for timing functions """

        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        print(f' The runtime for {func.__name__} took {runtime} seconds to complete')
        return value
    return function_timer

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        print(f"Establishing a connection to {self.host} on port {self.port}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"closing the connection to {self.host}!")
        self.connection.close()



@timerfunc
def import_data(products_file, customers_file, rentals_file):
# def import_data(directory_name, products_file, customers_file, rentals_file):
    """
    This function takes a directory name three csv files as input, one with
    product data, one with customer data and the third one with rentals data and
    creates and populates a new MongoDB database with the these data.
    It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a
    count of any errors that occurred, in the same order.

    Imports CSV data into a MongoDB.

    :param arg1: the name of the products csv file
    :param arg2: the name of the customers csv file
    :param arg3: the name of the rentals csv file
    """
    mongo = MongoDBConnection()

    with mongo:
        #connect to Mongo
        db = mongo.connection.hp_norton

        #name the first collection we will work on
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        record_count = 0
        error_count = 0

        #open the first csv to import into the db
        #could this be made its own function?? probably!
        try:
            with open(products_file) as products_csv, \
                 open(customers_file) as customers_csv, \
                 open(rentals_file) as rentals_csv:
                products_contents = csv.reader(products_csv, delimiter=',', quotechar='"')
                customers_contents = csv.reader(customers_csv, delimiter=',', quotechar='"')
                rentals_contents = csv.reader(rentals_csv, delimiter=',', quotechar='"')

                 #this probably won't work, we need to change the data to a dict
                 # yup! you were right!
                 # CONVERT ROW DATA TO DICT

                for row in products_contents:
                     # this could be made into a func couldn't it?
                    logging.info(f'IMPORTING PRODUCTS DATA')
                    convert_to_dict = {'product_id': row[0],
                                       'description': row[1],
                                       'product_type': row[2],
                                       'quantity_available': row[3]}
                    try:
                        result = products.insert_one(convert_to_dict)
                        record_count += 1
                    except Exception as e:
                        logging.error(f'Error adding {convert_to_dict} to the products collection!')
                        error_count += 1
                    # who needs comments when your logging explains it all LOL
                    logging.info(f'Adding {convert_to_dict} to the products collection')
                for row in customers_contents:
                    logging.info(f'IMPORTING CUSTOMERS DATA')
                    convert_to_dict = {'user_id': row[0],
                                       'name': row[1],
                                       'address': row[2],
                                       'zip_code': row[3],
                                       'phone_number': row[4],
                                       'email': row[5]}
                    try:
                        result = customers.insert_one(convert_to_dict)
                        logging.info(f'Adding {convert_to_dict} to the customers collection')
                        record_count += 1
                    except Exception as e:
                        logging.error(f'Error adding {convert_to_dict} to the customers collection!')
                        error_count += 1
                for row in rentals_contents:
                    logging.info(f'IMPORTING RENTALS DATA')
                    convert_to_dict = {'product_id': row[0],
                                       'user_id': row[1]}
                    try:
                        result = rentals.insert_one(convert_to_dict)
                        logging.info(f'Adding {convert_to_dict} to the rentals collection')
                        record_count += 1
                    except Exception as e:
                        logging.error(f'Error adding {convert_to_dict} to the customers collection!')
                        error_count += 1

            print(f' total number of records added: {record_count}')
            print(f' total number of documents in collection: {products.collection.estimated_data_count()}')
        except Exception as e:
            logging.error(f'Hm, we had an error here?')
            logging.error(e)

        print(f' the number of records are: {db.products.count()}')
        return (record_count, error_count)


@timerfunc
def show_available_products():
    """
    Returns a Python dictionary of products listed as available with
    the following fields:

    product_id.
    description.
    product_type.
    quantity_available.
    """
    mongo = MongoDBConnection()

    with mongo:
        #connect to Mongo
        db = mongo.connection.hp_norton

        #name the first collection we will work on
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        for name in products.find():
            logging.debug(f"{name.get('product_id')} : {name.get('quantity_available')}")
            try:
                if int(name.get('quantity_available')) > 0:
                    print(f"{name.get('product_id')}: {name.get('description')} is available!")
            except ValueError as e:
                logging.debug(f"skipping {name.get('product_id')} due to error")
                logging.error(e)


@timerfunc
def show_rentals(product_id):
    """
    Returns a Python dictionary with the following user information from
    users that have rented products matching product_id:

    user_id.
    name.
    address.
    phone_number.
    email.

    :param arg1: The product_id to search for
    """
    # gosh, I'm repeating myself a lot here with these Mongo commands. could
    # be simplified into its own function, yes??
    mongo = MongoDBConnection()

    with mongo:
        #connect to Mongo
        db = mongo.connection.hp_norton

        #the collections we will be using
        customers = db["customers"]
        rentals = db["rentals"]
        customer_list = []
        customer_dict ={}
        for rented_item in rentals.find():
            logging.debug(f"Does {product_id} match {rented_item.get('product_id')}?")
            try:
                if rented_item.get('product_id') == product_id:
                    logging.debug(f'found a match!')
                    customer_list.append(rented_item.get('user_id'))
                    logging.debug(f"Adding {rented_item.get('user_id')} to list")
            except ValueError as e:
                logging.debug(f"skipping {rented_item.get('product_id')} due to error")
                logging.error(e)

        for name in customers.find():
            logging.debug(f"comparing found user id to the customer list")
            logging.debug(f"looking for {name.get('user_id')} in {customer_list}")
            try:
                if name.get('user_id') in customer_list:
                    logging.debug(f"found {name.get('name')} in the list!")
                    customer_dict[name.get('user_id')] = [name.get('user_id'),
                                                          name.get('name'),
                                                          name.get('address'),
                                                          name.get('phone_number'),
                                                          name.get('email')]
            except ValueError as e:
                logging.debug(f"skipping {name.get('name')} due to error")
                logging.error(e)
        return customer_dict

# def record_count(collection):

#for testing
if __name__=="__main__":
    import_data('products.csv', 'customers.csv', 'rentals.csv')
