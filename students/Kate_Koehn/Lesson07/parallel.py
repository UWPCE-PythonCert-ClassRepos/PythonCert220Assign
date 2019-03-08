""""
Program to query products and customers in the rental database.

"""
import csv
from timeit import timeit
from pymongo import MongoClient
import threading
import os
import time

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


def add_data(results, collection, directory_name, filename):
    start_time = time.time()
    initial_records = collection.count_documents({})
    file_path = os.path.join(directory_name, filename)

    collection.insert_many(import_csv(file_path), ordered=False)

    end_records = collection.count_documents({})
    processed_records = end_records - initial_records
    # print(f"{filename} done")
    run_time = time.time() - start_time

    result_tuple = (processed_records, initial_records, end_records, run_time)

    results[collection.name] = result_tuple


def import_data(db, directory_name, product_file, customer_file, rentals_file):
    """
    Function to import data into three MongoDB tables
    :param directory_name:
    :param product_file: csv file of products with column names: product_id,description,product_type,quantity_available
    :param customer_file: csv file of products rented by users with column names: product_id,user_id
    :param rentals_file: csv file of customers who have rented with column names: user_id,name,address,zip_code,
    phone_number,email
    :return: tuple of records added to db, tuple of errors encountered while importing data
    """


    products = db["products"]
    customers = db["customers"]
    rentals = db["rentals"]

    output_dict = {}

    threads = [threading.Thread(target=add_data, args=(output_dict, products, directory_name, product_file)),
               threading.Thread(target=add_data, args=(output_dict, customers, directory_name, customer_file)),
               threading.Thread(target=add_data, args=(output_dict, rentals, directory_name, rentals_file))]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # print(output_dict["products"], output_dict["customers"])
    return [output_dict["products"], output_dict["customers"]]



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

            rental_users = {"first_name": customer_record["first_name"],
                            "last_name": customer_record["last_name"],
                            "address": customer_record["address"],
                            "phone_number": customer_record["phone_number"],
                            "email": customer_record["email"],
                            "status": customer_record["status"],
                            "credit_limit": customer_record["credit_limit"]}
            rental_users_dict[customer_id] = rental_users
            continue
        else:
            continue

    return rental_users_dict


def main():
    """
    Main function to create database connection, import data, and clear data from tables before program exists.
    """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        import_data(db, "", "products.csv", "customers.csv", "rentals.csv")

        clear_db(db)


def clear_db(db):
    """
    Clears data in mongodb database.
    """
    db.products.drop()
    db.customers.drop()
    db.rentals.drop()


if __name__ == "__main__":
    # main()
    print(timeit("main()", globals=globals(), number=1))
    print(timeit("main", globals=globals(), number=10))


