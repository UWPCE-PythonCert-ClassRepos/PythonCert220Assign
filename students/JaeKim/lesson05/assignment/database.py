import os
import csv
<<<<<<< HEAD
from pymongo import MongoClient


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


def cleanup():
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        [i.drop() for i in [database.products, database.customers, database.rentals]]


def import_data(directory_name, product_file, customer_file, rentals_file):
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
=======
import pymongo


class MongoDB():
    def __init__(self, address='127.0.0.1', port=27017, database='db'):
        self.mongo_client = pymongo.MongoClient("mongodb://{}:{}/".format(address, port))
        self.mongo_db = self.mongo_client[database]
        self.products = self.mongo_db["products"]
        self.customers = self.mongo_db["customers"]
        self.rentals = self.mongo_db["rentals"]

        self.collections = [self.products, self.customers, self.rentals]

    def cleanup(self):
        [i.drop() for i in [self.products, self.customers, self.rentals]]

    def import_data(self, directory_name, product_file, customer_file, rentals_file):
>>>>>>> ceec382e03dae1bff50204a507d3dad8e5fcdc78
        products_csv = os.path.join(directory_name, product_file)
        customer_csv = os.path.join(directory_name, customer_file)
        rentals_csv = os.path.join(directory_name, rentals_file)

        products_data = csv.reader(open(products_csv, encoding='utf-8-sig'))
        customers_data = csv.reader(open(customer_csv, encoding='utf-8-sig'))
        rentals_data = csv.reader(open(rentals_csv, encoding='utf-8-sig'))

<<<<<<< HEAD
        collection_products, collection_customers, collection_rentals = database['products'], database['customers'], database['rentals']
        data = [products_data, customers_data, rentals_data]

        [_insert_data(x, y) for x, y in zip([collection_products, collection_customers, collection_rentals], data)]


def _insert_data(collection, data):
    mongo = MongoDBConnection()
    iterproducts = iter(data)
    headers = next(iterproducts)
    result = []

    with mongo:
=======
        data = [products_data, customers_data, rentals_data]
        [self._insert_data(x, y) for x, y in zip(self.collections, data)]

    def _insert_data(self, collection, data):
        iterproducts = iter(data)
        headers = next(iterproducts)

        result = []
>>>>>>> ceec382e03dae1bff50204a507d3dad8e5fcdc78
        for i in data:
            value = dict(zip(headers, i))
            result.append(value)

        collection.insert_many(result)

<<<<<<< HEAD

def show_available_products():
    result = {}
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        available_products = database.products.find()
=======
    def show_available_products(self):
        result = {}
        available_products = self.products.find()
>>>>>>> ceec382e03dae1bff50204a507d3dad8e5fcdc78

        for i in available_products:
            if int(i['quantity_available']) > 1:
                product_id = i['product_id']

                for e in '_id', 'product_id':
                    i.pop(e, None)
                result[product_id] = {**i}

<<<<<<< HEAD
    return result


def show_rentals(product_id):
    renters = {}
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        results = database.rentals.find({'product_id': '{}'.format(product_id)})

        if results:
            for r in results:
                renter = database.customers.find_one({'user_id': '{}'.format(r['user_id'])})
=======
        return result

    def show_rentals(self, product_id):
        renters = {}
        results = self.rentals.find({'product_id': '{}'.format(product_id)})
        if results:
            for r in results:
                renter = self.customers.find_one({'user_id': '{}'.format(r['user_id'])})
>>>>>>> ceec382e03dae1bff50204a507d3dad8e5fcdc78
                user_id = renter.pop('user_id', None)
                renter.pop('_id')
                renters[user_id] = {**renter}

        return renters


if __name__ == "__main__":
<<<<<<< HEAD
    mongo = MongoDBConnection()
    import_data("", "products.csv", "customers.csv", "rentals.csv")
    print(show_available_products())
    print(show_rentals(3))
    cleanup()
=======
    mongo = MongoDB()
    mongo.import_data("", "products.csv", "customers.csv", "rentals.csv")

    print(mongo.show_available_products())
    print(mongo.show_rentals(3))

    mongo.cleanup()
>>>>>>> ceec382e03dae1bff50204a507d3dad8e5fcdc78
