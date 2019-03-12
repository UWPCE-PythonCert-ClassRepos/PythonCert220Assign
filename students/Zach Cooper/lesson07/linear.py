"""
    Create Database In Linear State Using MongoDB
"""
import csv
import time
from pymongo import MongoClient
from timeit import timeit


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
        products_start_time = time.time()
        product_collection = db['products']
        product_list = csv_list(products_csv)
        product_list_count = len(product_list)
        product_list_errors = 0
        for item in product_list:
            try:
                product_collection.insert_one(item)
            except:
                product_list_errors += 1
        products_end_time = time.time() - products_start_time
        print("It took %s seconds to import products.csv file" % products_end_time)


        customers_start_time = time.time()
        customer_collection = db['customers']
        customer_list = csv_list(customers_csv)
        customer_list_count = len(customer_list)
        customer_list_errors = 0
        for item in customer_list:
            try:
                customer_collection.insert_one(item)
            except:
                customer_list_errors += 1
        customers_end_time = time.time() - customers_start_time
        print("It took %s seconds to import customers.csv file" % customers_end_time)

        rentals_start_time = time.time()
        rental_collection = db['rentals']
        rental_list = csv_list(rentals_csv)
        rental_list_count = len(rental_list)
        rental_list_errors = 0
        for item in rental_list:
            try:
                rental_collection.insert_one(item)
            except:
                rental_list_errors += 1
        rentals_end_time = time.time() - rentals_start_time
        print("It took %s seconds to import rentals.csv file" % rentals_end_time)


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
        db = mongo.connection.HB_Norton_DB

        output_list = list(db.rentals.aggregate([
            {'$match':
                {'product_id': product_id}},
            {'$lookup':
                {'from': "customers",
                 'localField': "user_id",
                 'foreignField': "user_id",
                 'as': "cust"}},
            {'$project':
                {'_id': 0,
                 'user_id': 1,
                 'name': '$cust.name',
                 'address': '$cust.address',
                 'phone_number': '$cust.phone_number',
                 'email': '$cust.email'}}
                ]))
        return(output_list)


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
    # import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    print(timeit("import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')", globals=globals(), number=1))

    drop_data_response = input("Drop data?")
    if drop_data_response.upper() == 'Y':
        drop_database_data('products')
        drop_database_data('customers')
        drop_database_data('rentals')
        print("Data Has Been Dropped")