"""
    Tests for database.py in lesson 05
"""
import pytest
import database as data_base


@pytest.fixture(scope="function")
def mongo_db():
    mongo = data_base.MongoDBConncetion()

    with mongo:
        db = mongo.conncetion.HB_Norton_DB


        data_base.clear

def test_csv_import():
    customers_list = data_base.csv_import("customers.csv")

    assert {"user_id": "user001", "name": "Elisa Miles", "addres": "4490 Union Street",
            "zip_code": "98109", "phone": "206-922-0882", "email": "elisa.miles@yahoo.com"}
    assert len(customers_list) == 10

def test_import_data(mongo_db):
    result = data_base(mongo_db, "", "customers.csv", "products.csv", "rentals.csv")

    assert len ==((10, 10, 9))

def test_show_available_proudcts(mongo_db):
    data_base.import_data(mongo_db, "", "customers.csv", "products.csv", "rentals.csv")
    
    result = data_base.show_available_proudcts(mongo_db)

    assert "prd001" in result

def test_show_rentals(mongo_db):
    data_base.import_data(mongo_db, "", "customers.csv", "products.csv", "rentals.csv")

    result = data_base.show_rentals(mongo_db, "prd004")
    assert len(result) == 2