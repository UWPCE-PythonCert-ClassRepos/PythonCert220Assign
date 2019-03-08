"""
Tests for the HP Norton database functions
"""
import pytest
import database


@pytest.fixture(scope='function', autouse=True)
def setup_database(request):
    test_entry, test_errors = database.import_data('main_mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    def remove_database():
        database.drop_database_data('products')
        database.drop_database_data('customers')
        database.drop_database_data('rentals')
    request.addfinalizer(remove_database)

def test_import_data():
    #should return 2 tuples, 1 with record count of the number of products, customers and rentals added
    #and a count of any errors that occurred
    records_added, record_errors = database.import_data('test mongo', 'products.csv', 'customers.csv', 'rentals.csv')
    assert records_added == (10, 10, 9)
    assert record_errors == (1, 0, 0)


def test_show_available_products():
    #returns dictionary of available products with prod id, desc, type, qty
    available_products = database.show_available_products()
    assert (item for item in available_products if item['product_id'] == 'prd004')
    assert (item for item in available_products if item['description'] == 'Popcorn machine')


def test_show_rentals():
    """
    returns dict with user id, name, address, phone number, email
    """
    prod2_rentals = database.show_rentals('prd002')
    assert (item for item in prod2_rentals if item['name'] == 'Shirlene Harris')
    prod00X_rentals = database.show_rentals('prodX')
    assert prod00X_rentals == []
