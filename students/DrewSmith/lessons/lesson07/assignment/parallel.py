'''
HP Norton inventory and customer information database functions
'''


import datetime
import csv
from pathlib import Path
import logging
import peewee as pw
import assignment.create_customers as cc
import assignment.config as config
from assignment.customers_model import Customer
from pymongo import MongoClient
from threading import Thread
from multiprocessing.pool import ThreadPool

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

def _read_csv(directory, file_name):
    with open(directory / file_name, 'r') as file:
        csv_file = csv.reader(file)
        columns = next(csv_file, None)
        columns = [column if not column.startswith('ï»¿') else column[3:] for column in columns]
        for record in csv_file:
            yield dict(zip(columns, record))

def insert_csv(directory, file_name, collection):
    '''
    Read a CSV file and insert records into MongoDB

    :param directory: csv file directory
    :param file_name: csv file name
    :param collection: MongoDB collection to insert the records
    '''
    records = [record for record in _read_csv(directory, file_name)]
    collection.insert_many(records)
    return len(records)
        
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

    pool = ThreadPool(processes=3)
    counts = [0, 0, 0]
    with connection:
        database = connection.connection.get_database(name=database_name)

        prod = pool.apply_async(insert_csv, (directory, product_file, database["products"]))
        cust = pool.apply_async(insert_csv, (directory, customer_file, database["customers"]))
        rent = pool.apply_async(insert_csv, (directory, rentals_file, database["rentals"]))

        counts[0] = prod.get()
        counts[1] = cust.get()
        counts[2] = rent.get()
        
        pool.close()
        pool.join()

    return (tuple(counts), )

def get_prodcuts_total_record_count(connection=None, database_name=None):
    '''
    Get total record count for products, customers, and rentals
    '''
    connection = connection or MongoDBConnection()
    database_name = database_name or config.DATABASE_NAME

    with connection:
        database = connection.connection.get_database(name=database_name)
        return sum((database[collection].count() for collection in ["products", "customers", "rentals"]))

def show_available_products(connect=None, database_name=None):
    '''
    Returns all products that are available to rent

    :param connect: connection object, or None to use default
    :param database_name: Database to use for the query,
        or None to use production default
    '''
    connect = connect or MongoDBConnection()
    database_name = database_name or config.DATABASE_NAME
    with connect:
        database = connect.connection.get_database(name=database_name)
        products = database["products"]
        result = dict()
        for record in products.find({"quantity_available": {"$gt": 0}}):
            result[record["product_id"]] = {
                "description": record["description"],
                "product_type": record["product_type"],
                "quantity_available": record["quantity_available"]
            }
    return result

def show_rentals(product_id, connect=None, database_name=None):
    '''
    Returns all users that are renting a specific product_id

    :param product_id: product_id to search for
    :param connect: connection object, or None to use default
    :param database_name: Database to use for the query,
        or None to use production default
    '''
    connect = connect or MongoDBConnection()
    database_name = database_name or config.DATABASE_NAME
    with connect:
        database = connect.connection.get_database(name=database_name)
        rentals = database["rentals"]
        customers = database["customers"]
        result = dict()

        user_ids = [rental["user_id"] for rental in rentals.find({"product_id": product_id})]

        for record in customers.find({"user_id": {"$in": user_ids}}):
            result[record["user_id"]] = {
                "name": record["name"],
                "address": record["address"],
                "phone_number": record["phone_number"],
                "email": record["email"]
            }
    return result


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
    pool = ThreadPool(processes=3)
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
            pool.apply_async(_insert_customer_list, (list(customer_list), database))
            customer_list = list()
            records_added += batch_size

    if len(customer_list) > 0:
        pool.apply_async(_insert_customer_list, (list(customer_list), database))
        records_added += len(customer_list)
    
    pool.close()
    pool.join()
    
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
    '''
    Get the Customers count
    '''
    return Customer.select().count()


def _database_setup():
    '''
    reset database
    '''
    cc.get_database().drop_tables([Customer])
    cc.get_database().create_tables([Customer])

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.get_database(name=config.DATABASE_NAME)
        db.drop_collection("customers")
        db.drop_collection("products")
        db.drop_collection("rentals")

def main():
    _database_setup()
    pool = ThreadPool(processes=2)

    start = datetime.datetime.now()
    parent_path = Path(__file__).parent

    products_starting = get_prodcuts_total_record_count()
    customers_starting = get_customers_record_count()

    products_thread = pool.apply_async(import_product_data, (parent_path, "products.csv", "contacts.csv", "rentals.csv"))
    customers_thread = pool.apply_async(bulk_add_customers, (convert_csv("customers.csv"), ))
    pool.close()
    pool.join()

    products_ending = get_prodcuts_total_record_count()
    customers_end = get_customers_record_count()

    execute_time = (datetime.datetime.now() - start).total_seconds()

    return [(sum(products_thread.get()[0]), products_starting, products_ending, execute_time),
            (customers_thread.get(), customers_starting, customers_end, execute_time)]

if __name__ == '__main__':
    print(main())