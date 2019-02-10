"""
Lesson 05 Assignment
MongoDB
"""

from pymongo import MongoClient
import csv


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
    for doc in collection_name.find():
        print(doc)


def import_csv(filename):
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


def import_data(db, directory_name, product_file, customer_file, rentals_file):
    """
    Takes a directory name and three csv files as input.  Creates and populates a new MongoDB.
    :param db: MongoDB
    :param directory_name: directory name for files
    :param product_file: csv file with product data
    :param customer_file: csv file with customer data
    :param rentals_file: csv file with rentals data
    :return: Tuple with record count for products, customers, rentals added (in that order) and
             tuple with count of errors that occurred for products, customers, rentals (in that order).
    """

    products = db["products"]
    products.insert_many(import_csv(product_file))

    customers = db["customers"]
    customers.insert_many(import_csv(customer_file))

    rentals = db["rentals"]
    rentals.insert_many(import_csv(rentals_file))

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

    # Example:
    # {‘user001’:{‘name’:’Elisa Miles’, ’address’:‘4490 Union Street’, ’phone_number’:‘206-922-0882’, ’email’:’elisa.miles@yahoo.com’},
    # ’user002’:{‘name’:’Maya Data’, ’address’:‘4936 Elliot Avenue’, ’phone_number’:‘206-777-1927’, ’email’:’mdata@uw.edu’}}

    # TODO: Write this


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

        import_data(db, "", "products.csv", "customers.csv", "rentals.csv")

        print(show_available_products(db))

        clear_data(db)


