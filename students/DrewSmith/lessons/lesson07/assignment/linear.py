'''
HP Norton inventory and customer information database functions
'''


import datetime
import csv
from threading import Thread
from pathlib import Path
import logging
import peewee as pw
import create_customers as cc
import config as config
from customers_model import Customer
from pymongo import MongoClient


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class MongoDBConnection(object):
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

def import_product_data(directory_name, product_file, customer_file, rentals_file,
                connection=None, database_name=None):
    '''
    Imports data from 3 files an inserts product, customer and rental data

    :param directory_name: directory where data files are stored
    :param product_file: file name with product data
    :param customer_file: file name with customer data
    :param rentals_file: file name with rentals data
    :param connection: DB connection for data inserts
    :param database_name: Database to use for the query,
        or None to use production default
    '''
    connection = connection or MongoDBConnection()
    database_name = database_name or config.DATABASE_NAME
    directory = Path(directory_name)

    errors = [0, 0, 0]
    counts = [0, 0, 0]
    with connection:
        database = connection.connection.get_database(name=database_name)

        with open(directory / product_file, 'r') as file:
            csv_file = csv.DictReader(file, fieldnames=("product_id",
                                                        "description",
                                                        "product_type",
                                                        "quantity_available"))
            records = list()
            for index, record in enumerate(csv_file):
                if index == 0:
                    continue
                try:
                    record["quantity_available"] = int(record["quantity_available"])
                except ValueError:
                    errors[0] += 1
                else:
                    records.append(record)
            counts[0] = len(records)
            database["products"].insert_many(records)

        with open(directory / customer_file, 'r') as file:
            csv_file = csv.DictReader(file, fieldnames=("user_id",
                                                        "name",
                                                        "address",
                                                        "zip_code",
                                                        "phone_number",
                                                        "email"))
            records = [record for index, record in enumerate(csv_file) if index > 0]
            counts[1] = len(records)
            database["customers"].insert_many(records)

        with open(directory / rentals_file, 'r') as file:
            csv_file = csv.DictReader(file, fieldnames=("product_id", "user_id"))
            records = [record for index, record in enumerate(csv_file) if index > 0]
            counts[2] = len(records)
            database["rentals"].insert_many(records)

    return (tuple(counts), tuple(errors))

def get_prodcuts_total_record_count(connection=None, database_name=None):
    connection = connection or MongoDBConnection()
    database_name = database_name or config.DATABASE_NAME

    with connection:
        database = connection.connection.get_database(name=database_name)
        return sum((database[collection].count() for collection in ["products", "customers", "rentals"]))


# Customers (sqlite)
def convert_csv(file_path):
    '''
    Generator for CSV file formatted for Customer model data

    :param file_path: file path for the CSV file
    :yield: CSV line dictionary formatted for Customer model
    '''
    fields = ('customer_id', 'first_name', 'last_name', 'home_address',
              'phone_number', 'email_address', 'status', 'credit_limit')
    with open(file_path, 'r') as file:
        csv_file = csv.DictReader(file, fieldnames=fields)
        for index, row in enumerate(csv_file):
            if index == 0:
                continue

            row['phone_number'] = "".join(
                char for char in row['phone_number'] if char not in  '.()- ')
            row['status'] = bool(row['status'].lower() == 'active')
            row['credit_limit'] = float(row['credit_limit'])
            yield row

def bulk_add_customers(customers):
    '''
    Adds a bulk amount of customers

    :param customers: sequence of dictionaries, expects keys:
        customer_id, first_name, last_name, home_address,phone_number, email_address,
        status, credit_limit
    '''
    records_added = 0
    batch_size = 120
    customer_list = list()
    database = cc.get_database()
    for index, customer in enumerate(customers, start=1):
        try:
            customer['credit_limit'] = float(customer['credit_limit'])
        except ValueError as err:
            logging.error(err)
            raise ValueError(f"Invalid value: record {index}: " \
                f"invalid credit_limit: '{customer['credit_limit']}'")

        if not isinstance(customer['status'], bool):
            text = f"Invalid value: record {index}: status is not a bool: '{customer['status']}'"
            logging.error(text)
            raise ValueError(text)

        customer_list.append(customer)
        if index % batch_size == 0:
            _insert_customer_list(customer_list, database)
            customer_list = list()
            records_added += batch_size

    if len(customer_list) > 0:
        _insert_customer_list(customer_list, database)
        records_added += len(customer_list)
    
    return records_added

def _insert_customer_list(customer_list, database):
    '''
    Internal function to add customer list with error checking

    :param customer_list: sequence of customer dictionaries to insert
    :param database: database object for the atomic transaction
    '''
    with database.atomic():
        try:
            Customer.insert_many(customer_list).execute()
        except pw.IntegrityError as error:
            logging.error(f"Customer already exists: {str(error)}")
            raise
        else:
            LOGGER.info(f"Inserted {len(customer_list)} customer(s)")

def get_customers_record_count():
    return Customer.select().count()


def database_setup():
    cc.get_database().drop_tables([Customer])
    cc.get_database().create_tables([Customer])

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.get_database(name=config.DATABASE_NAME)
        db.drop_collection("customers")
        db.drop_collection("products")
        db.drop_collection("rentals")

def main():
    database_setup()

    start = datetime.datetime.now()
    parent_path = Path(__file__).parent

    products_starting = get_prodcuts_total_record_count()    
    products_add = import_product_data(parent_path, "products.csv", "contacts.csv", "rentals.csv")
    products_ending = get_prodcuts_total_record_count()


    customers_starting = get_customers_record_count()
    customers_add = bulk_add_customers(convert_csv("customers.csv"))
    customers_end = get_customers_record_count()

    execute_time = (datetime.datetime.now() - start).total_seconds()

    return [(sum(products_add[0]), products_starting, products_ending, execute_time),
            (customers_add, customers_starting, customers_end, execute_time)]

if __name__ == "__main__":
    print(main())