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
    rentals_list = d._import_csv("rentals.csv")

    assert {'product_id': 'prd002', 'user_id': 'user008'} in rentals_list
    assert len(rentals_list) == 9


def test_import_data(mongo_database):
    result = d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    assert result == ((10, 10, 9), (0, 0, 0))


def test_show_available_products(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    result = d.show_available_products(mongo_database)

    assert len(result) == 7
    assert "prd001" in result
    assert "prd002" not in result


def test_show_rentals(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    result = d.show_rentals(mongo_database, "prd005")
    assert len(result) == 2

    assert list(result.keys()) == ["user001", "user003"]


def test_clear_data(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    result = mongo_database.list_collection_names()
    assert result == ["products", "rentals", "customers"]

    d.clear_data(mongo_database)
    result2 = mongo_database.list_collection_names()
    assert result2 == []
