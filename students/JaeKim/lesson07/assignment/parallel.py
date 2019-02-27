import os
import csv
from pymongo import MongoClient
import threading
import datetime
from multiprocessing.pool import ThreadPool
from time import sleep


class MongoDBConnection():
    '''
    Mongo connection
    '''

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def cleanup():
    '''
    Used to cleanup mongo collections

    :return:
    '''
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        [i.drop() for i in [database.products, database.customers, database.rentals]]


def import_data(directory_name, product_file, rentals_file):
    '''
    Imports CSV files and uses threading to load them concurrently

    :param directory_name:
    :param product_file:
    :param customer_file:
    :param rentals_file:
    :return:
    '''
    mongo = MongoDBConnection()

    pool = ThreadPool(processes=3)

    with mongo:
        database = mongo.connection.media
        products_csv, rentals_csv = (os.path.join(directory_name, filename) for filename in
                                                   (product_file, rentals_file))

        products_data = csv.reader(open(products_csv, encoding='utf-8-sig'))
        rentals_data = csv.reader(open(rentals_csv, encoding='utf-8-sig'))

        collection_products, collection_rentals = database['products'], database['rentals']
        data = [products_data, rentals_data]

        records_inserted = [pool.apply_async(_insert_data, (collection, data)).get() for collection, data in
                   zip([collection_products, collection_rentals], data)]

        print(records_inserted)

        pool.close()
        pool.join()

    return records_inserted


def import_data_customers(directory_name, customer_file):
    mongo = MongoDBConnection()

    pool = ThreadPool(processes=3)

    with mongo:
        database = mongo.connection.media
        customers_csv = os.path.join(directory_name, customer_file)
        customers_data = csv.reader(open(customers_csv, encoding='utf-8-sig'))

        collection_customers = database['customers']

        records_inserted = pool.apply_async(_insert_data, (collection_customers, customers_data)).get()

        print(records_inserted)

        pool.close()
        pool.join()

    return records_inserted


def _insert_data(collection, data):
    '''
    Internal method to insert data set into a collection

    :param collection:
    :param data:
    :return:
    '''
    mongo = MongoDBConnection()
    iterproducts = iter(data)
    headers = next(iterproducts)
    result = []

    with mongo:
        for i in data:
            value = dict(zip(headers, i))
            result.append(value)

        collection.insert_many(result)

        return len(result) + 1

def show_available_products():
    '''
    Lists available products with a quantity of 1

    :return:
    '''
    result = {}
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        available_products = database.products.find()

        for i in available_products:
            if int(i['quantity_available']) >= 1:
                product_id = i['product_id']

                for e in '_id', 'product_id':
                    i.pop(e, None)
                result[product_id] = {**i}

    return result


def show_rentals(product_id):
    '''
    Returns product detail given a product id

    :param product_id:
    :return:
    '''
    renters = {}
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        results = database.rentals.find({'product_id': '{}'.format(product_id)})

        if results:
            for r in results:
                renter = database.customers.find_one({'user_id': '{}'.format(r['user_id'])})
                user_id = renter.pop('user_id', None)
                renter.pop('_id')
                renters[user_id] = {**renter}

        return renters

if __name__ == "__main__":
    pool = ThreadPool(processes=3)
    start = datetime.datetime.now()

    mongo = MongoDBConnection()
    import_products_rentals = pool.apply_async(import_data("", "products.csv", "rentals.csv"))
    import_customers =  pool.apply_async(import_data_customers("", "customers.csv"))

    pool.close()
    pool.join()
    runtime = (start - datetime.datetime.now())

    print('import_products_rentals', import_products_rentals)
    print('import_customers', import_customers)

    print(show_available_products())
    # print(show_rentals(3))
    # # cleanup()