import logging
from pymongo import MongoClient
class MongoDBConnection(object):
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
    def calculate_availability(product_list, rental_list):
        for product in product_list:
            count = 0
            for rental in rental_list:
                if rental["product_id"] == product["product_id"]:
                 count += 1
                 product_available = int(product["quantity_available"]) - count
                 product["quantity_available"] = product_available
        return product_list

    def make_product_dict(prod_available_list):
        fields = ["description", "product_type", "quantity_available"]
        product_values_dict = {}
        product_dict = {}
        for product in prod_available_list:
            product_values_dict = {}
            for field in fields:
                product_values_dict[field] = product[field]
                if product["quantity_available"] > 0:
                    product_dict[product["product_id"]] = product_values_dict
        return product_dict

    def return_user_ids(rental_list):
        return [rental["user_id"] for rental in rental_list]

    def make_customer_dict(user_list):
        fields = ["name", "address", "phone_number", "email"]
        customer_values_dict = {}
        customer_dict = {}
        for customer in user_list:
            customer_values_dict = {}
            for field in fields:
                customer_values_dict[field] = customer[field]
                customer_dict[customer["user_id"]] = customer_values_dict
        return customer_dict
    def import_data(directory, product_file, customer_file, rental_file):
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.furniture
            files = [product_file, customer_file, rental_file]
            added_count_list=[]
            error_count_list = []
            for file in files:
                with open(os.path.join(directory, file)) as csv_file:
                    csv_dict = csv.DictReader(csv_file, delimiter=',')
                     collection = db[file.replace(".csv", "")]
                     try:
                        result = collection.insert_many(csv_dict)
                        added_count_list.append(len(result.inserted_ids))
                        error_count_list.append(0)
                    except BulkWriteError as bwe:
                        error_count_list.append(1)
                        logging.error(bwe)
                        return (tuple(added_count_list),tuple(error_count_list))
    def show_available_products():
        pass
    def show_available_products():
        mongo = MongoDBConnection()
    def show_rentals():
        with mongo:
            db = mongo.connection.furniture
            product_collection = db["product_data"]
            rental_collection = db["rental_data"]
            product_list = list(product_collection.find())
            rental_list = list(rental_collection.find())
            product_available_list = calculate_availability(product_list, rental_list)
            product_dict = make_product_dict(product_available_list)
        return product_dict

     def show_rentals(prod_id):
        mongo = MongoDBConnection()
        user_list = []
        with mongo:
            db = mongo.connection.furniture
            rental_collection = db["rental_data"]
            customer_collection = db["customer_data"]
            rental_list = list(rental_collection.find({"product_id": prod_id}))
            users = return_user_ids(rental_list)
            for user in users:
                user_list.append(customer_collection.find_one({'user_id': user}))
                customer_dict = make_customer_dict(user_list)
        return customer_dict