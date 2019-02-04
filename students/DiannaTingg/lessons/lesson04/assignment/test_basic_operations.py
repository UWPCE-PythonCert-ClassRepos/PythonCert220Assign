"""
Tests for basic_operations
"""

import peewee as pw
import pytest
import customer_model as cm
import basic_operations as bo

# pylint: disable-msg=missing-docstring
# pylint: disable-msg=redefined-outer-name
# pylint: disable-msg=unused-argument

CUSTOMER1 = {"customer_id": "1", "first_name": "Fred", "last_name": "Flintstone",
             "home_address": "301 Cobblestone Way, Bedrock, 70777", "phone_number": "928-635-2600",
             "email_address": "fred@hotmail.com", "status": "Active", "credit_limit": 100.00}

CUSTOMER2 = {"customer_id": "2", "first_name": "Barney", "last_name": "Rubble",
             "home_address": "303 Cobblestone Way, Bedrock, 70777", "phone_number": "928-635-2700",
             "email_address": "barney@aol.com", "status": "Inactive", "credit_limit": 50.00}

CUSTOMER3 = {"customer_id": "3", "first_name": "Wilma", "last_name": "Flintstone",
             "home_address": "301 Cobblestone Way, Bedrock, 70777", "phone_number": "928-635-2600",
             "email_address": "wilma@hotmail.com", "status": "Active", "credit_limit": 100.00}

CUSTOMER4 = {"customer_id": "4", "first_name": "Betty", "last_name": "Rubble",
             "home_address": "303 Cobblestone Way, Bedrock, 70777", "phone_number": "928-635-2700",
             "email_address": "barney@aol.com", "status": "Inactive", "credit_limit": 50.00}


@pytest.fixture(scope="function")
def sample_database():
    cm.DATABASE.create_tables([cm.Customer])
    bo.add_customer(**CUSTOMER1)
    bo.add_customer(**CUSTOMER2)
    bo.add_customer(**CUSTOMER3)

    yield sample_database

    cm.DATABASE.drop_tables([cm.Customer])


def test_add_customer(sample_database):
    bo.add_customer(**CUSTOMER4)

    test_customer = cm.Customer.get(cm.Customer.customer_id == "4")
    assert test_customer.first_name == CUSTOMER4["first_name"]
    assert test_customer.last_name == CUSTOMER4["last_name"]


def test_add_customer_duplicate(sample_database):
    with pytest.raises(pw.IntegrityError):
        bo.add_customer(**CUSTOMER1)


def test_search_customer(sample_database):
    test_customer = bo.search_customer("3")

    assert test_customer["email_address"] == CUSTOMER3["email_address"]


def test_search_customer_missing(sample_database):
    assert bo.search_customer("8") == {}


def test_delete_customer(sample_database):
    number_of_customer_2s = (cm.Customer.select().where(cm.Customer.customer_id == "2").count())
    assert number_of_customer_2s == 1

    bo.delete_customer("2")
    new_number_of_customer_2s = (cm.Customer.select().where(cm.Customer.customer_id == "2").count())
    assert new_number_of_customer_2s == 0


def test_delete_customer_missing(sample_database):
    with pytest.raises(pw.DoesNotExist):
        bo.delete_customer("9")


def test_update_customer_credit(sample_database):
    bo.update_customer_credit("1", 5000)

    target_customer = cm.Customer.get(cm.Customer.customer_id == 1)

    assert target_customer.credit_limit == 5000


def test_update_customer_credit_missing(sample_database):
    with pytest.raises(pw.DoesNotExist):
        bo.update_customer_credit("44", 300)


def test_list_active_customers(sample_database):
    assert bo.list_active_customers() == 2


def test_lifecycle(sample_database):
    # Delete one customer
    bo.delete_customer(CUSTOMER3["customer_id"])

    # Update customer credit
    bo.update_customer_credit("2", 300.00)

    updated_customer = cm.Customer.get(cm.Customer.customer_id == 2)
    assert updated_customer.credit_limit == 300.00

    # Search for a customer
    target_customer = bo.search_customer("1")
    assert target_customer["email_address"] == CUSTOMER1["email_address"]

    # List active customers
    assert bo.list_active_customers() == 1


@pytest.fixture(scope="function")
def csv_database():
    cm.DATABASE.create_tables([cm.Customer])
    bo.upload_csv("test_customer.csv")

    yield csv_database

    cm.DATABASE.drop_tables([cm.Customer])


def test_csv_add_customer(csv_database):
    bo.add_customer(**CUSTOMER1)

    test_customer = cm.Customer.get(cm.Customer.customer_id == "1")
    assert test_customer.phone_number == CUSTOMER1["phone_number"]

    with pytest.raises(pw.IntegrityError):
        bo.add_customer(**CUSTOMER1)


def test_csv_search_customer(csv_database):
    test_customer = bo.search_customer("C000001")

    assert test_customer["email_address"] == "Alexander.Weber@monroe.com"
    assert bo.search_customer("100") == {}


def test_csv_delete_customer(csv_database):
    bo.delete_customer("C000002")

    with pytest.raises(pw.DoesNotExist):
        bo.delete_customer("C000002")


def test_csv_update_customer_credit(csv_database):
    bo.update_customer_credit("C000003", 100)

    target_customer = cm.Customer.get(cm.Customer.customer_id == "C000003")

    assert target_customer.credit_limit == 100

    with pytest.raises(pw.DoesNotExist):
        bo.update_customer_credit("200", 200)


def test_csv_list_active_customers(csv_database):
    assert bo.list_active_customers() == 4


cm.DATABASE.close()
