"""
    Create Database Using MongoDB
"""
import csv
from pymongo import MongoClient
import time
import csv


class MongoDBConnection():
    """ Set up MongoDB Connection and then close it"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ Windows needs to connect to host IP Address """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """ Closes Database Connecton"""
        self.connection.close()


def timed_function(func):
    """
    This function times stuff
    """
    def decorate_func(*args, **kwargs)
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        if total_time > 0:
            time_str = f'{func.__nam__},{total_time}\n'
            with open("timing.csv", "a") as file:
                file.write(time_str)
        return result


class Time_stuff(type):
    """
        Example used from website we viewed online
    """
    def__new__(cls, name, bases, attr):
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(
                    value) is types.MethodType:
                attr[name] = time_func(value)
            return super(Time_stuff, cls).__new__(cls, name, bases, attr)


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)


def csv_list(file):
    return_list = []
    with open('sample_csv_files/' + file, encoding='utf-8-sig') as csv_file:
        file_input = csv.DictReader(csv_file)
        for row in file_input:
            return_list.append(row)
    return return_list


def import_data(directory_name, customers_csv, products_csv, rentals_csv):
    """
        Takes directory and 3 csv files to imput data into MongoDB

    """
    # # Customers Collection in db
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.HB_Norton_DB

        #Refactor at some point - reduce repetition
        product_collection = db['products']
        product_list = csv_list(products_csv)
        product_list_count = len(product_list)
        product_list_errors = 0
        for item in product_list:
            try:
                product_collection.insert_one(item)
            except:
                product_list_errors += 1

        customer_collection = db['customers']
        customer_list = csv_list(customers_csv)
        customer_list_count = len(customer_list)
        customer_list_errors = 0
        for item in customer_list:
            try:
                customer_collection.insert_one(item)
            except:
                customer_list_errors += 1

        rental_collection = db['rentals']
        rental_list = csv_list(rentals_csv)
        rental_list_count = len(rental_list)
        rental_list_errors = 0
        for item in rental_list:
            try:
                rental_collection.insert_one(item)
            except:
                rental_list_errors += 1

        import_data_added = (product_list_count - product_list_errors,
                             customer_list_count - customer_list_errors,
                             rental_list_count - rental_list_errors)
        import_data_errors = (product_list_errors,
                              customer_list_errors,
                              rental_list_errors)

        return import_data_added, import_data_errors


def show_available_products(db):
    """
        Return a dictionary with each product listed infor
        :param db: MongoDB
        :retun in a dict: product_id, description, product_type, quantity_available
    """
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database connects here
            db = mongo.connection.HB_Norton_DB

    products_available = {}

    for product in db.products.find():
        if int(product["quantity_available"]) > 0:

            products_dict = {"description": product["description"],
                             "product_type": product["product_type"],
                             "quantity_available": product['quantity_available']}

            products_available[product["product_id"]] = products_dict
    return products_available


def show_rentals(db, product_id):
    """
        Return a dictionary with information from user who have rented products on product_id
        : param db: MongoDB
        : param product_id: proudctOid
        : return: user_id, name, address, phone_number, email
    """
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database connects here
        db = mongo.connection.HB_Norton_DB

    customer_data = {}

    for rental in db.rentals.find():
        if rental["product_id"] == product_id:
            customer_id = rental["user_id"]

            customer_data_record = db.customers.find_one({"user_id": customer_id})

            customer_dict = {"name": customer_data_record["name"],
                             "address": customer_data_record["address"],
                             "phone_number": customer_data_record["phone_number"],
                             "email": customer_data_record["email"]}

            customer_data[customer_id] = customer_dict
    return customer_data


def drop_database_data(collection):
    """
        Deletes the collections from MongoDB
        :param db: MongoDB
        :return: MongoDB empty with no collection names
    """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.HB_Norton_DB
        db[collection].drop()
        return True


if __name__ == '__main__':
    import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    drop_data_response = input("Drop data?")
    if drop_data_response.upper() == 'Y':
        drop_database_data('products')
        drop_database_data('customers')
        drop_database_data('rentals')
        print("Data Dropped")
