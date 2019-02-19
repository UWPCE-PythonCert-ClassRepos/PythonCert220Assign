from basic_operations import search_for_customer, delete_customer, list_active_customers, update_customer_credit, batch_add_customer
from customer_model import Customers
from create_customer import create_tables
import pytest

ok_customer1 = ("C000000",
                "Rickey",
                "Shanahan",
                "337 Eichmann Locks",
                "+1(615)598-8649 x975",
                "Jessy@myra.net",
                "Active",
                "237")

ok_customer2 = ("C000001",
                "Shea",
                "Boehm",
                "3343 Sallie Gateway",
                "+1(508)104-0644 x4976",
                "Alexander.Weber@monroe.com",
                "Inactive",
                "461")


@pytest.fixture(scope="function")
def database_connection():
    database = create_tables()
    yield database_connection
    print("Delete database")
    database.drop_tables(Customers)

# all tests need to be updated for tuples instead of dictionaries
def test_add_ok_customer(database_connection):
    batch_add_customer(ok_customer1)
    test_customer = Customers.get(Customers[1] == ok_customer1[0])
    assert test_customer[4] == ok_customer1[3]


# def test_add_batch_customer(database_connection):
#     batch_add_customer("furniture_data.csv")
#     test_customer = Customers.get(Customers.customer_id == )

#
# def test_credit_limit_float(database_connection):
#     bad_customer = dict(ok_customer1)
#     bad_customer["credit_limit"] = "$40"
#
#     with pytest.raises(ValueError):
#         add_customer(**bad_customer)
#
#
# def test_search_for_customer_when_customer_exists(database_connection):
#     add_customer(**ok_customer1)
#     test_customer = Customers.get(Customers.customer_id == ok_customer1["customer_id"])
#     assert search_for_customer(test_customer.customer_id)['email_address'] == ok_customer1["email_address"]
#
#
# def test_search_for_customer_when_customer_does_not_exist(database_connection):
#     assert search_for_customer(ok_customer1["customer_id"]) == {}
#
#
# def test_delete_customer_from_database(database_connection):
#     add_customer(**ok_customer1)
#     delete_customer(Customers.get(Customers.customer_id == ok_customer1["customer_id"]))
#
#     deleted = search_for_customer(ok_customer1["customer_id"])
#     assert deleted == {}
#
#
# def test_list_active_customers(database_connection):
#     add_customer(**ok_customer1)
#     assert list_active_customers() == 1
#     add_customer(**ok_customer2)
#     assert list_active_customers() == 2
#
#
# def test_update_customer_credit_limit_if_customer_exists(database_connection):
#     add_customer(**ok_customer2)
#
#     update_customer_credit("W54Hi66", "800")
#     updated_customer = Customers.get(Customers.customer_id == "W54Hi66")
#
#     assert updated_customer.credit_limit == 800