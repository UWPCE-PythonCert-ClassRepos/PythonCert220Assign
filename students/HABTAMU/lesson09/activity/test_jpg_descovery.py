'''
Tests for the database.py module
'''


from pathlib import Path
import jpg_discovery
from pymongo import MongoClient
from pytest import fixture

TEST_DATABASE_NAME = "inventory_test"


@fixture(autouse=True)
def setup_teardown():
    ''' Fixture to execute before and after tests '''
    mongo = jpg_discovery.MongoDBConnection()
    with mongo:
        db = mongo.connection.get_database(name=TEST_DATABASE_NAME)
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
    result = jpg_discovery.import_data(parent_path, 'products.csv', 'customers.csv', 'rentals.csv', database_name=TEST_DATABASE_NAME)
    print(TEST_DATABASE_NAME)
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
