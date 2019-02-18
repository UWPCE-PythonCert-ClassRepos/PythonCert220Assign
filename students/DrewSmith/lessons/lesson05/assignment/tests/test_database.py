'''
Tests for the database.py module
'''


from pathlib import Path
import assignment.database
from pymongo import MongoClient
from pytest import fixture
import assignment.config as config

@fixture(autouse=True)
def setup_teardown():
    ''' Fixture to execute before and after tests '''
    mongo = assignment.database.MongoDBConnection()
    with mongo:
        db = mongo.connection.get_database(name=config.TEST_DATABASE_NAME)
        db.drop_collection("customers")
        db.drop_collection("products")
        db.drop_collection("rentals")
    
    yield


def test_import_data():
    '''
    Test the import_data method
    '''
    # files path is in test file parent
    parent_path = Path(__file__).parent.parent
    result = assignment.database.import_data(parent_path, 
        'products.csv', 'customers.csv', 'rentals.csv', database_name=config.TEST_DATABASE_NAME)
    print(config.TEST_DATABASE_NAME)
    assert False

    assert len(result) == 2
    assert len(result[0]) == 3
    # record counts
    assert result[0][0] == 10
    assert result[0][1] == 10
    assert result[0][2] == 9
    # error counts
    assert result[1][0] == 0
    assert result[1][1] == 0
    assert result[1][2] == 0

def test_show_available_products():
    ''' Test the show_available_products function '''

    parent_path = Path(__file__).parent.parent
    assignment.database.import_data(parent_path, 
        'products.csv', 'customers.csv', 'rentals.csv', database_name=config.TEST_DATABASE_NAME)
    result = assignment.database.show_available_products(database_name=config.TEST_DATABASE_NAME)

    assert len(result) == 7
    assert "prd010" in result

def test_show_rentals():
    ''' Test the show_rentals function '''

    parent_path = Path(__file__).parent.parent
    assignment.database.import_data(parent_path, 
        'products.csv', 'customers.csv', 'rentals.csv', database_name=config.TEST_DATABASE_NAME)
    result = assignment.database.show_rentals("prd002", database_name=config.TEST_DATABASE_NAME)

    assert len(result) == 2
    assert "user008" in result
    assert "user005" in result
