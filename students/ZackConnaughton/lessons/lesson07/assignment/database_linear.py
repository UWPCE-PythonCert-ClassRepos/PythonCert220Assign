"""
creates database with customer info and product info
"""
#TODO do timing of this function and the linear function I still need to write
#TODO split files to linear.py and parallel():
#TODO return a list of tuples for customer and one for product with record count, record count before, record count after, time taken to run module

import csv
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


def import_data(dir_name, product_csv, customer_csv, rental_csv):

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        start = time.clock()
        #Refactor at some point - reduce repetition
        product_collection = database['products']
        start_product_collection = product_collection.count()
        product_list = csv_list(product_csv)
        product_list_count = len(product_list)
        product_list_errors = 0
        for item in product_list:
            try:
                product_collection.insert_one(item)
            except:
                #add log here for which record failed
                product_list_errors += 1
        end_product_collection = product_collection.count()
        time_product_collection = (time.clock() - start)

        start = time.clock()
        customer_collection = database['customers']
        start_customer_collection = customer_collection.count()
        customer_list = csv_list(customer_csv)
        customer_list_count = len(customer_list)
        customer_list_errors = 0
        for item in customer_list:
            try:
                customer_collection.insert_one(item)
            except:
                customer_list_errors += 1
        end_customer_collection = customer_collection.count()
        time_customer_collection = (time.clock() - start)

        start = time.clock()
        rental_collection = database['rentals']
        start_rental_collection = rental_collection.count()
        rental_list = csv_list(rental_csv)
        rental_list_count = len(rental_list)
        rental_list_errors = 0
        for item in rental_list:
            try:
                rental_collection.insert_one(item)
            except:
                rental_list_errors += 1
        end_rental_collection = rental_collection.count()
        time_rental_collection = (time.clock() - start)

        product_output = (product_list_count, start_product_collection, end_product_collection, time_product_collection)
        customer_output = (customer_list_count, start_customer_collection, end_customer_collection, time_customer_collection)
        rental_output = (rental_list_count, start_rental_collection, end_rental_collection, time_rental_collection)

        return product_output, customer_output, rental_output


if __name__ == '__main__':
    new_start = time.clock()
    print(import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv'))
    new_end = time.clock()
    print("Program run time:" + str(new_end - new_start))
