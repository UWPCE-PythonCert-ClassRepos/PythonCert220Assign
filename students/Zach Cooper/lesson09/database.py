#!/usr/bin/env python3

"""
    Create Database Using MongoDB and MultiThreading
    Context Manager Part 2 for Lesson09
"""
import csv
import time
import logging
import queue as Queue
import pymongo
from threading import Thread
from pymongo import MongoClient


class MongoDBConnection():
    """ Set up MongoDB Connection and then close it"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ Windows needs to connect to host IP Address """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
            Opens Connection
        """
        if self.connection is None:
            try:
                self.connection = MongoClient(self.host, self.port)
            except pymongo.errors.ConnectionError as error:
                logging.error(f"MongoDB ConnectionError: {error}")
                raise
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """ Closes Database Connecton"""
        print("\nClosing the MongoDB connection.")
        self.connection.close()


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)

# Could be used for logging purposes
# def log_setup():
#     log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
#                   %(message)s"
#     logging.basicConfig(level=logging.WARNING, format=log_format,
#                         filename='mylog.log')


def csv_list(file):
    """
        Iterates through csv file and file contents in a list
        param: csvfile
    """
    return_list = []
    with open('sample_csv_files/' + file, encoding='utf-8-sig') as csv_file:
        file_input = csv.DictReader(csv_file)
        for row in file_input:
            return_list.append(row)
    return return_list


def show_available_products(db):
    """
        Return a dictionary with each product listed infor
        :param db: MongoDB
        :retun in a dict: product_id, description, product_type, quantity_available
    """
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database connects here
            db = mongo.connection.HB_Norton_DB

    products_available = {}

    for product in db.products.find():
        if int(product["quantity_available"]) > 0:

            products_dict = {"description": product["description"],
                             "product_type": product["product_type"],
                             "quantity_available": product['quantity_available']}

            products_available[product["product_id"]] = products_dict
    return products_available


def show_rentals(db, product_id):
    """
        Return information from user who have rented products on product_id
        Used MongoDB aggregate() framework methods I found online
        : param db: MongoDB
        : param product_id: proudctid
        : return: user_id, name, address, phone_number, email
    """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.HB_Norton_DB

        # Aggretion framework used in MongoDB
        output_list = list(db.rentals.aggregate([
            {'$match':
                {'product_id': product_id}},
            {'$lookup':
                {'from': "customers",
                 'localField': "user_id",
                 'foreignField': "user_id",
                 'as': "cust"}},
            {'$project':
                {'_id': 0,
                 'user_id': 1,
                 'name': '$cust.name',
                 'address': '$cust.address',
                 'phone_number': '$cust.phone_number',
                 'email': '$cust.email'}}]))
        return(output_list)


def drop_db_data(collection):
    """
        Deletes the collections from MongoDB
        :param db: MongoDB
        :return: MongoDB empty with no collection names
    """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.HB_Norton_DB
        db[collection].drop()
        return True


class db_thread(Thread):
    """
        Create subclass that inputs csv contents through multiple threads
        Queue import helps info be exhchanged safely between multiple threads.

    """

    def __init__(self, queue, collection_name, csv_file):
        self.queue = queue
        self.collection_name = collection_name
        self.csv_file = csv_file
        super().__init__()  # Inherits from superclass MongoDBConnection

    # Define a run method in our class
    # Will be executed when start() is called in import_data()
    def run(self):
        start_time = time.clock()
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.HB_Norton_DB

            db_collection = db[self.collection_name]
            start_count = db_collection.count()
            db_list = csv_list(self.csv_file)
            db_errors_in_list = 0
            for item in db_list:
                try:
                    db.collection.insert_one(item)
                except:  # What exception could I call here?
                    db_errors_in_list += 1
        output_list = (self.collection_name, db_collection.count() - start_count(),
                       start_count, db_collection.count(), time.clock() - start_time)

        self.queue.put(output_list) # Put output_list in queue
        self.queue.task_done()  # Formerly enqueued task is complete
        return None


def import_data(directory_name, customers_csv, products_csv, rentals_csv):
    """
        Takes the csv file data into the queue and threads them into MongoDB
        param: directory_name, customers_csv, products_csv, rentals_csv
        return: records added to db
    """

    data_input_queue = Queue.Queue()

    # Each csv file thread
    # Customers thread
    customers_thread_clock_start = time.clock()
    customers_thread = db_thread(data_input_queue, 'customers', customers_csv)
    customers_thread_clock_end = time.clock() - customers_thread_clock_start
    print("Customers thread took %s seconds\n" % str(customers_thread_clock_end))

    # Products thread
    products_thread_clock_start = time.clock()
    products_thread = db_thread(data_input_queue, 'products', products_csv)
    products_thread_clock_end = time.clock() - products_thread_clock_start
    print("Products thread took %s seconds\n" % str(products_thread_clock_end))

    # Rentals thread
    rentals_thread_clock_start = time.clock()
    rentals_thread = db_thread(data_input_queue, 'rentals', rentals_csv)
    rentals_thread_clock_end = time.clock() - rentals_thread_clock_start
    print("Rentals thread took %s seconds\n" % str(rentals_thread_clock_end))

    # Append each thread into list
    threads = []
    threads.append(customers_thread)
    threads.append(products_thread)
    threads.append(rentals_thread)
    # Start threads activiity
    for thread in threads:
        thread.start()

    # Block all items in the queue until all have been grabbed and processed
    data_input_queue.join()

    # Output each thread list from the queue into one
    data_output = []
    for item in range(len(threads)):  # Possible comprehension?
        data_output.append(data_input_queue.get())

    return data_output


if __name__ == '__main__':
    # import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    new_start_time = time.clock()
    print(import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv'))
    new_end_time = new_start_time - time.clock()
    print("It took %s for the program to run" % str(new_end_time))

    # Drops db data if needed
    drop_data_response = input("Drop data?")
    if drop_data_response.upper() == 'Y':
        drop_db_data('products')
        drop_db_data('customers')
        drop_db_data('rentals')
        print("Data Has Been Dropped")
