#!/usr/bin/env Python3

"""
This set up is only for development use. Not production
Uses Pymongo to access MongoDB database.
Imports 3 files, directs them to different collections
Retrieves information necessary for HP Norton collection

Can be used as a module or stand-alone
Lacks error checking of data (due to time constraints.)
"""
import csv
from pymongo import MongoClient



class MongoDBConnection():
    """Connect to MongoDB"""
    def __init__(self, host='127.0.0.1', port=27017):

        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(db, collection_name):
    """Prints the collection specified"""
    for doc in collection_name.find():
        print(doc)


def import_data(db, coll_dict):
    """Adds files to collection. if the file/date type (k) fits into three categories
       it will be added to that collection.
    """
    for k, v in coll_dict.items():
        if k == 'rentals':
            rentals_db = db['rentals_db']
            rentals_data = read_csv(v)
            result = rentals_db.insert_many(rentals_data)

        elif k == 'customers':
            customers_db = db['customers_db']
            customers = read_csv(v)
            result = customers_db.insert_many(customers)

        elif k == 'products':
            products_db = db['products_db']
            products = read_csv(v)
            result = products_db.insert_many(products)

    return db.rentals_db.count(), db.customers_db.count(), db.products_db.count()


def read_csv(v):
    '''
    Opens csv files, creates a list of dictionarys with matching keys from header to values
    returns the dictionary and saves it to different mongodb collections based upon the
    file name given to main.
    '''
    with open(v, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = True
        first_line = []
        coll_of_dicts = []
        for row in csv_reader:
            if header:
                header = False
                first_line = [value.strip() for value in row]
            else:
                new_dict = {}
                str_row = []
                str_row = [value.strip() for value in row]
                for i in range(len(str_row)):
                    new_dict[first_line[i]] = str_row[i]
                coll_of_dicts.append(new_dict)
        return coll_of_dicts


def check_redundancy(db, unique_identifier_key, unique_identifier_value, collection):
    """
    For each row to be entered into a collection, this checks to see if it is already there.
    Not added to csv above as I ran out of time. Not implemented!
    """
    query = {unique_identifier_key : unique_identifier_value}
    query_data = collection.find(query)
    if collection.find(query).count() > 0:
        return False

    return True


def show_avail_products(db):
    '''
    Shows rentals available to rent
    queries products_db and returns any values that aren't 0
    '''
    query = {"quantity_available": {"$gt": "0"}}
    query_data = db.products_db.find(query)
    print("\n\n***Product Availability***")
    rental_dict = {}
    for record in query_data:
        prod_id = record['product_id']
        record.pop('_id')
        record.pop('product_id')
        rental_dict[prod_id] = record
        print(f'{record["description"]} has',
              f'{record["quantity_available"]}'
              f' units available to rent.')
    print("\n\n")
    return rental_dict


def show_rentals(db, prod_id):
    ''''
    Searches rentals_db collection and finds user id
    Then pulls user id customer information from customer_db
    Returns python dictionary containing id, name, address, phone, email
    '''
    query = {"product_id": prod_id}
    query_data = db.rentals_db.find(query)
    found_renters = {}
    for record in query_data:
        renters = record['user_id']
        renter_info = db.customers_db.find({"user_id": renters})
        for renter in renter_info:
            renter.pop('zip_code')
            renter.pop('user_id')
            renter.pop('_id')
            found_renters[renters] = renter

    return found_renters


def drop_data(db):
    '''
    Asks user if they want to drop tables created?

    '''
    drop_results = input("Drop all data?")
    if drop_results.upper() == 'Y':
        db.rentals_db.drop()
        db.customers_db.drop()
        db.products_db.drop()


if __name__ == '__main__':
    coll_dict = {'customers': 'customers.csv',
                 'products': 'products.csv',
                 'rentals': 'rentals.csv'
                 }

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.norton_products
        drop_data(db)
        print(import_data(db, coll_dict))
        check_redundancy(db, 'user_id', 'user010', db.customers_db)
        show_avail_products(db)
        show_rentals(db, 'prd002')
