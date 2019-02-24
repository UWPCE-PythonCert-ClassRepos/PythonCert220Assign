from pymongo import MongoClient
import pandas as pd


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
    renters = []

    with mongo:
        db = mongo.connection.media
        rentals = db.rentals.find({"product_id": f"{rented_product_id}"})
        if rentals:
            for i in rentals:
                renter = db.customers.find_one({"user_id": f"{i['user_id']}"})
                reters.append(renter)
        print(renters)

def list_available_products():
    mongo = MongoDBConnection()
    output = []

    with mongo:
        db = mongo.connection.media
        all_prod = db.products.find()
        for i in all_prod:
            if int(i["quantity_available"]) > 0:
                output.append(i)
        print(output)

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
    import pdb; pdb.set_trace()
    mongo = MongoDBConnection()
    result = []

    with mongo:
        for i in range(len(data)):
            value = dict(data.iloc[i])
            result.append(value)
        x.insert_many(result)

if __name__ == "__main__":
    main_upload_data("products.csv", "customers.csv", "rentals.csv")
    list_available_products()
