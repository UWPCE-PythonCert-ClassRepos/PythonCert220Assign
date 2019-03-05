import os
import pytest
from pymongo import MongoClient
from database import csv
from database import import_data
from database import show_available_products
from database import show_rentals
from database import calculate_availability
from database import make_product_dict
from database import return_user_ids
from database import make_customer_dict

# Connect to the MongoDB, change the connection string per my MongoDB environment
client = MongoClient(port=27017)
# Set the db object to point to the business database
db=client.business
# this is import my  directory name three csv files as input
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)

class MongoDBConnection(object):
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

@pytest.fixture
def setup_db(request):
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.furniture
        db.product_data.drop()
        db.customer_data.drop()
        db.rental_data.drop()
        import_data("dat", "product_data.csv", "customer_data.csv","rental_data.csv")
        def cleanup():
            db.product_data.drop()
            db.customer_data.drop()
            db.rental_data.drop()
            request.addfinalizer(cleanup)

@pytest.fixture
def _show_available_products():
    product_dict = {'prd1001': {'description': '60 inch TV stand','product_type': 'livingroom','quantity_available': 2},
        'prd1003': {'description': 'Hobart Stand Mixer','product_type': 'kitchen','quantity_available': 10}}
    return product_dict

@pytest.fixture
def _show_rentals():
    rental_dict = {'user1001': {'name': 'Elisa Miles','address': '4490 Union Street','phone_number': '206-922-0882','email': 'elisa.miles@yahoo.com'},
        'user1002': {'name': 'Maya Data','address': '4936 Elliot Avenue','phone_number': '206-777-1927','email': 'mdata@uw.edu'}}
    return rental_dict

def test_import_data():
    added, error = import_data("dat", "product_data.csv", "customer_data.csv","rental_data.csv")
    assert added == (3, 3, 5)
    assert error == (0, 0, 0)

def test_calculate_availability():
    rental_list = [{"user": 1001, "product_id": "prd1001"}, {"user": 1002, "product_id": "prd1002"}]
    product_list = [{"product_id": "prd1001","quantity_available": "10"}, {"product_id": "prd1002","quantity_available": "2"}]
    product_calculated = calculate_availability(product_list, rental_list)
    for product in product_calculated:
        if product["product_id"] == "prd1001":
            assert product["quantity_available"] == 9

def test_make_product_dict():
    product_dict_list = product_list = [{"product_id": "prd1001","quantity_available": 10,"description": "blah","product_type": "yes","garbage_field": "yuck"}]
     assert make_product_dict(product_dict_list) == {'prd1001': {"description": "blah","product_type": "yes","quantity_available": 10}}
     product_list = [{"product_id": "prd1001","quantity_available": 0,"description": "blah","product_type": "yes","garbage_field": "yuck"}]
     assert make_product_dict(product_dict_list) == {}

def test_return_user_ids():
    rental_list = rental_list = [{"user_id": '1001',"product_id": "prd1001"}, {"user_id": '1002',"product_id": "prd1002"}]
    assert return_user_ids(rental_list) == ['1001', '1002']
def test_make_customer_dict():
    user_list = [{"user_id": "1001","name": "Jim","address": "1234","phone_number": "555","email": "something","stuff": "stuff"}]
    assert make_customer_dict(user_list) == {'1001': {"name": "Jim","address": "1234","phone_number": "555","email": "something"}}

def test_show_available_products(setup_db, _show_available_products):
    available_dict = show_available_products()
    assert available_dict == _show_available_products

def test_show_rentals(setup_db, _show_rentals):
    rental_dict = show_rentals('prd1002')
    assert rental_dict == _show_rentals



