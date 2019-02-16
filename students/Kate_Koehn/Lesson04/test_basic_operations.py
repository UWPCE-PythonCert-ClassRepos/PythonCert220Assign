from basic_operations import add_customer, batch_add_customer, search_for_customer, delete_customer, list_active_customers, update_customer_credit
from customer_model import Customers
from create_customer import create_tables
import pytest

ok_customer1 = {"customer_id": "C000000",
                "first_name" : "Rickey",
                "last_name" : "Shanahan",
                "home_address" : "337 Eichmann Locks",
                "phone_number" : "+1(615)598-8649 x975",
                "email_address" : "Jessy@myra.net",
                "status" : "Active",
                "credit_limit" : "237"}


ok_customer2 = {"customer_id": "C000001",
                "first_name" : "Shea",
                "last_name" : "Boehm",
                "home_address" : "3343 Sallie Gateway",
                "phone_number" : "+1(508)104-0644 x4976",
                "email_address" : "Alexander.Weber@monroe.com",
                "status" : "Inactive",
                "credit_limit" : "461"}


ok_customer3 = {"customer_id": "C000002",
                "first_name" : "Blanca",
                "last_name" : "Bashirian",
                "home_address" : "0193 Malvina Lake",
                "phone_number" : "+1(240)014-9496 x08349",
                "email_address" : "Joana_Nienow@guy.org",
                "status" : "Active",
                "credit_limit" : "689"}


@pytest.fixture(scope="function")
def database_connection():
    database = create_tables()
    yield database_connection
    print("Delete database")
    database.drop_tables(Customers)


def test_add_ok_customer(database_connection):
    add_customer(**ok_customer2)
    test_customer = Customers.get(Customers.customer_id == "C000001")
    assert test_customer.email_address == "Alexander.Weber@monroe.com"


def test_add_batch_customer(database_connection):
    batch_add_customer("customer.csv")
    test_customer = Customers.get(Customers.customer_id == "C000000")
    assert test_customer.email_address == "Jessy@myra.net"

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
    add_customer(**ok_customer3)
    assert list_active_customers() == 2


def test_update_customer_credit_limit_if_customer_exists(database_connection):
    add_customer(**ok_customer2)

    update_customer_credit("C000001", "500")
    updated_customer = Customers.get(Customers.customer_id == "C000001")

    assert updated_customer.credit_limit == 500


def test_update_customer_credit_limit_if_customer_does_not_exist(database_connection):
    with pytest.raises(ValueError):
        update_customer_credit("C000001", "500")
