"""
Tests for Lesson 10 Assignment
Metaprogramming with MongoDB
"""

import pytest
import database as d

# pylint: disable-msg=missing-docstring
# pylint: disable-msg=line-too-long
# pylint: disable-msg=invalid-name
# pylint: disable-msg=protected-access
# pylint: disable-msg=redefined-outer-name


@pytest.fixture(scope="function")
def mongo_database():
    """
    Creates a MongoDB for testing.
    """
    mongo = d.MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        test_utilities = d.Database()

        yield (db, test_utilities)

        test_utilities.clear_data(db)


def test_import_csv(mongo_database):
    rentals_list = mongo_database[1]._import_csv("rentals_10.csv")

    example = {"user_id": "C000001", "name": "Shea Boehm", "address": "3343 Sallie Gateway",
               "phone_number": "508.104.0644 x4976", "email": "Alexander.Weber@monroe.com", "product_id": "P000003"}

    assert example in rentals_list
    assert len(rentals_list) == 10


def test_import_data(mongo_database):
    result = mongo_database[1].import_data(mongo_database[0], "", "products_10.csv", "customers_10.csv", "rentals_10.csv")

    assert result == ((10, 10, 10), (0, 0, 0))


def test_show_available_products(mongo_database):
    mongo_database[1].import_data(mongo_database[0], "", "products_10.csv", "customers_10.csv", "rentals_10.csv")

    result = mongo_database[1].show_available_products(mongo_database[0])

    assert len(result) == 10
    assert "P000004" in result
    assert "P000012" not in result


def test_show_rentals(mongo_database):
    mongo_database[1].import_data(mongo_database[0], "", "products_10.csv", "customers_10.csv", "rentals_10.csv")

    result = mongo_database[1].show_rentals(mongo_database[0], "P000003")

    assert len(result) == 3
    assert list(result.keys()) == ["C000001", "C000003", "C000009"]


def test_clear_data(mongo_database):
    mongo_database[1].import_data(mongo_database[0], "", "products_10.csv", "customers_10.csv", "rentals_10.csv")
    result = mongo_database[0].list_collection_names()

    assert result == ["products", "rentals", "customers"]

    mongo_database[1].clear_data(mongo_database[0])
    result2 = mongo_database[0].list_collection_names()

    assert result2 == []
