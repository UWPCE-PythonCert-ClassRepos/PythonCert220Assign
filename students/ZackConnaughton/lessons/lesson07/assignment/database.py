"""
creates database with customer info and product info
"""

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
        output_list = (self.collection_name, database_collection.count() - starting_count, database_list_errors)
        self.queue.put(output_list)
        self.queue.task_done()
        return None

def format_output(output_raw):
    data_entered = [0, 0, 0]
    errors = [0, 0, 0]
    for row in output_raw:
        collection_name = row[0]
        if collection_name == 'products':
            data_entered[0] = row[1]
            errors[0] = row[2]
        if collection_name == 'customers':
            data_entered[1] = row[1]
            errors[0] = row[2]
        if collection_name == 'rental':
            data_entered[2] = row[1]
            errors[0] = row[2]
    print(data_entered)
    print(errors)
    return [data_entered, errors]


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

    output_raw = []
    for item in range(len(threads)):
        output_raw.append(data_entry_queue.get())

    print(output_raw)
    output = format_output(output_raw)
    return output


def import_data_old(dir_name, product_csv, customer_csv, rental_csv):

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        #Refactor at some point - reduce repetition
        product_collection = database['products']
        product_list = csv_list(product_csv)
        product_list_count = len(product_list)
        product_list_errors = 0
        for item in product_list:
            try:
                product_collection.insert_one(item)
            except:
                #add log here for which record failed
                product_list_errors += 1

        customer_collection = database['customers']
        customer_list = csv_list(customer_csv)
        customer_list_count = len(customer_list)
        customer_list_errors = 0
        for item in customer_list:
            try:
                customer_collection.insert_one(item)
            except:
                customer_list_errors += 1

        rental_collection = database['rentals']
        rental_list = csv_list(rental_csv)
        rental_list_count = len(rental_list)
        rental_list_errors = 0
        for item in rental_list:
            try:
                rental_collection.insert_one(item)
            except:
                rental_list_errors += 1

        import_data_added = (product_list_count - product_list_errors,
                             customer_list_count - customer_list_errors,
                             rental_list_count - rental_list_errors)
        import_data_errors = (product_list_errors,
                              customer_list_errors,
                              rental_list_errors)

        return import_data_added, import_data_errors


if __name__ == '__main__':
    new_start = time.clock()
    import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    new_end = time.clock()
    # drop_data_response = input("Drop data?")
    # if drop_data_response.upper() == 'Y':
    #     drop_database_data('products')
    #     drop_database_data('customers')
    #     drop_database_data('rentals')
    #     print("Data Dropped")
    # old_start = time.clock()
    # import_data_old('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    # old_end = time.clock()
    # drop_data_response = input("Drop data?")
    # if drop_data_response.upper() == 'Y':
    #     drop_database_data('products')
    #     drop_database_data('customers')
    #     drop_database_data('rentals')
    #     print("Data Dropped")
    # print('New Time %s' % (new_end - new_start))
    # print('Old Time %s' % (old_end - old_start))

    #show_available_products()
    #show_rentals('prd002')
