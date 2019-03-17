#!/usr/bin/env Python3

"""
Lesson09 part 2 Context Manager. 
MongoDB is already in a context manager, but I did a little editing
and put more things within the context manager.

This set up is only for development use. Not production
Uses Pymongo to access MongoDB database.
Imports 3 files, directs them to different collections
Retrieves information necessary for HP Norton collection
"""
import time
import csv
from pymongo import MongoClient

# pylint: disable-msg=redefined-outer-name
# pylint: disable-msg=invalid-name
# pylint: disable-msg=too-many-locals


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
        print("connection to MongoDB successfully closed...")


def print_mdb_collection(db, collection_name):
    """Prints the collection specified"""

    for doc in collection_name.find():
        print(doc)


def import_data(db, customers=None, products=None, rentals=None, start_time=0):
    """
    Adds files to collection.
    if the file/date type (k) fits into three categories
    it will be added to that collection.
    I created a thread for rentals as well,
    but commented it out to adhere to instructions.
    """

    data_list = []

    # if statements were added to facilitate testing.
    if products:
        products_db = db['products_db']
        _read_csv(db, products_db, products, data_list, start_time)

    if customers:
        customers_db = db['customers_db']
        _read_csv(db, customers_db, customers, data_list, start_time)

    if rentals:
        rentals_db = db['rentals_db']
        _read_csv(db, rentals_db, rentals, data_list, start_time)

    print("data_list: ", data_list)
    return data_list


def _read_csv(db, collection, csv_file, data_list=None, start_time=0):
    '''
    Opens csv files, creates a list of
    dictionarys with matching keys from header to values
    returns the dictionary and saves it to
    different mongodb collections based upon the
    file name given to main.
    '''

    if data_list is None:
        data_list = []

    with open(csv_file, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = True
        first_line = []
        num_processed = 0
        coll_of_dicts = []
        count_before_running = collection.count()
        for row in csv_reader:
            if header:
                header = False
                first_line = [value.strip() for value in row]
            else:
                num_processed += 1
                new_dict = {}
                str_row = []
                str_row = [value.strip() for value in row]
                for i in range(len(str_row)):
                    k = first_line[i]
                    v = str_row[i]
                    novelty_test = check_redundancy(db, k, v, collection)
                    if novelty_test:
                        new_dict[first_line[i]] = str_row[i]
                coll_of_dicts.append(new_dict)
        try:
            collection.insert_many(coll_of_dicts)
        except Exception as err:
            print("error!:", err, collection.name, coll_of_dicts)
        time_to_run = time.time() - start_time
        results = (num_processed,
                   count_before_running,
                   collection.count(),
                   time_to_run)
        print(collection.name,
              " finished: ",
              num_processed,
              count_before_running,
              collection.count(),
              time_to_run)
        data_list.append(results)
        return data_list


def check_redundancy(db, unique_identifier_key,
                     unique_identifier_value,
                     collection):
    """
    For each row to be entered into a collection,
    this checks to see if it is already there.
    I cannot get this to work.
    """

    if collection.find({unique_identifier_key:
                        unique_identifier_value}).count() > 0:
        return False
    return True


def show_avail_products(db):
    '''
    Shows rentals available to rent
    queries products_db and returns any values that aren't 0
    '''

    query = {"quantity_available": {"$gt": "0"}}
    print("\n\n***Product Availability***")
    rental_dict = {}
    for record in db.products_db.find(query):
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
    Asks user if they want to drop tables in Mongodb created by
    this program: rentals_db, customers_db, products_db
    '''

    drop_results = input("Drop all data?")
    if drop_results.upper() == 'Y':
        db.rentals_db.drop()
        db.customers_db.drop()
        db.products_db.drop()
        print("All documents were dropped from db.")


def main(start_time, db):
    '''
    runs methods within this script to add three csv files
    to their own collections
    within MongoDB named db.
    '''
    db = mongo.connection.norton_products
    import_data(db, 'customers.csv', 'products.csv', 'rentals.csv', start_time)


if __name__ == '__main__':

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.norton_products
        drop_data(db)
        start_time = time.time()
        main(start_time, db)
