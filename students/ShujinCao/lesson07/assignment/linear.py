from pymongo import MongoClient
import pandas as pd
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

def list_renter_info(rented_product_id):
    mongo = MongoDBConnection()
    renters = {}

    with mongo:
        db = mongo.connection.media
        rentals = db.rentals.find({"product_id": f"{rented_product_id}"})
        if rentals:
            for i in rentals:
                renter = db.customers.find_one({"user_id": f"{i['user_id']}"})
                user_id = renter.pop('user_id')
                renters[user_id] = {**renter}
        return renters

def list_available_products():
    mongo = MongoDBConnection()
    output = {}

    with mongo:
        db = mongo.connection.media
        all_prod = db.products.find()
        for i in all_prod:
            if int(i["quantity_available"]) > 0:
                p_id = i['product_id']
                output[p_id] = {**i}
    return output

def main_upload_data(f_product, f_customer, f_rental):

    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        product_df = pd.read_csv(f_product)
        customer_df = pd.read_csv(f_customer)
        rental_df = pd.read_csv(f_rental)

        x_product, x_customer, x_rental = db["products"], db["customers"], db["rentals"]
        data = [product_df, customer_df, rental_df]

        [upload_data(x, y) for x, y in zip([x_product, x_customer, x_rental],
                                           data)]


def upload_data(x, data):
    mongo = MongoDBConnection()
    result = []

    with mongo:
        for i in range(len(data)):
            data = data.astype(str)
            value = dict(data.loc[i])
            result.append(value)
        x.insert_many(result)

if __name__ == "__main__":
    start_time = time.time()
    main_upload_data("products.csv", "customers.csv", "rentals.csv")
    print("--- %s seconds ---" % (time.time() - start_time))
    print(list_available_products())
    print(list_renter_info("prd005"))
