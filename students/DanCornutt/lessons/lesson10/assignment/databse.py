"""HW 10:
Outputs details of timing for all functions in the program.
Gather this data and write it to a file called timings.csv.
The file should contain function name, time taken, and number of records
    processed, and be called timing.csv.

Timing Class from:
    https://stackabuse.com/python-metaclasses-and-metaprogramming/
"""

import types
import time
import csv
import logging
from pymongo import MongoClient


def timefunc(fn, *args, **kwargs):

    def fncomposite(*args, **kwargs):
        timer = Timer()
        timer.start()
        rt = fn(*args, **kwargs)
        timer.stop()
        # open CSV append and add timer file
        with open("timing.csv", 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([fn.__name__, timer.elapsed])  # &items processed
        return rt
    # return the composite function
    return fncomposite


class Timer:
    """Timer class to be used to time event
    """

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


class Timed(type):
    """Timed MetaClass for timing the events of instanced classes
    """
    def __new__(cls, name, bases, attr):
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is \
                    types.MethodType:
                attr[name] = timefunc(value)

        return super(Timed, cls).__new__(cls, name, bases, attr)


class MongoDBConnection():
    """MongoDB Connection to database"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class DataLink(metaclass=Timed):

    def __init__(self):
        mongo = MongoDBConnection()
        with mongo:
            self.db = mongo.connection.media

    def log_setup(self):
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
        %(message)s"
        logging.basicConfig(level=logging.WARNING, format=log_format,
                            filename='mylog.log')

    def show_available_products(self):
        """Returns dict of products available for rental"""
        info = {}
        qset = self.db['products'].find({"quantity_available": {"$gt": "0"}})
        for item in qset:
            id_num = item['product_id']
            content = dict((k, item[k]) for k in (
                'description', 'product_type', 'quantity_available'
            ))
            info.update({id_num: content})
        return info

    def show_rentals(self, product_id):
        """Returns a Python dictionary with the following user information from
        users that have rented products matching product_id:
        user_id.
        name.
        address.
        phone_number.
        email.
        """
        info = {}
        qset = self.db.rentals.aggregate([
            {"$match": {
                "product_id": product_id
            }},
            {"$lookup": {
                "localField": "user_id",
                "from": "customers",
                "foreignField": "user_id",
                "as": "cust"
            }},
            {"$unwind": "$cust"},
            {"$project": {
                "user_id": 1,
                "name": "$cust.name",
                "address": "$cust.address",
                "phone_number": "$cust.phone_number",
                "email": "$cust.email"
            }}
        ])
        for item in qset:
            id = item['user_id']
            content = dict((k, item[k]) for k in (
                'name', 'address', 'phone_number', 'email'
            ))
            info.update({id: content})
        return info

    def add_collection_csv(self, directory, f_name):
        """Reads csv by line. Uses csv dict iterator to loop through csv and add
        document to collection
        param1: directory
        param2: csv file for collection
        """

        coll = f_name.split('.')[0]
        cd = self.db[coll]
        err = 0
        with open(f_name, mode='r', encoding='utf-8-sig') as csv_f:
            reader = csv.DictReader(csv_f)
            for row in reader:
                logging.debug("Parsing data: {}".format(row))
                try:
                    cd.insert_one(row)
                except ValueError:
                    err += 1
        return (cd.count(), err)

    def import_data(self, dir_name, prod_f, cust_f, rent_f):
        """
        Fuction takes directory name and 3 csv files and then creates a new
        MongoDB with 3 collections.
        param1: directory name? I don't know the purpose
        param2: products
        param3: customers
        param4: rentals
        """

        prod_rpt = self.add_collection_csv(dir_name, prod_f)
        cust_rpt = self.add_collection_csv(dir_name, cust_f)
        rent_rpt = self.add_collection_csv(dir_name, rent_f)

        return((prod_rpt[0], cust_rpt[0], rent_rpt[0]),
               (prod_rpt[1], cust_rpt[1], rent_rpt[1]))


if __name__ == "__main__":
    dl = DataLink()
    dl.log_setup()
    # rpt = dl.import_data("", 'products.csv', 'customers.csv', 'rentals.csv')
    # dl.logging.error(rpt)

    available = dl.show_available_products()
    users = dl.show_rentals('prd002')
