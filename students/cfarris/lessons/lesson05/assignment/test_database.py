#!/usr/bin/env Python3

'''
Pytest for database.py
'''
from pymongo import MongoClient
import pytest
from database import read_csv, import_data, show_avail_products, show_rentals, check_redundancy


coll_dict = {'customers': 'customers.csv',
             'products': 'products.csv',
             'rentals': 'rentals.csv'
             }


class MongoDBConnection(object):
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


def test_read_csv(set_up_connection):
    """
    Tests read csv function is able to pull in a csv and return a dictionary
    That has the header for column as key and the value from row as value
    """
    result = read_csv('rentals.csv')
    print(result)
    assert result == [{'product_id': 'prd003', 'user_id': 'user004'},
                      {'product_id': 'prd002', 'user_id': 'user008'},
                      {'product_id': 'prd002', 'user_id': 'user005'},
                      {'product_id': 'prd005', 'user_id': 'user001'},
                      {'product_id': 'prd010', 'user_id': 'user002'},
                      {'product_id': 'prd007', 'user_id': 'user002'},
                      {'product_id': 'prd006', 'user_id': 'user003'},
                      {'product_id': 'prd005', 'user_id': 'user003'},
                      {'product_id': 'prd001', 'user_id': 'user010'}]




def test_import_data(set_up_connection):
    """
    Tests main function which intakes a dict of names and csv files, and 
    creates a collection based on value and adds documents from csv file to that
    collection. 
    This test tests that Main returns the three collections 
    (products_db, rentals_db, customers_db)
    """
    db = set_up_connection
    result = import_data(db, coll_dict)
    print(result)
    assert result == (9, 10, 10)


def test_show_avail_products(set_up_connection):
    """
    tests whether show available products works. Is dependent on having a products_db
    This te
    """
    db = set_up_connection
    result = import_data(db, coll_dict)
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
    Tests show_rentals function which accepts a product_id as a parameter, queries rentals_db
    retrieves the customer_id and then queries the customer_db to retrieve the customers contact
    information. This function returns a dictionary with the product_id as key, and the customers
    name, phone number, address, and email as the value. The db object Id, product id and zip code are
    omitted from the return dictionary.
    """
    db = set_up_connection
    result = import_data(db, coll_dict)
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
    test check redundancy. Note, this isn't linked to any function in database.py
    I ran out of time. This is to be added later.
    """
    db = set_up_connection
    result = import_data(db, coll_dict)
    results = check_redundancy(db,'user_id', 'user010', db.customers_db)
    assert results == False
