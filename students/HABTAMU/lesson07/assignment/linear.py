'''
HP Norton inventory and customer information database functions
'''


import csv
import os
import logging
import pathlib
import time
from pprint import pprint
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
import logging_config as log_conf

log_conf.logger.info("*prototype migration of product data from a sample csv file into MongoDB using MongoDB API")

#Step 1: Connect to HP_Norton MongoDB
myclient = MongoClient("mongodb://localhost:27017/")
db = myclient.HP_Norton
# directory = pathlib.Path(directory_name)

log_conf.logger.info('* HP_Norton MongoDB created and connected successfuly')
# Customers collection
customers = db["customers"]
# Products collection
products = db["products"]
# Rentals collection
rentals = db["rentals"]


def import_data(directory_name, product_file, customer_file, rentals_file):
    """creates and populates a new MongoDB database with these csv data file,
       :param  product_file:
       :param  customer_file:
       :param  rentals_file:
       :return: 2 tuples: numbers of record count product, customers, and rentals added, and count of any error that occurred.
    """
    start = time.time()

    with open('lesson05_assignment_sample_csv_files_customers.csv', 'r') as cust_file:
        csvreader = csv.reader(cust_file, delimiter=',', quotechar='|')
        for row in csvreader:
            # import pdb; pdb.set_trace()
            db.customers.insert_one({'user_id': row[0], 'name': row[1], 'address': row[2], 'zip_code': row[3], 'phone_number': row[4], 'email': row[5]})
        log_conf.logger.info('* read and load customer csv file to customers collection ')

    with open('lesson05_assignment_sample_csv_files_products.csv', 'r') as prod_file:
        csvreader = csv.reader(prod_file, delimiter=',', quotechar='|')
        for row in csvreader:
            db.products.insert_one({'product_id': row[0], 'description': row[1], 'product_type': row[2], 'quantity_available': row[3]})
        log_conf.logger.info('* read a products csv file and load to products collection ')

    with open('lesson05_assignment_sample_csv_files_rentals.csv', 'r') as rent_file:
        csvreader = csv.reader(rent_file, delimiter=',', quotechar='|')
        for row in csvreader:
            db.rentals.insert_one({'product_id': row[0], 'user_id': row[1]})
        log_conf.logger.info('read a rentals csv file and load to rentals collection ')

    # customers_count = db.customers.find().Collection.count_documents()
    # products_count = db.products.find().Collection.count_documents()
    # rentals_count = db.rentals.find().Collection.count_documents()

    customers_count = db.customers.find().count()
    products_count = db.products.find().count()
    rentals_count = db.rentals.find().count()


    end = time.time()
    # returns record count of the number of products, customers and rentals added (in that order)
    print(f'\nWith linear time taken to add customer, product and rentals csv file to mongodb: {end - start:.2f}s\n')

    return (products_count, customers_count, rentals_count), "None"


def show_available_products():
    """Returns a dictionary of products listed as available with the following fields:
       :return: dictionary of product_id.
           description.
           product_type.
           quantity_available.:
    """
    # import pdb; pdb.set_trace()
    products_dic = db.products.find()
    all_prod = {product['product_id']:dict(product) for product in products_dic}

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
    # import pdb; pdb.set_trace()
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

# def main():
#     """ Connect to MongoDB """
#     try:
#         # c = Connection(host="localhost", port=27017)
#         myclient = MongoClient("mongodb://localhost:27017/")
#         import pdb; pdb.set_trace()
#     except ConnectionFailure as e:
#         sys.stderr.write("Could not connect to Mongo to MongoDB: %s" % e)
#         logger.error("Could not connect to Mongo to MongoDB")
#         logger.exception(e)
#         sys.exit(1)
#     #Get a Database handle to a database named HP_Norton
#     db = myclient["HP_Norton"]
#
#     # Customers collection
#     customers = db["customers"]
#     # Products collection
#     products = db["products"]
#     # Rentals collection
#     rentals = db["rentals"]
#
#     assert db.connection == myclient
#     print("Successfully set up a database handle")


if __name__ == "__main__":
    directory_name = '/Users/hasfaw/Documents/Study and Tutor/UW/UW_PY/py220201901habtamu/PythonCert220Assign/students/HABTAMU/lesson05/assignment'
    product_file = '/Users/hasfaw/Documents/Study and Tutor/UW/UW_PY/py220201901habtamu/PythonCert220Assign/students/HABTAMU/lesson05/assignment/lesson05_assignment_sample_csv_files_products.csv'
    customer_file = '/Users/hasfaw/Documents/Study and Tutor/UW/UW_PY/py220201901habtamu/PythonCert220Assign/students/HABTAMU/lesson05/assignment/directory_name/lesson05_assignment_sample_csv_files_customers.csv'
    rentals_file = '/Users/hasfaw/Documents/Study and Tutor/UW/UW_PY/py220201901habtamu/PythonCert220Assign/students/HABTAMU/lesson05/assignment/directory_name/lesson05_assignment_sample_csv_files_rentals.csv'
    product_id = 'prd001'
    import_data(directory_name, product_file, customer_file, rentals_file)
    show_available_products()
    # print(show_rentals(product_id))
    # main()
