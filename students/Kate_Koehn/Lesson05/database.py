""""
Program to query products and customers in the rental database.

"""
import csv
from pymongo import MongoClient


class MongoDBConnection():
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


def import_csv(filename):
    """
    function to import csv files, this function is called in the import_data() function
    :param filename: takes a csv, removes unexpected character from first line, reads rows into dictionaries
    :return: list of dictionaries of rows
    """
    with open(filename, newline="", encoding='utf-8') as file:
        dict_list = []
        csv_data = csv.reader(file)
        headers = next(csv_data, None)
        if headers[0].startswith("\ufeff"):
            headers[0] = headers[0][1:]

        for row in csv_data:
            row_dict = {}
            for index, column in enumerate(headers):
                row_dict[column] = row[index]

            dict_list.append(row_dict)

        return dict_list


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Function to import data into three MongoDB tables
    :param directory_name:
    :param product_file: csv file of products with column names: product_id,description,product_type,quantity_available
    :param customer_file: csv file of products rented by users with column names: product_id,user_id
    :param rentals_file: csv file of customers who have rented with column names: user_id,name,address,zip_code,
    phone_number,email
    :return: tuple of records added to db, tuple of errors encountered while importing data
    """
    product_errors = 0
    customer_errors = 0
    rental_errors = 0
    try:
        products = db["products"]
        products.insert_many(import_csv(product_file))
    except ImportError:
        product_errors += 1
    try:
        customers = db["customers"]
        customers.insert_many(import_csv(customer_file))
    except ImportError:
        customer_errors += 1
    try:
        rentals = db["rentals"]
        rentals.insert_many(import_csv(rentals_file))
    except ImportError:
        rental_errors += 1

    record_count = (db.products.find().count(), db.customers.find().count(), db.rentals.find().count())
    error_count = (product_errors, customer_errors, rental_errors)

    return record_count, error_count


def show_available_products(db):
    """
    Returns a dictionary for each product that is available for rent (quantity > 0).
    :param db: MongoDB
    :return: Dictionary with product_id, description, product_type, quantity_available.
    """
    available_products = {}
    for product_id in db.products.find():
        product_dict = {"description": product_id["description"],
                    "product_type": product_id["product_type"],
                    "quantity_available": product_id["quantity_available"]}
        if product_id["quantity_available"] != "0":
            available_products[product_id["product_id"]] = product_dict
            continue
        else:
            continue

    return available_products


def show_rentals(db, product_id):
    """
    Function to look up customers who have rented a specific product.
    :param db: MongoDB
    :param product_id: ex: "prd005"
    :return: dictionary of customer info. Key: user_id, values: dict of name, address, phone number, and email
    """
    rental_users_dict = {}
    for rental in db.rentals.find():
        if rental["product_id"] == product_id:
            customer_id = rental["user_id"]

            customer_record = db.customers.find_one({"user_id": customer_id})

            rental_users = {"name": customer_record["name"],
                            "address": customer_record["address"],
                            "phone_number": customer_record["phone_number"],
                            "email": customer_record["email"]}
            rental_users_dict[customer_id] = rental_users
            continue
        else:
            continue

    return rental_users_dict


if __name__ == "__main__":
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database connection
        db = mongo.connection.media


        import_data("", "products.csv", "customers.csv", "rentals.csv")

        show_available_products(db)

        show_rentals(db, "prd005")

        # clear tables for next time
        drop_prompt = input("Drop data?")
        if drop_prompt.upper() == 'Y':
            db.products.drop()
            db.customers.drop()
            db.rentals.drop()
