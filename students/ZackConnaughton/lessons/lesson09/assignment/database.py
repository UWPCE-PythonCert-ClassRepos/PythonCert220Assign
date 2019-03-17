"""
creates database with customer info and product info
"""

import argparse
import csv
import sys
import logging
import datetime
from pymongo import MongoClient

def disable_logging(funct):
    def return_function(*args, **kwargs):
        logger = logging.getLogger()
        if ARG_PARSE.disable:
            logger.disabled = True
        funct(*args, **kwargs)
        logger.disabled = False
    return return_function


def parse_cmd_arguments():
    """
    arg parser to determine if logging should be disabled from decorated functions
    """
    parser = argparse.ArgumentParser(description='Disable logging.')
    parser.add_argument('-d', '--disable', help='disable logging for @disable_logging decorated functions', action='store_true')
    return parser.parse_args()


def set_logging():
    """
    sets logging level
    """

    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'

    formatter = logging.Formatter(log_format)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return None


class MongoDBConnection():
    """MongoDB Connection"""

    @disable_logging
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None
        logging.debug("Initializing Mongo Connection")

    @disable_logging
    def __enter__(self):
        logging.debug("Enterting context manager for mongo connection")
        self.connection = MongoClient(self.host, self.port)
        return self

    @disable_logging
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.debug("Leaving context manager for mongo connection")
        self.connection.close()

def show_available_products():
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        output_dict = list(database.products.find({'quantity_available': {'$gt':'0'}}, {"_id": 0}))

        print(output_dict)
        return(output_dict)

def show_rentals(product_id):
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        output_list = list(database.rentals.aggregate([
            {'$match':
                {'product_id': product_id}},
            {'$lookup':
                {'from': "customers",
                'localField': "user_id",
                'foreignField': "user_id",
                'as': "cust"}},
            {'$project':
                {'_id': 0,
                'user_id': 1,
                'name': '$cust.name',
                'address': '$cust.address',
                'phone_number': '$cust.phone_number',
                'email': '$cust.email'}}

                ]))
        return(output_list)


def print_mdb_collection(collection_name):
    for doc in collection_name.find({}):
        print(doc)

def csv_list(file):
    return_list = []
    with open('sample_csv_files/' + file, encoding='utf-8-sig') as csv_file:
        file_input = csv.DictReader(csv_file)
        for row in file_input:
            return_list.append(row)
    return return_list


def drop_database_data(collection):
    logging.debug("Dropping data collections")
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        database[collection].drop()
        return True
        #add something here if it cant be found


def import_data(dir_name, product_csv, customer_csv, rental_csv):
    logging.debug("Importing info")
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        #Refactor at some point - reduce repetition
        product_collection = database['products']
        product_list = csv_list(product_csv)
        product_list_count = len(product_list)
        product_list_errors = 0
        for item in product_list:
            try:
                product_collection.insert_one(item)
            except:
                product_list_errors += 1

        customer_collection = database['customers']
        customer_list = csv_list(customer_csv)
        customer_list_count = len(customer_list)
        customer_list_errors = 0
        for item in customer_list:
            try:
                customer_collection.insert_one(item)
            except:
                customer_list_errors += 1

        rental_collection = database['rentals']
        rental_list = csv_list(rental_csv)
        rental_list_count = len(rental_list)
        rental_list_errors = 0
        for item in rental_list:
            try:
                rental_collection.insert_one(item)
            except:
                rental_list_errors += 1

        import_data_added = (product_list_count - product_list_errors,
                             customer_list_count - customer_list_errors,
                             rental_list_count - rental_list_errors)
        import_data_errors = (product_list_errors,
                              customer_list_errors,
                              rental_list_errors)

        return import_data_added, import_data_errors

if __name__ == '__main__':
    ARG_PARSE = parse_cmd_arguments()
    set_logging()
    import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    drop_data_response = input("Drop data?")
    if drop_data_response.upper() == 'Y':
        drop_database_data('products')
        drop_database_data('customers')
        drop_database_data('rentals')
        print("Data Dropped")
    #show_available_products()
    show_rentals('prd002')
