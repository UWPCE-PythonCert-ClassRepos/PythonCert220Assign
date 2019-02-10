"""
Tests for Lesson 05 Assignment
MongoDB
"""

import pytest
import database as d


@pytest.fixture(scope="function")
def mongo_database():
    mongo = d.MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        yield db

        d.clear_data(db)


def test_import_csv():
    rentals_list = d.import_csv("rentals.csv")

    assert {'product_id': 'prd002', 'user_id': 'user008'} in rentals_list
    assert len(rentals_list) == 9


def test_import_data(mongo_database):
    result = d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    assert result == ((10, 10, 9), (0, 0, 0))




# def show_available_products(db):
#     """
#     Returns a dictionary for each product listed as available.
#     :param db: MongoDB
#     :return: Dictionary with product_id, description, product_type, quantity_available.
#     """
#
#     available_products = {}
#
#     for product in db.products.find():
#         if int(product["quantity_available"]) > 0:
#
#             product_dict = {"description": product["description"],
#                             "product_type": product["product_type"],
#                             "quantity_available": product["quantity_available"]}
#
#             available_products[product["product_id"]] = product_dict
#
#     return available_products
#
#
# def show_rentals(db, product_id):
#     """
#     Returns a dictionary with user information from users who have rented products matching the product_id.
#     :param db: MongoDB
#     :param product_id: product id
#     :return: user_id, name, address, phone_number, email
#     """
#
#     customer_info = {}
#
#     for rental in db.rentals.find():
#         if rental["product_id"] == product_id:
#             customer_id = rental["user_id"]
#
#             customer_record = db.customers.find_one({"user_id": customer_id})
#
#             customer_dict = {"name": customer_record["name"],
#                              "address": customer_record["address"],
#                              "phone_number": customer_record["phone_number"],
#                              "email": customer_record["email"]}
#
#             customer_info[customer_id] = customer_dict
#
#     return customer_info
#
#
# def clear_data(db):
#     """
#     Delete data in MongoDB.
#     :param db: MongoDB
#     :return: Empty MongoDB.
#     """
#     db.products.drop()
#     db.customers.drop()
#     db.rentals.drop()
#
#
