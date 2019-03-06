#Tim Pauley
#Assignment 05, 
#Feb 10 2019
#Update Feb 20 2019

'''
Testing requirements

In order for your code to be evaluated, you need to create a file called 
database.py with the following functions:

import_data
    (directory_name
    , product_file
    , customer_file
    , rentals_file): This function takes a directory name three csv files 
    as input, one with product data, one with customer data and the third 
    one with rentals data and creates and populates a new MongoDB database 
    with the these data. It returns 2 tuples: the first with a record count 
    of the number of products, customers and rentals added (in that order)
    , the second with a count of any errors that occurred, in the same order.

show_available_products(): Returns a Python dictionary of products listed 
as available with the following fields:
product_id.
description.
product_type.
quantity_available.

For example:

{‘prd001’:{‘description’:‘60-inch TV stand’,’product_type’:’livingroom’
,’quantity_available’:‘3’},’prd002’:{‘description’:’L-shaped sofa’
,’product_type’:’livingroom’,’quantity_available’:‘1’}}

show_rentals(product_id): Returns a Python dictionary with the following 
user information from users that have rented products matching 
product_id:
user_id.
name.
address.
phone_number.
email.
For example:

{‘user001’:{‘name’:’Elisa Miles’,’address’:‘4490 Union Street’
,’phone_number’:‘206-922-0882’,’email’:’elisa.miles@yahoo.com’}
,’user002’:{‘name’:’Maya Data’,’address’:‘4936 Elliot Avenue’
,’phone_number’:‘206-777-1927’,’email’:’mdata@uw.edu’}}

'''

"""
Tests for Lesson 05 Assignment
MongoDB
"""

import pytest
import database as d

# pylint: disable-msg=invalid-name
# pylint: disable-msg=redefined-outer-name
# pylint: disable-msg=missing-docstring
# pylint: disable-msg=protected-access

"""
Creates MongoDB database
"""
@pytest.fixture(scope="function")
def mongo_database():

    mongo = d.MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        yield db

        d.clear_data(db)

'''
Test Import csv function
'''
def test_import_csv():
    rentals_list = d._import_csv("rentals.csv")

    assert {'product_id': 'prd002', 'user_id': 'user008'} in rentals_list
    assert len(rentals_list) == 9

'''
Test Import Data Function
'''
def test_import_data(mongo_database):
    result = d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    assert result == ((10, 10, 9), (0, 0, 0))


'''
Test show available products
'''
def test_show_available_products(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    result = d.show_available_products(mongo_database)

    assert len(result) == 7
    assert "prd001" in result
    assert "prd002" not in result

'''
Test show rentals function
'''
def test_show_rentals(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    result = d.show_rentals(mongo_database, "prd005")
    assert len(result) == 2

    assert list(result.keys()) == ["user001", "user003"]

'''
Test Clear Data Function
'''
def test_clear_data(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    result = mongo_database.list_collection_names()
    assert result == ["products", "rentals", "customers"]

    d.clear_data(mongo_database)
    result2 = mongo_database.list_collection_names()
    assert result2 == []

#End Tests