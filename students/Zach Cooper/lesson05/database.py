"""
    Create Database Using Mongo
"""
import csv
from pymongo import MongoClient
import os

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

### First Attempt Failure
"""
    Need to create a single function that can open each csv file
"""
# def main():
#     mongo = MongoDBConnection()

#     with mongo:
#         # mongodb database connects here
#             db = mongo.connection.HB_Norton_DB

#         # collection name in database
#         # customers = db["customers"]


#     # print_mdb_collection('customers')
#     """
#         Use db.collection_name.find().pretty() to queary data results in clean format
#     """
#     filename_cust = "/Users/Zach/UWPYTHON/PythonCert220Assign/students/Zach Cooper/lesson05/customers.csv"
#     with open(filename_cust) as csvfile_customers:
#         csvreader = csv.reader(csvfile_customers, delimiter=',', quotechar='|')
#         for row in csvreader:
#             db.customers.insert_one({'user_id': row[0], 'name': row[1], 'address': row[2], 'area_code': row[3], 'phone_number': row[4], 'email': row[5]})
            

#     filename_products = "/Users/Zach/UWPYTHON/PythonCert220Assign/students/Zach Cooper/lesson05/products.csv"
#     with open(filename_products) as csvfile:
#         csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#         for row in csvreader:
#             db.products.insert_one({'product_id': row[0], 'description': row[1], 'product_type': row[2], 'quantity_available': row[3]})


#     # print_mdb_collection('rentals')
#     filename_rentals = "/Users/Zach/UWPYTHON/PythonCert220Assign/students/Zach Cooper/lesson05/rentals.csv"
#     with open(filename_rentals) as csvfile:
#         csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#         for row in csvreader:
#             db.rentals.insert_one({'product_id': row[0], 'user_id': row[1]})


#     # Related Data
#     """
#         Subract one count because of the header column in each file
#     """
#     customer_count = (db.customers.find().count() - 1)
#     products_count = (db.products.find().count() - 1) #### How to I get sum of total products. Sum isnt part of MongoDB
#     rentals_count = (db.rentals.find().count() - 1)
#     print("Total number of Customer is %s.\n"
#           "Total number of Products is %s.\n"
#           "Total number of Rentals is %s.\n" % (customer_count, products_count, rentals_count))

#     ### ERROR COUNT
#     # Using the count() method to find the total product_types that have zero available quantities
#     total_zero_available_products = db.products.find({[3]: 0}).count()
#     print("There are %s products that have no products available" % total_zero_available_products)


# Second Attempt
# Create a csv import function to call later to open the three csv files
def csv_import(filename):
    """
        One dictionary for each row of data is returned via csv file
    """
    filename = "/Users/Zach/UWPYTHON/PythonCert220Assign/students/Zach Cooper/lesson05"
    with open(filename, newline='') as csvfile:
        dict_list = []
        csv_data = csv.reader(csvfile, "*.csv")
    

        # First line as headers
        headers = next(csv_data, None)

        # Return content in rows as a dict
        for row in csv_data:
            row_dict = {}   

            for row, column in inumerate(headers):
                row_dict[column] = row[index]

            dict_list.append(row_dict)

        return dict_list


def import_data(db, directory_name, customers_file, products_file, rentals_file):
    """
        Takes directory and 3 csv files to imput data into MongoDB

    """
    # Customers Collection in db
    customers = db["customers"]
    customers_file_path = os.path.join(directory_name, products_file)
    customers.insert_many(csv_import(customers_file_path))

    # Products Collections in db
    products = db["products"]
    products_file_path = os.path.join(directory_name, products_file)
    products.insert_many(csv_import(products_file_path))

    # Rentals Collection in db
    rentals = db["rentals"]
    rentals_file_path = os.path.join(directory_name, rentals_file)
    rentals.insert_many(csv_import(rentals_file_path))

    record_count = (db.customers.count_documents({}), db.products.count_documents({}), db.rentals.count_documents({}))

    return record_count


def show_available_products(db):
    """
        Return a dictionary with each product listed infor
        :param db: MongoDB
        :retun in a dict: product_id, description, product_type, quantity_available
    """

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

    customer_data = {}

    for rental in db.rentals.find():
        if rental["product_id"] == products_id:
            custemer_id = rental["user_id"]

            customer_data_record = db.customers.find_one({"user_id": customer_id})

            customer_dict = {"name": customer_data_record["name"],
                             "address": customer_data_record["address"],
                             "phone_number": customer_data_record["phone_number"],
                             "email": customer_data_record["email"]}

            customer_data[customer_id] = customer_dict
    return customer_info


def clear_db_data_collection(db):
    """
        Deletes the collections from MongoDB
        :param db: MongoDB
        :return: MongoDB empty with no collection names
    """

    clear_db= input("Clear database collections? Y or N")
    if clear_db.upper() == 'Y':
        
        db.customers.drop()
        db.products.drop()
        db.rentals.drop()



if __name__ == "__main__":
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database connects here
        db = mongo.connection.HB_Norton_db



