from pymongo import MongoClient

import csv
import os
import pathlib
import logging
from charges_calc import exception
from pymongo.errors import ConnectionFailure


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


DATABASE_NAME = "inventory_v2"


@exception
def import_data(directory, product_file, customer_file, rental_file, connection=None, database_name=None):
    """creates and populates a new MongoDB database with these csv data file,
       :param  product_file:
       :param  customer_file:
       :param  rentals_file:
       :return: 2 tuples: numbers of record count product, customers, and rentals added, and count of any error that occurred.
    """

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
def show_available_products():
    """Returns a dictionary of products listed as available with the following fields:
       :return: dictionary of product_id.
           description.
           product_type.
           quantity_available.:
    """
    mongo = MongoDBConnection()
    database_name = DATABASE_NAME

    with mongo:
        db = mongo.connection.get_database(name=database_name)
        products_dict = db.products.find()
        all_prod = {product['product_id']:dict(product) for product in products_dict}

        return all_prod

@exception
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
    database_name = DATABASE_NAME

    with mongo:
        db = mongo.connection.get_database(name=database_name)

        customer_info = {}
        for rental in db.rentals.find():
            if rental["product_id"] == product_id:
                customer_id = rental["user_id"]

                customer_record = db.customers.find_one({"user_id":customer_id})

                customer_dict = {"name": customer_record["name"],
                                "address":customer_record["address"],
                                "phone_number": customer_record["phone_number"],
                                "email": customer_record["email"]}
                customer_info[customer_id] = customer_dict
        return customer_info


if __name__ == '__main__':
    directory = os.getcwd()
    product_file = 'products.csv'
    customer_file = 'customers.csv'
    rental_file = 'rentals.csv'
    # database_name = 'inventory_v1'

    import_data(directory, product_file, customer_file,
                rental_file, connection=None, database_name=None)
    
    # product_id = 'prd001'
    # import_data(directory_name, product_file, customer_file, rentals_file)
    # print(show_available_products())
    # print(show_rentals(product_id))
    # main()
