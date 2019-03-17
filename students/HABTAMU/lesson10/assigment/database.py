
""" 
A metaprogramming program to add timing information to the HP Norton application
"""

from pymongo.errors import ConnectionFailure
import logging
import pathlib
import os
import csv
from pymongo import MongoClient
import types
import csv

# A timer utility class
import time


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


# Below, we create the Timed metaclass that times its classes' methods
# along with the setup functions that rewrite the class methods at class creation times

# Function that times execution of a passed in function, returns a new function
# encapsulating the behavior of the original function
def timefunc(fn, *args, **kwargs):

    def fncomposite(*args, **kwargs):
        timing = 'timings.csv'
        timer = Timer()
        timer.start()
        rt = fn(*args, **kwargs)
        timer.stop()
        print(f'{fn.__name__},{float(timer.elapsed):.5f}sec\n')
        
        with open(timing, 'a+') as csv_timing:
            csv_timing.write(
                f'{fn.__name__},{float(timer.elapsed):.5f}sec \n')

        return rt
    # return the composite function
    return fncomposite

# The 'Timed' metaclass that replaces methods of its classes
# with new methods 'timed' by the behavior of the composite function transformer


class Timed(type):

    def __new__(cls, name, bases, attr):
        # replace each function with
        # a new function that is timed
        # run the computation with the provided args and return the computation result
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = timefunc(value)

        return super(Timed, cls).__new__(cls, name, bases, attr)

# The below code example test the metaclass
# Classes that use the Timed metaclass should be timed for us automatically
# check the result in the REPL


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

class DBCls(metaclass=Timed):
    
    DATABASE_NAME = "inventory_v3"
    def import_data(directory, product_file, customer_file, rental_file, connection=None, database_name=None):
        """creates and populates a new MongoDB database with these csv data file,
        :param  product_file:
        :param  customer_file:
        :param  rentals_file:
        :return: 2 tuples: numbers of record count product, customers, and rentals added, and count of any error that occurred.
        """

        mongo = MongoDBConnection()
        database_name = database_name or DBCls.DATABASE_NAME
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


    def show_available_products():
        """Returns a dictionary of products listed as available with the following fields:
        :return: dictionary of product_id.
            description.
            product_type.
            quantity_available.:
        """
        mongo = MongoDBConnection()
        database_name = DBCls.DATABASE_NAME

        with mongo:
            db = mongo.connection.get_database(name=database_name)
            products_dict = db.products.find()
            all_prod = {product['product_id']: dict(product) for product in products_dict}

            return all_prod


    def show_rentals(product_id):
        """Returns a dictionary with the following user information from users,
        that have rented products matching product_id:
            :param product_id:
            :return: dictionary of user information
                user_id.
                    name.
                    address.
                    phone_number.
                    email.
        """
        mongo = MongoDBConnection()
        database_name = DBCls.DATABASE_NAME

        with mongo:
            db = mongo.connection.get_database(name=database_name)

            customer_info = {}
            for rental in db.rentals.find():
                if rental["product_id"] == product_id:
                    customer_id = rental["user_id"]

                    customer_record = db.customers.find_one(
                        {"user_id": customer_id})

                    customer_dict = {"name": customer_record["name"],
                                    "address": customer_record["address"],
                                    "phone_number": customer_record["phone_number"],
                                    "email": customer_record["email"]}
                    customer_info[customer_id] = customer_dict
            return customer_info


if __name__ == '__main__':
    directory = os.getcwd()
    product_file = 'products.csv'
    customer_file = 'customers.csv'
    rental_file = 'rentals.csv'
    database_name = 'inventory_v1'
    product_id = 'prd001'

    DBCls.import_data(directory, product_file, customer_file,
                rental_file, connection=None, database_name=None)

    # prod = timefunc(DBCls.show_available_products)
    # prod()

    # DBCls.show_available_products()
    # DBCls.show_rentals(product_id)
    

