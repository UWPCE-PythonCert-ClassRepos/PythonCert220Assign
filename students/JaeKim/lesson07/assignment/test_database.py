import database as d
import pytest

@pytest.fixture(scope="function")
def mongo_database():
    """
    Creates a MongoDB.
    :return:
    """
    mongo = d.MongoDBConnection()
    with mongo:
        db = mongo.connection.media

        yield db

        d.cleanup()


def test_import_data():
    d.import_data("", "products.csv", "customers.csv", "rentals.csv")
    results = d.show_available_products()

    assert results['1']['description'] == "Playstation 4"
    assert results['2']['description'] == "Xbox One"
    assert results['4']['description'] == "Coca-Cola 20 oz"
    assert results['5']['description'] == "Mountain Dew"
    assert results['6']['description'] == "Pepsi"


def test_show_rentals(mongo_database):
    results = d.show_rentals(3)

    assert results['1']['name'] == "Jae Kim"
    assert results['3']['name'] == "Bernie Sanders"


def test_show_available_products(mongo_database):
    results = d.show_available_products()

    with pytest.raises(KeyError):
        # An item with 1 quantity
        results['3']