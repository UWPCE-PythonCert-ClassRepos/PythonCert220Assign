import os
import csv
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
        products_csv = os.path.join(directory_name, product_file)
        customer_csv = os.path.join(directory_name, customer_file)
        rentals_csv = os.path.join(directory_name, rentals_file)

        products_data = csv.reader(open(products_csv, encoding='utf-8-sig'))
        customers_data = csv.reader(open(customer_csv, encoding='utf-8-sig'))
        rentals_data = csv.reader(open(rentals_csv, encoding='utf-8-sig'))

        collection_products, collection_customers, collection_rentals = database['products'], database['customers'], database['rentals']
        data = [products_data, customers_data, rentals_data]

        [_insert_data(x, y) for x, y in zip([collection_products, collection_customers, collection_rentals], data)]


def _insert_data(collection, data):
    mongo = MongoDBConnection()
    iterproducts = iter(data)
    headers = next(iterproducts)
    result = []

    with mongo:
        for i in data:
            value = dict(zip(headers, i))
            result.append(value)

        collection.insert_many(result)

def show_available_products():
    result = {}
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        available_products = database.products.find()

        for i in available_products:
            if int(i['quantity_available']) > 1:
                product_id = i['product_id']

                for e in '_id', 'product_id':
                    i.pop(e, None)
                result[product_id] = {**i}

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
                user_id = renter.pop('user_id', None)
                renter.pop('_id')
                renters[user_id] = {**renter}

        return renters


if __name__ == "__main__":
    mongo = MongoDBConnection()
    import_data("", "products.csv", "customers.csv", "rentals.csv")
    print(show_available_products())
    print(show_rentals(3))
    cleanup()
