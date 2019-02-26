'''
HP Norton inventory and customer information database functions
'''

import csv
import os
import logging
import pathlib
import multiprocessing
import concurrent.futures
import time
from pprint import pprint
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
import logging_config as log_conf
import _thread


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

a_lock = _thread.allocate_lock()


with a_lock:
    def import_data(directory_name, product_file, customer_file, rentals_file):
        """creates and populates a new MongoDB database with these csv data file,
           :param  product_file:
           :param  customer_file:
           :param  rentals_file:
           :return: 2 tuples: numbers of record count product, customers, and rentals added, and count of any error that occurred.
        """
        customer_counts = [0, 0, 0, 0]
        product_counts = [0, 0, 0, 0]
        customer_counts[1] = db.customers.find().count()
        product_counts[1] = db.products.find().count()
        # import pdb; pdb.set_trace()

        def customer():
            '''To populates a customers database collection with customer csv data file'''
            customer_start = time.time()
            with open('lesson05_assignment_sample_csv_files_customers.csv', 'r') as cust_file:
                csvreader = csv.reader(cust_file, delimiter=',', quotechar='|')
                customer_record_count = 0 # To count the number of customer records processed (int)
                for row in csvreader:
                    db.customers.insert_one({'user_id': row[0], 'name': row[1], 'address': row[2], 'zip_code': row[3], 'phone_number': row[4], 'email': row[5]})
                    customer_record_count = customer_record_count + 1
                    print(f' pid {os.getpid()} Processing customer record {customer_record_count}')
                log_conf.logger.info('* read a customer csv file and load to customers collection ')
                customer_counts[0] = customer_record_count
            customer_end = time.time()
            # time taken to run the customer module (float).
            customer_counts[3] = round(customer_end - customer_start, 5)

        def product():
            '''To populates a products database collection with products csv data file'''
            product_start = time.time()
            with open('lesson05_assignment_sample_csv_files_products.csv', 'r') as prod_file:
                csvreader = csv.reader(prod_file, delimiter=',', quotechar='|')
                product_record_count = 0 # To count the number of product records processed (int)
                for row in csvreader:
                    db.products.insert_one({'product_id': row[0], 'description': row[1], 'product_type': row[2], 'quantity_available': row[3]})
                    product_record_count = product_record_count + 1
                    print(f'pid {os.getpid()} Processing product record {product_record_count}')
                log_conf.logger.info('* read a products csv file and load to products collection ')
                product_counts[0] = product_record_count
            product_end = time.time()
            # time taken to run the customer module (float).
            product_counts[3] = round(product_end - product_start, 5)
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                executor.submit(customer)
                executor.submit(product)
        except Exception as exc:
            print('generated an exception: %s' % (exc))

        #the customers record count in the database after running (int)
        customer_counts[2] = db.customers.find().count()

        #the products record count in the database after running (int)
        product_counts[2] = db.products.find().count()

        print(f'\ntime taken with multithread(parallel) to add customer = {customer_counts[3]:.5f}s, and product {product_counts[3]:.5f}s csv file to mongodb  \n')
        return([tuple(customer_counts), tuple(product_counts)])

def show_available_products():
    """Returns a dictionary of products listed as available with the following fields:
       :return: dictionary of product_id.
           description.
           product_type.
           quantity_available.:
    """
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

if __name__ == "__main__":
    directory_name = '/Users/hasfaw/Documents/Study and Tutor/UW/UW_PY/py220201901habtamu/PythonCert220Assign/students/HABTAMU/lesson05/assignment'
    product_file = '/Users/hasfaw/Documents/Study and Tutor/UW/UW_PY/py220201901habtamu/PythonCert220Assign/students/HABTAMU/lesson05/assignment/lesson05_assignment_sample_csv_files_products.csv'
    customer_file = '/Users/hasfaw/Documents/Study and Tutor/UW/UW_PY/py220201901habtamu/PythonCert220Assign/students/HABTAMU/lesson05/assignment/directory_name/lesson05_assignment_sample_csv_files_customers.csv'
    rentals_file = '/Users/hasfaw/Documents/Study and Tutor/UW/UW_PY/py220201901habtamu/PythonCert220Assign/students/HABTAMU/lesson05/assignment/directory_name/lesson05_assignment_sample_csv_files_rentals.csv'
    product_id = 'prd001'
    start_time = time.time()
    print(import_data(directory_name, product_file, customer_file, rentals_file))
    end_time = time.time()
    time_print = end_time - start_time
    print(f' {time_print} Total time taken to process in parallel')
    # print(show_available_products())
    # print(show_rentals(product_id))
