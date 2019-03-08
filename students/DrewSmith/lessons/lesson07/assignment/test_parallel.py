'''
Tests for the parallel.py module
'''


from pathlib import Path
import assignment.parallel as parallel
from pymongo import MongoClient
from unittest import TestCase
import assignment.config as config
import assignment.create_customers as cc
from assignment.customers_model import Customer

class Test_Mongo(TestCase):

    def setup(self):
        ''' Fixture to execute before and after tests '''
        mongo = parallel.MongoDBConnection()
        with mongo:
            db = mongo.connection.get_database(name=config.TEST_DATABASE_NAME)
            db.drop_collection("customers")
            db.drop_collection("products")
            db.drop_collection("rentals")


    def test_import_data(self):
        '''
        Test the import_data method
        '''
        # files path is in test file parent
        parent_path = Path(__file__).parent
        result = parallel.import_product_data(parent_path, 
            'products.csv', 'contacts.csv', 'rentals.csv', database_name=config.TEST_DATABASE_NAME)

        assert len(result) == 1
        assert len(result[0]) == 3
        # record counts
        assert result[0][0] == 999
        assert result[0][1] == 990
        assert result[0][2] == 9

    def test_show_available_products(self):
        ''' Test the show_available_products function '''

        parent_path = Path(__file__).parent
        parallel.import_product_data(parent_path, 
            'products.csv', 'contacts.csv', 'rentals.csv', database_name=config.TEST_DATABASE_NAME)
        result = parallel.show_available_products(database_name=config.TEST_DATABASE_NAME)

        assert len(result) == 0

    def test_show_rentals(self):
        ''' Test the show_rentals function '''

        parent_path = Path(__file__).parent
        parallel.import_product_data(parent_path, 
            'products.csv', 'contacts.csv', 'rentals.csv', database_name=config.TEST_DATABASE_NAME)
        result = parallel.show_rentals("prd002", database_name=config.TEST_DATABASE_NAME)

        assert len(result) == 2
        assert "user008" in result
        assert "user005" in result

class Test_Sqlite(TestCase):

    def setup(self):
        ''' Fixture to execute before and after tests '''
        db = cc.get_database()
        db.drop_tables([Customer])
        db.create_tables([Customer])

    def test_add_csv_bulk(self):
        '''
        Adds the contents of the test data csv to the database
        This tests the bulk_add_customers and convert_csv methods
        '''
        parallel.bulk_add_customers(parallel.convert_csv('customers.csv'))
        assert Customer.select().count() == 10000