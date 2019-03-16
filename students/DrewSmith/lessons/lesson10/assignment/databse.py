'''
HP Norton inventory and customer information database functions
'''


import csv
import logging
import types
import inspect
from datetime import datetime
from pathlib import Path
from multiprocessing.pool import ThreadPool
import config
import pymongo
from pymongo import MongoClient


TIMING_PATH = "timing.csv"

def timefunc(func, counts):
    ''' Time logging decorator times function execution and logs results
    :param func: function to execute and time
    :param counts: reference to counts dictionary to log records affected
    '''
    def fncomposite(*args, **kwargs):
        ''' Timing function called on decorated functions '''
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        # Write to log file
        with open(TIMING_PATH, "a") as file:
            file.write(f"{func.__name__},{(end - start)},{counts[func.__name__]}\n")

        return result
    return fncomposite

class Timer(type):
    ''' Timer meta class for logging standard timing values '''
    def __new__(cls, name, bases, attr):
        ''' Set all external functions with a timefunc decorator '''
        for attr_name, value in attr.items():
            if not attr_name.startswith("_") and (isinstance(value, (types.FunctionType, types.MethodType))):
                attr[attr_name] = timefunc(value, attr["counts"])

        return super(Timer, cls).__new__(cls, name, bases, attr)

class RentalTransactions(metaclass=Timer):
    '''
    Handle transactions in the products MongoDB
    '''

    counts = {}
    def _read_csv(self, directory, file_name):
        ''' Read csv file and yield records
        :param directory: file directory of the csv file
        :param file_name: csv file name
        :yield: dictionary of record values (keys are column names)
        '''
        with open(directory / file_name, 'r') as file:
            csv_file = csv.reader(file)
            columns = next(csv_file, None)
            columns = [column if not column.startswith('ï»¿') else column[3:] for column in columns]
            for record in csv_file:
                yield dict(zip(columns, record))

    def _insert_csv(self, directory, file_name, collection):
        '''
        Read a CSV file and insert records into MongoDB

        :param directory: csv file directory
        :param file_name: csv file name
        :param collection: MongoDB collection to insert the records
        '''
        records = [record for record in self._read_csv(directory, file_name)]
        collection.insert_many(records)
        return len(records)

    def import_product_data(self, directory_name, product_file, customer_file, rentals_file,
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
        directory = Path(directory_name)

        pool = ThreadPool(processes=3)
        counts = [0, 0, 0]
        with connection:
            database = connection.connection.get_database(name=database_name)

            prod = pool.apply_async(self._insert_csv, (directory, product_file, database["products"]))
            cust = pool.apply_async(self._insert_csv, (directory, customer_file, database["customers"]))
            rent = pool.apply_async(self._insert_csv, (directory, rentals_file, database["rentals"]))

            counts[0] = prod.get()
            counts[1] = cust.get()
            counts[2] = rent.get()

            pool.close()
            pool.join()

        self.counts[inspect.currentframe().f_code.co_name] = sum(counts)
        return (tuple(counts), )

    def get_prodcuts_total_record_count(self, connection=None, database_name=None):
        '''
        Get total record count for products, customers, and rentals
        '''
        connection = connection or MongoDBConnection()
        database_name = database_name or config.DATABASE_NAME

        with connection:
            database = connection.connection.get_database(name=database_name)
            result = sum((database[collection].count() for collection in ["products", "customers", "rentals"]))
            self.counts[inspect.currentframe().f_code.co_name] = result
            return result

    def show_available_products(self, connect=None, database_name=None):
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
        self.counts[inspect.currentframe().f_code.co_name] = len(result)
        return result

    def show_rentals(self, product_id, connect=None, database_name=None):
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
        self.counts[inspect.currentframe().f_code.co_name] = len(result)
        return result

class MongoDBConnection:
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        if self.connection is None:
            try:
                self.connection = MongoClient(self.host, self.port)
            except pymongo.errors.InvalidURI as error:
                logging.error(f"MongoDB InvalidURI: {error}")
                raise
            except pymongo.errors.ConfigurationError as error:
                logging.error(f"MongoDB configurationError: {error}")
                raise
            except pymongo.errors.ConnectionFailure as error:
                logging.error(f"MongoDB ConnectionFailure: {error}")
                raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            self.connection.close()
        return False
