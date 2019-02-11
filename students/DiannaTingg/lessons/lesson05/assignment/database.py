"""
Lesson 05 Assignment
MongoDB
"""

import csv
import os
from pymongo import MongoClient

# pylint: disable-msg=line-too-long
# pylint: disable-msg=invalid-name
# pylint: disable-msg=redefined-outer-name


class MongoDBConnection:
    """
    Creates a MongoDB Connection
    """
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    """
    Prints documents in a collection.
    :param collection_name: collection
    :return:
    """
    for doc in collection_name.find():
        print(doc)


def _import_csv(filename):
    """
    Returns a list of dictionaries.  One dictionary for each row of data in a csv file.
    :param filename: csv file
    :return: list of dictionaries
    """

    with open(filename, newline="") as csvfile:
        dict_list = []

        csv_data = csv.reader(csvfile)

        headers = next(csv_data, None)  # Save the first line as the headers

        if headers[0].startswith("ï»¿"):  # Check for weird formatting
            headers[0] = headers[0][3:]

        for row in csv_data:
            row_dict = {}

            for index, column in enumerate(headers):
                row_dict[column] = row[index]

            dict_list.append(row_dict)

        return dict_list


def import_data(db, directory_name, products_file, customers_file, rentals_file):
    """
    Takes a directory name and three csv files as input.  Creates and populates a new MongoDB.
    :param db: MongoDB
    :param directory_name: directory name for files.  Use "" for current directory.
    :param products_file: csv file with product data
    :param customers_file: csv file with customer data
    :param rentals_file: csv file with rentals data
    :return: Tuple with record count for products, customers, rentals added (in that order) and
             tuple with count of errors that occurred for products, customers, rentals (in that order).
    """

    products = db["products"]
    products_file_path = os.path.join(directory_name, products_file)
    products.insert_many(_import_csv(products_file_path))

    customers = db["customers"]
    customers_file_path = os.path.join(directory_name, customers_file)
    customers.insert_many(_import_csv(customers_file_path))

    rentals = db["rentals"]
    rentals_file_path = os.path.join(directory_name, rentals_file)
    rentals.insert_many(_import_csv(rentals_file_path))

    record_count = (db.products.count_documents({}), db.customers.count_documents({}), db.rentals.count_documents({}))

    # TODO: Fix this
    error_count = (0, 0, 0)

    return record_count, error_count


def show_available_products(db):
    """
    Returns a dictionary for each product listed as available.
    :param db: MongoDB
    :return: Dictionary with product_id, description, product_type, quantity_available.
    """

    available_products = {}

    for product in db.products.find():
        if int(product["quantity_available"]) > 0:

            product_dict = {"description": product["description"],
                            "product_type": product["product_type"],
                            "quantity_available": product["quantity_available"]}

            available_products[product["product_id"]] = product_dict

    return available_products


def show_rentals(db, product_id):
    """
    Returns a dictionary with user information from users who have rented products matching the product_id.
    :param db: MongoDB
    :param product_id: product id
    :return: user_id, name, address, phone_number, email
    """

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
    """
    Delete data in MongoDB.
    :param db: MongoDB
    :return: Empty MongoDB.
    """
    db.products.drop()
    db.customers.drop()
    db.rentals.drop()


if __name__ == "__main__":
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
