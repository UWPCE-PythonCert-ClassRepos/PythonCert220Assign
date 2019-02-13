import os
import csv
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
        products_csv = os.path.join(directory_name, product_file)
        customer_csv = os.path.join(directory_name, customer_file)
        rentals_csv = os.path.join(directory_name, rentals_file)

        products_data = csv.reader(open(products_csv, encoding='utf-8-sig'))
        customers_data = csv.reader(open(customer_csv, encoding='utf-8-sig'))
        rentals_data = csv.reader(open(rentals_csv, encoding='utf-8-sig'))

        data = [products_data, customers_data, rentals_data]
        [self._insert_data(x, y) for x, y in zip(self.collections, data)]

    def _insert_data(self, collection, data):
        iterproducts = iter(data)
        headers = next(iterproducts)

        result = []
        for i in data:
            value = dict(zip(headers, i))
            result.append(value)

        collection.insert_many(result)

    def show_available_products(self):
        result = {}
        available_products = self.products.find()

        for i in available_products:
            if int(i['quantity_available']) > 1:
                product_id = i['product_id']

                for e in '_id', 'product_id':
                    i.pop(e, None)
                result[product_id] = {**i}

        return result

    def show_rentals(self, product_id):
        renters = {}
        results = self.rentals.find({'product_id': '{}'.format(product_id)})
        if results:
            for r in results:
                renter = self.customers.find_one({'user_id': '{}'.format(r['user_id'])})
                user_id = renter.pop('user_id', None)
                renter.pop('_id')
                renters[user_id] = {**renter}

        return renters


if __name__ == "__main__":
    mongo = MongoDB()
    mongo.import_data("", "products.csv", "customers.csv", "rentals.csv")

    print(mongo.show_available_products())
    print(mongo.show_rentals(3))

    mongo.cleanup()
