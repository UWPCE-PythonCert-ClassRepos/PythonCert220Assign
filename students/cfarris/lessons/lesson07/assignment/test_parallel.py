#!/usr/bin/env Python3

'''
Pytest for parallel.py
'''

# pylint: disable-msg=redefined-outer-name
# pylint: disable-msg=invalid-name
# pylint: disable-msg=too-many-locals

from pymongo import MongoClient
import pytest
from parallel import (import_data,
                      _read_csv,
                      show_avail_products,
                      show_rentals,
                      check_redundancy)


class MongoDBConnection():
    """Connect to MongoDB"""

    def __init__(self, host='127.0.0.1', port=27017):

        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


@pytest.fixture(scope="function")
def set_up_connection():
    """sets up mongoDB connection for eeach test"""

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.test_hp_norton
        yield db
        db.rentals_db.drop()
        db.customers_db.drop()
        db.products_db.drop()


def test__read_csv(set_up_connection):
    """
    def _read_csv(db, collection, csv_file, dict_of_values, start_time):
    Tests read csv function is able to pull in a csv and return a dictionary
    That has the header for column as key and the value from row as value
    """
    db = set_up_connection
    rentals_db = db['rentals_db']
    data_list = []
    result = _read_csv(db, rentals_db, 'rentals.csv', data_list)
    assert result[0][0] == 9
    assert result[0][1] == 0
    assert result[0][2] == 9


def test_import_data(set_up_connection):
    """
    Tests main function which intakes a dict of names
    and csv files, and creates a collection based on
    value and adds documents from csv file to that collection.
    This test tests that Main returns the three collections.
    (products_db, rentals_db, customers_db)
    """

    customers = 'customers.csv'
    products = 'products.csv'
    db = set_up_connection
    result = import_data(db, customers, products)
    assert result[0][:3] == (10, 0, 10)
    assert result[1][:3] == (10, 0, 10)


def test_show_avail_products(set_up_connection):
    """
    tests whether show available products works.
    Is dependent on having a products_db
    """

    db = set_up_connection
    products_db = db['products_db']
    _read_csv(db, products_db, 'products.csv')
    results = show_avail_products(db)
    print(results)
    assert results == {'prd001': {'description': '60-inch TV stand',
                                  'product_type': 'livingroom',
                                  'quantity_available': '3'},
                       'prd003': {'description': 'Acacia kitchen table',
                                  'product_type': 'kitchen',
                                  'quantity_available': '7'},
                       'prd004': {'description': 'Queen bed',
                                  'product_type': 'bedroom',
                                  'quantity_available': '10'},
                       'prd005': {'description': 'Reading lamp',
                                  'product_type': 'bedroom',
                                  'quantity_available': '20'},
                       'prd006': {'description': 'Portable heater',
                                  'product_type': 'bathroom',
                                  'quantity_available': '14'},
                       'prd008': {'description': 'Smart microwave',
                                  'product_type': 'kitchen',
                                  'quantity_available': '30'},
                       'prd010': {'description': '60-inch TV',
                                  'product_type': 'livingroom',
                                  'quantity_available': '3'}}


def test_show_rentals(set_up_connection):
    """
    Tests show_rentals function which accepts a
    product_id as a parameter, queries rentals_db
    retrieves the customer_id and then queries
    the customer_db to retrieve the customers contact
    information. This function returns a dictionary
    with the product_id as key, and the customers
    name, phone number, address, and email as
    the value. The db object Id, product id and zip code are
    omitted from the return dictionary.
    """

    db = set_up_connection
    rentals_db = db['rentals_db']
    customers_db = db['customers_db']
    _read_csv(db, rentals_db, 'rentals.csv')
    _read_csv(db, customers_db, 'customers.csv')
    results = show_rentals(db, 'prd002')
    assert results == {'user008': {'name': 'Shirlene Harris',
                                   'address': '4329 Honeysuckle Lane',
                                   'phone_number': '206-279-5340',
                                   'email': 'harrisfamily@gmail.com'},
                       'user005': {'name': 'Dan Sounders',
                                   'address': '861 Honeysuckle Lane',
                                   'phone_number': '206-279-1723',
                                   'email': 'soundersoccer@mls.com'}}


def test_check_redundancy(set_up_connection):
    """
    test check redundancy. Note, this isn't linked
    to any function in database.py
    False means user010 is already in db.
    """

    db = set_up_connection
    customers_db = db['customers_db']
    _read_csv(db, customers_db, 'customers.csv')
    results = check_redundancy(db, 'user_id', 'user010', db.customers_db)
    assert results == False
