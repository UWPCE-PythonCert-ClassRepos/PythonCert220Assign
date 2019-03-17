"""
Lesson 10 Assignment
Metaprogramming
"""

import csv
import os
import types
import time
import pymongo

# pylint: disable-msg=line-too-long
# pylint: disable-msg=invalid-name
# pylint: disable-msg=no-self-use
# pylint: disable-msg=too-many-arguments


class MongoDBConnection:
    """
    Creates a context manager to access MongoDB.
    """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = pymongo.MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    """
    Prints the documents in a collection.
    :param collection_name: collection
    """

    for doc in collection_name.find():
        print(doc)


def timed_wrapper(func):
    """
    Function that times the execution of the passed in function.
    Returns a new function that encapsulates the behavior of the original function.
    """

    def timed_func(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        time_elapsed = time.time() - start

        mongo = MongoDBConnection()

        with mongo:
            db = mongo.connection.media

            record_count = (db.products.count_documents({}), db.customers.count_documents({}), db.rentals.count_documents({}))

            time_results = f"{func.__name__}, {time_elapsed}, {record_count}\n"

        with open("timings.csv", "a+") as file:
            file.write(time_results)

        return result
    return timed_func


class MetaTimer(type):
    """
    Metaclass that replaces class methods with timed methods.
    """

    def __new__(cls, name, bases, attr):
        """
        Replace each function with a new function that is timed.
        Returns result from original function.
        """
        for key, value in attr.items():
            if isinstance(value, (types.FunctionType, types.MethodType)):
                attr[key] = timed_wrapper(value)

        return super(MetaTimer, cls).__new__(cls, name, bases, attr)


class Database(metaclass=MetaTimer):
    """
    Class to manage the MongoDB.
    """

    def _import_csv(self, filename):
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
                row_dict = {column: row[index] for index, column in enumerate(headers)}
                dict_list.append(row_dict)

            return dict_list

    def _add_bulk_data(self, collection, directory_name, filename):
        """
        Adds bulk data to the database.
        :param collection: collection
        :param directory_name: directory name
        :param filename: filename
        :return: number of errors
        """
        file_path = os.path.join(directory_name, filename)

        try:
            collection.insert_many(Database._import_csv(self, file_path), ordered=False)
            return 0

        except pymongo.errors.BulkWriteError as bwe:
            print(bwe.details)
            return len(bwe.details["writeErrors"])

    def import_data(self, db, directory_name, products_file, customers_file, rentals_file):
        """
        Takes a directory name and three csv files as input.  Creates and populates a new MongoDB.
        :param db: MongoDB
        :param directory_name: Directory name for files.  Use "" for current directory.
        :param products_file: Csv file with product data.
        :param customers_file: Csv file with customer data.
        :param rentals_file: Csv file with rentals data.
        :return: Tuple with record count for products, customers, rentals added (in that order) and
                tuple with count of errors that occurred for products, customers, rentals (in that order).
        """

        products = db["products"]
        products_errors = Database._add_bulk_data(self, products, directory_name, products_file)

        customers = db["customers"]
        customers_errors = Database._add_bulk_data(self, customers, directory_name, customers_file)

        rentals = db["rentals"]
        rentals_errors = Database._add_bulk_data(self, rentals, directory_name, rentals_file)

        record_count = (db.products.count_documents({}), db.customers.count_documents({}), db.rentals.count_documents({}))
        error_count = (products_errors, customers_errors, rentals_errors)

        return record_count, error_count

    def show_available_products(self, db):
        """
        Returns a dictionary for each product listed as available.
        :param db: MongoDB
        :return: Dictionary with product_id, description, product_type, quantity_available.
        """

        available_products = {}

        for product in db.products.find():
            if product["quantity_available"] != "0":
                short_dict = {key: value for key, value in product.items() if key not in ("_id", "product_id")}
                available_products[product["product_id"]] = short_dict

        return available_products

    def show_rentals(self, db, product_id):
        """
        Returns a dictionary with user information from users who have rented products matching the product_id.
        :param db: MongoDB
        :param product_id: product id
        :return: user_id, first name, last name, address, phone_number, email, status, credit limit
        """

        customer_info = {}

        for rental in db.rentals.find():
            if rental["product_id"] == product_id:
                customer_id = rental["user_id"]
                customer_record = db.customers.find_one({"user_id": customer_id})

                short_dict = {key: value for key, value in customer_record.items() if key not in ("_id", "user_id")}
                customer_info[customer_id] = short_dict

        return customer_info

    def clear_data(self, db):
        """
        Delete the data in MongoDB.
        :param db: MongoDB
        :return: Empty MongoDB.
        """
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()


if __name__ == "__main__":
    MONGO = MongoDBConnection()

    with MONGO:
        DB = MONGO.connection.media

        TIMED_DATABASE = Database()

        print("Importing data for products, customers, and rentals.\n")
        records_and_errors = TIMED_DATABASE.import_data(DB, "", "products_10.csv", "customers_10.csv", "rentals_10.csv")
        # records_and_errors = TIMED_DATABASE.import_data(DB, "", "products_10000.csv", "customers_10000.csv", "rentals_10000.csv")

        print(f"Number of records for products, customers, rentals: {records_and_errors[0]}.")
        print(f"Number of errors for products, customers, rentals: {records_and_errors[1]}.")
        print()

        print("Showing available products:")
        print(TIMED_DATABASE.show_available_products(DB))

        print("\nShowing rental information for P000002:")
        print(TIMED_DATABASE.show_rentals(DB, "P000002"))

        print("\nClearing data from database.")
        TIMED_DATABASE.clear_data(DB)
