'''
HP Norton inventory and customer information database functions
'''


import csv
import pathlib
from pymongo import MongoClient
import assignment.config as config


class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file,
                connection=None, database_name=None):
    '''
    Imports data from 3 files an inserts product, customer and rental data

    :param directory_name: directory where data files are stored
    :param product_file: file name with product data
    :param customer_file: file name with customer data
    :param rentals_file: file name with rentals data
    :param connection: DB connection for data inserts
    :param database_name: Database to use for the query,
        or None to use production default
    '''
    connection = connection or MongoDBConnection()
    database_name = database_name or config.DATABASE_NAME
    directory = pathlib.Path(directory_name)

    errors = [0, 0, 0]
    counts = [0, 0, 0]
    with connection:
        database = connection.connection.get_database(name=database_name)

        with open(directory / product_file, 'r') as file:
            csv_file = csv.DictReader(file, fieldnames=("product_id",
                                                        "description",
                                                        "product_type",
                                                        "quantity_available"))
            records = list()
            for index, record in enumerate(csv_file):
                if index == 0:
                    continue
                try:
                    record["quantity_available"] = int(record["quantity_available"])
                except ValueError:
                    errors[0] += 1
                else:
                    records.append(record)
            counts[0] = len(records)
            database["products"].insert_many(records)

        with open(directory / customer_file, 'r') as file:
            csv_file = csv.DictReader(file, fieldnames=("user_id",
                                                        "name",
                                                        "address",
                                                        "zip_code",
                                                        "phone_number",
                                                        "email"))
            records = [record for index, record in enumerate(csv_file) if index > 0]
            counts[1] = len(records)
            database["customers"].insert_many(records)

        with open(directory / rentals_file, 'r') as file:
            csv_file = csv.DictReader(file, fieldnames=("product_id", "user_id"))
            records = [record for index, record in enumerate(csv_file) if index > 0]
            counts[2] = len(records)
            database["rentals"].insert_many(records)

    return (tuple(counts), tuple(errors))

def show_available_products(connect=None, database_name=None):
    '''
    Returns all products that are available to rent

    :param connect: connection object, or None to use default
    :param database_name: Database to use for the query,
        or None to use production default
    '''
    connect = connect or MongoDBConnection()
    database_name = database_name or config.DATABASE_NAME
    with connect:
        database = connect.connection.get_database(name=database_name)
        products = database["products"]
        result = dict()
        for record in products.find({"quantity_available": {"$gt": 0}}):
            result[record["product_id"]] = {
                "description": record["description"],
                "product_type": record["product_type"],
                "quantity_available": record["quantity_available"]
            }
    return result

def show_rentals(product_id, connect=None, database_name=None):
    '''
    Returns all users that are renting a specific product_id

    :param product_id: product_id to search for
    :param connect: connection object, or None to use default
    :param database_name: Database to use for the query,
        or None to use production default
    '''
    connect = connect or MongoDBConnection()
    database_name = database_name or config.DATABASE_NAME
    with connect:
        database = connect.connection.get_database(name=database_name)
        rentals = database["rentals"]
        customers = database["customers"]
        result = dict()

        user_ids = [rental["user_id"] for rental in rentals.find({"product_id": product_id})]

        for record in customers.find({"user_id": {"$in": user_ids}}):
            result[record["user_id"]] = {
                "name": record["name"],
                "address": record["address"],
                "phone_number": record["phone_number"],
                "email": record["email"]
            }
    return result
