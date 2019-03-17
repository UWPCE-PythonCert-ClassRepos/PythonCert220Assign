"""
creates database with customer info and product info
"""

import csv
from pymongo import MongoClient
import time
import inspect

def timing(func):
    def wrapper(*args, **kwargs):
        output = [func.__name__]
        collection = ""
        arguments = (inspect.getfullargspec(func))
        if [arg for arg in arguments if arg == ['collection']]:
            collection = args[0]
            start_count = (data_count(collection))
        start = time.clock()
        func(*args, **kwargs)
        output.append(time.clock() - start)
        if collection:
            end_count = data_count(collection)
            output.append(abs(end_count - start_count))
        else:
            output.append("N/A")
        csv_output(output)
    return wrapper

def csv_output(timing_info):
    with open('timings.txt', 'a') as append_file:
        append_file.write(f"{timing_info[0]},{timing_info[1]:.5f},{timing_info[2]}\n")

def data_count(collection):
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        return database[collection].count()


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

@timing
def show_available_products():
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        output_dict = list(database.products.find({'quantity_available': {'$gt':'0'}}, {"_id": 0}))

        print(output_dict)
        return(output_dict)

@timing
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

@timing
def print_mdb_collection():
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        for col in database.collection_names():
            print(col)

def csv_list(file):
    return_list = []
    with open('sample_csv_files/' + file, encoding='utf-8-sig') as csv_file:
        file_input = csv.DictReader(csv_file)
        for row in file_input:
            return_list.append(row)
    return return_list

@timing
def drop_database_data(collection):
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        database[collection].drop()
        return True
        #add something here if it cant be found

@timing
def import_data(dir_name, product_csv, customer_csv, rental_csv):
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
    import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    import_data('main_mongo', 'products2.csv', 'customers2.csv', 'rentals2.csv')
    show_available_products()
    show_rentals('prd002')
    print_mdb_collection()
    drop_data_response = input("Drop data?")
    if drop_data_response.upper() == 'Y':
        drop_database_data('products')
        drop_database_data('customers')
        drop_database_data('rentals')
        print("Data Dropped")
