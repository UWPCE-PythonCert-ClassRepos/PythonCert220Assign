"""
Tests for Lesson 07 Assignment
Concurrency & Async Programming
"""

import pytest
import parallel as d

# pylint: disable-msg=invalid-name
# pylint: disable-msg=redefined-outer-name
# pylint: disable-msg=missing-docstring
# pylint: disable-msg=protected-access


@pytest.fixture(scope="function")
def mongo_database():
    """
    Creates a MongoDB.
    """
    mongo = d.MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        yield db

        d.clear_data(db)


def test_import_csv():
    products_list = d._import_csv("products.csv")

    assert len(products_list) == 9999


def test_add_bulk_data(mongo_database):
    result = d._add_bulk_data(mongo_database.rentals, "", "rentals.csv")

    assert result[0] == 9999
    assert result[1] == 0
    assert result[2] == 9999
    assert isinstance(result[3], float)


def test_import_data(mongo_database):
    result = d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")

    assert result[0][0] == 9999
    assert result[0][1] == 0
    assert result[0][2] == 9999
    assert isinstance(result[0][3], float)

    assert result[1][0] == 9999
    assert result[1][1] == 0
    assert result[1][2] == 9999
    assert isinstance(result[1][3], float)


def test_show_available_products(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")
    result = d.show_available_products(mongo_database)

    assert len(result) == 9999
    assert "P000001" in result
    assert "P010999" not in result


def test_show_rentals(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")
    result = d.show_rentals(mongo_database, "P000004")

    assert len(result) == 2
    assert list(result.keys()) == ["C000002", "C000004"]


def test_clear_data(mongo_database):
    d.import_data(mongo_database, "", "products.csv", "customers.csv", "rentals.csv")
    result = sorted(mongo_database.list_collection_names())
    assert result == ["customers", "products", "rentals"]

    d.clear_data(mongo_database)
    result2 = mongo_database.list_collection_names()
    assert result2 == []
