from basic_operations import add_customer, search_for_customer, delete_customer, list_active_customers, update_customer_credit
from customer_model import Customers
from create_customer import create_tables
import pytest

ok_customer1 = {"customer_id" : "W54Hi45",
               "name" : "Ted",
                "last_name" : "Danson",
                "home_address" : "1600 Pennsylvania Avenue, Seattle, WA, 98101",
                "phone_number" : "205-234-1232",
                "email_address" : "ted.danson@yahoo.com",
                "status" : True,
                "credit_limit" : "40"}

ok_customer2 = {"customer_id" : "W54Hi66",
               "name" : "Gerard",
                "last_name" : "Depardieu",
                "home_address" : "1313 S Western Ave, Seattle, WA, 98101",
                "phone_number" : "232-666-7886",
                "email_address" : "frenchie@aol.com",
                "status" : True,
                "credit_limit" : "80"}


@pytest.fixture(scope="function")
def database_connection():
    database = create_tables()
    yield database_connection
    print("Delete database")
    database.drop_tables(Customers)


def test_add_ok_customer(database_connection):
    add_customer(**ok_customer1)
    test_customer = Customers.get(Customers.customer_id == ok_customer1["customer_id"])
    assert test_customer.email_address == ok_customer1["email_address"]


def test_credit_limit_float(database_connection):
    bad_customer = dict(ok_customer1)
    bad_customer["credit_limit"] = "$40"

    with pytest.raises(ValueError):
        add_customer(**bad_customer)


def test_search_for_customer_when_customer_exists(database_connection):
    add_customer(**ok_customer1)
    test_customer = Customers.get(Customers.customer_id == ok_customer1["customer_id"])
    assert search_for_customer(test_customer.customer_id)['email_address'] == ok_customer1["email_address"]


def test_search_for_customer_when_customer_does_not_exist(database_connection):
    assert search_for_customer(ok_customer1["customer_id"]) == {}


def test_delete_customer_from_database(database_connection):
    add_customer(**ok_customer1)
    delete_customer(Customers.get(Customers.customer_id == ok_customer1["customer_id"]))

    deleted = search_for_customer(ok_customer1["customer_id"])
    assert deleted == {}


def test_list_active_customers(database_connection):
    add_customer(**ok_customer1)
    assert list_active_customers() == 1
    add_customer(**ok_customer2)
    assert list_active_customers() == 2


def test_update_customer_credit_limit_if_customer_exists(database_connection):
    add_customer(**ok_customer2)

    update_customer_credit("W54Hi66", "800")
    updated_customer = Customers.get(Customers.customer_id == "W54Hi66")

    assert updated_customer.credit_limit == "800"