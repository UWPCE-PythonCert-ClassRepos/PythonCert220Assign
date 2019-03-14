"""
creates database with customer info and product info
"""

import csv
from pymongo import MongoClient
import time
import inspect
from metatimer import Timed


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

class Database_Class(metaclass=Timed):

    def __init__(self, collection, collection_csv):
        self.mongo = MongoDBConnection()
        self.collection = collection
        self.csv = collection_csv

    def _csv_list(self, file):
        return_list = []
        with open('sample_csv_files/' + file, encoding='utf-8-sig') as csv_file:
            file_input = csv.DictReader(csv_file)
            for row in file_input:
                return_list.append(row)
        return return_list

    def drop_database_data(self):
        with self.mongo:
            database = self.mongo.connection.media
            database[self.collection].drop()
        return True
        #add something here if it cant be found

    def import_data(self):
        with self.mongo:
            database = self.mongo.connection.media
            mongo_coll = database[self.collection]
            mongo_list = self._csv_list(self.csv)
            mongo_list_count = len(mongo_list)
            mongo_list_errors = 0
            for item in mongo_list:
                try:
                    mongo_coll.insert_one(item)
                except:
                    #add log here for which record failed
                    mongo_list_errors += 1

            return mongo_list_count - mongo_list_errors, mongo_list_errors

    def print_mdb_collection(self):
        with self.mongo:
            database = self.mongo.connection.media

            for col in database.collection_names():
                print(col)

    def show_available_products(self):
        with self.mongo:
            database = self.mongo.connection.media

        output_dict = list(database.products.find({'quantity_available': {'$gt':'0'}}, {"_id": 0}))

        print(output_dict)
        return(output_dict)

    def show_rentals(self, product_id):
        with self.mongo:
            database = self.mongo.connection.media

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


if __name__ == '__main__':
    products = Database_Class("products", "products.csv")
    customers = Database_Class("customers", "customers.csv")
    rentals = Database_Class("rentals", "rentals.csv")
    coll_list = [products, customers, rentals]
    for coll in coll_list:
        coll.import_data()
    products.show_available_products()
    rentals.show_rentals('prd002')
    products.print_mdb_collection()
    drop_data_response = input("Drop data?")
    if drop_data_response.upper() == 'Y':
        for col in coll_list:
            coll.drop_database_data()
        print("Data Dropped")
