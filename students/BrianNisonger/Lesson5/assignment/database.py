import os
import csv
import logging
from pymongo import MongoClient

class MongoDBConnection(object):
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def import_data(directory,product_file,customer_file,rental_file):
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.furniture
        files=[product_file,customer_file,rental_file]
        added_count_list=[]
        error_count_list=[]
        for file in files:
            with open(os.path.join(directory,file)) as csv_file:
                csv_dict = csv.DictReader(csv_file, delimiter=',')
                collection = db[file.replace(".csv","")]
                result = collection.insert_many(csv_dict)
                added_count=result("insertedCount")
                error_count=0
                added_count_list.append(added_count)
                error_count_list.append(error_count)
    return added_count_list,error_count_list
    
    def show_available_products():
        pass
    
    def show_rentals():
        pass