""""
HW5 HP Norton MongoDB Project

"""
import csv
import logging
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

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


def log_setup():
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
    %(message)s"
    logging.basicConfig(level=logging.WARNING, format=log_format,
                        filename='mylog.log')


def show_available_products():
    """Returns dict of products available for rental"""
    info = {}
    qset = db['products'].find({"quantity_available": {"$gt": "0"}})
    for item in qset:
        id = item['product_id']
        content = dict((k, item[k]) for k in (
            'description', 'product_type', 'quantity_available'
        ))
        info.update({id: content})
    return info


def show_rentals(product_id):
    """Returns a Python dictionary with the following user information from
    users that have rented products matching product_id:
    user_id.
    name.
    address.
    phone_number.
    email.
    """
    info = {}
    qset = db.rentals.aggregate([
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


def add_collection_csv(directory, f_name):
    """Reads csv by line. Uses csv dict iterator to loop through csv and add
    document to collection
    param1: directory
    param2: csv file for collection
    """

    coll = f_name.split('.')[0]
    cd = db[coll]
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


def import_data(dir_name, prod_f, cust_f, rent_f):
    """
    Fuction takes directory name and 3 csv files and then creates a new
    MongoDB with 3 collections.
    param1: directory name? I don't know the purpose
    param2: products
    param3: customers
    param4: rentals
    """

    prod_rpt = add_collection_csv(dir_name, prod_f)
    cust_rpt = add_collection_csv(dir_name, cust_f)
    rent_rpt = add_collection_csv(dir_name, rent_f)

    return((prod_rpt[0], cust_rpt[0], rent_rpt[0]),
           (prod_rpt[1], cust_rpt[1], rent_rpt[1]))


def main():
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
    return db


if __name__ == "__main__":
    log_setup()
    db = main()
    rpt = import_data("", 'products.csv', 'customers.csv', 'rentals.csv')
    logging.error(rpt)

    available = show_available_products()
    users = show_rentals('prd002')
