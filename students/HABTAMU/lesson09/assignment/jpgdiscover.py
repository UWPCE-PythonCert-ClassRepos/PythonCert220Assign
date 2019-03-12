# """ Recursively go through directories looking for pngs """
import functools
import sys
import csv
import os
import pathlib
import logging
import argparse
from pymongo import MongoClient

DATABASE_NAME = "inventory"

class MongoDBConnection(object):
    """MongoDB Connection"""

    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def create_logger():
    """
    Creates a logging object and returns it, parse logging argument selective, by using decorators.
    conditional logging with single command line variable which can turn logging on or off for decorated classes or functions.
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    file_handler = logging.FileHandler("exception_err.log")

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(file_handler)

    parser = argparse.ArgumentParser(description="enable logging")
    parser.add_argument('-d', '--debug', help='enable debug logging', required=False, default=0)

    return logger


def exception(function):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in  "
            err += function.__name__
            logger.exception(err)

            # re-raise the exception
            raise
    return wrapper


@exception
def import_data(directory, product_file, customer_file, rental_file, connection=None, database_name=None):
    mongo = MongoDBConnection()
    database_name = database_name or DATABASE_NAME
    directory = pathlib.Path(directory)

    with mongo:
        db = mongo.connection.get_database(name=database_name)

        files = [product_file, customer_file, rental_file]
        count = []
        error = []
        for file in files:
            with open(os.path.join(directory, file)) as csv_file:
                csv_dict = csv.DictReader(csv_file, delimiter=',')
                collection = db[file.replace(".csv", "")]
                try:
                    result = collection.insert_many(csv_dict)
                    count.append(len(result.inserted_ids))
                    error.append(0)
                except Exception as e:
                    error.append(1)
                    logging.error(e)
    return (tuple(count), tuple(error))


@exception
def png_discovery(directory, png_paths=None):
    if png_paths is None:
        png_paths = []
    current_list = [directory, []]
    for filename in os.listdir(directory):
        path_join = os.path.join(directory, filename)
        if os.path.isdir(path_join):
            png_discovery(path_join, png_paths)
        if filename.endswith(".png"):
            current_list[1].append(path_join)

    if current_list[1]:
        png_paths.extend(path_join)
        
    return current_list


if __name__ == '__main__':
    directory = os.getcwd()
    product_file = 'products.csv'
    customer_file = 'customers.csv'
    rental_file = 'rentals.csv'
    database_name = 'inventory'

    import_data(directory, product_file, customer_file,
                rental_file, connection=None, database_name=None)

    png_discovery(directory)
