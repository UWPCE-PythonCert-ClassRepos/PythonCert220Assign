"""
creates database with customer info and product info
"""
#TODO do timing of this function and the linear function I still need to write
#TODO split files to linear.py and parallel():
#TODO return a list of tuples for customer and one for product with record count, record count before, record count after, time taken to run module

from threading import Thread
import csv
import queue as Queue
from pymongo import MongoClient
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


def show_available_products():
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        output_dict = list(database.products.find({'quantity_available': {'$gt':'0'}}, {"_id": 0}))

        print(output_dict)
        return(output_dict)

def show_rentals(product_id):
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        output_list = list(database.rentals.aggregate([
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
                'email': '$cust.email'}}

                ]))
        return(output_list)


def print_mdb_collection(collection_name):
    for doc in collection_name.find({}):
        print(doc)

def csv_list(file):
    return_list = []
    with open('sample_csv_files/' + file, encoding='utf-8-sig') as csv_file:
        file_input = csv.DictReader(csv_file)
        for row in file_input:
            return_list.append(row)
    return return_list

def drop_database_data(collection):
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        database[collection].drop()
        return True
        #add something here if it cant be found


class database_thread(Thread):

    def __init__(self, q, collection_name, csv_file):
        self.queue = q
        self.collection_name = collection_name
        self.csv_file = csv_file
        super().__init__()

    def run(self):
        start_time = time.clock()
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.media

            database_collection = database[self.collection_name]
            starting_count = database_collection.count()
            database_list = csv_list(self.csv_file)
            database_list_errors = 0
            for item in database_list:
                try:
                    database_collection.insert_one(item)
                except:
                    database_list_errors += 1
        output_list = (self.collection_name, database_collection.count() - starting_count, starting_count, database_collection.count(), time.clock()-start_time)
        self.queue.put(output_list)
        self.queue.task_done()
        return None


def import_data(dir_name, product_csv, customer_csv, rental_csv):


    data_entry_queue = Queue.Queue()

    product_thread = database_thread(data_entry_queue, 'products', product_csv)
    customer_thread = database_thread(data_entry_queue, 'customers', customer_csv)
    rental_thread = database_thread(data_entry_queue, 'rental', rental_csv)

    threads = []
    threads.append(product_thread)
    threads.append(customer_thread)
    threads.append(rental_thread)
    for thread in threads:
        thread.start()

    data_entry_queue.join()

    output = []
    for item in range(len(threads)):
        output.append(data_entry_queue.get())

    return output


if __name__ == '__main__':
    new_start = time.clock()
    print(import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv'))
    new_end = time.clock()
    print("Program run time:" + str(new_end - new_start))
