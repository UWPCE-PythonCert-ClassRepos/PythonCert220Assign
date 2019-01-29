"""
Tests for basic_operations
"""

import customer_model as cm
import basic_operations as bo
import peewee as pw
import pytest

customer1 = {"customer_id": "1", "first_name": "Fred", "last_name": "Flintstone",
             "home_address": "301 Cobblestone Way, Bedrock, 70777", "phone_number": "928-635-2600",
             "email_address": "fred@hotmail.com", "active_status": True, "credit_limit": 100.00}

customer2 = {"customer_id": "2", "first_name": "Barney", "last_name": "Rubble",
             "home_address": "303 Cobblestone Way, Bedrock, 70777", "phone_number": "928-635-2700",
             "email_address": "barney@aol.com", "active_status": False, "credit_limit": 50.00}

customer3 = {"customer_id": "3", "first_name": "Wilma", "last_name": "Flintstone",
             "home_address": "301 Cobblestone Way, Bedrock, 70777", "phone_number": "928-635-2600",
             "email_address": "wilma@hotmail.com", "active_status": True, "credit_limit": 100.00}

customer4 = {"customer_id": "4", "first_name": "Betty", "last_name": "Rubble",
             "home_address": "303 Cobblestone Way, Bedrock, 70777", "phone_number": "928-635-2700",
             "email_address": "barney@aol.com", "active_status": False, "credit_limit": 50.00}


def clear_database():
    cm.database.drop_tables([
        cm.Customer
    ])

    cm.database.close()


def create_empty_database():
    clear_database()

    cm.database.create_tables([
        cm.Customer
    ])

    cm.database.close()


def test_add_customers():
    create_empty_database()
    bo.add_customer(**customer1)
    bo.add_customer(**customer2)

    test_customer1 = cm.Customer.get(cm.Customer.customer_id == "1")
    assert test_customer1.first_name == customer1["first_name"]
    assert test_customer1.last_name == customer1["last_name"]

    test_customer2 = cm.Customer.get(cm.Customer.customer_id == "2")
    assert test_customer2.first_name == customer2["first_name"]
    assert test_customer2.last_name == customer2["last_name"]

    clear_database()


def test_add_customers_duplicate():
    create_empty_database()
    bo.add_customer(**customer1)

    with pytest.raises(pw.IntegrityError):
        bo.add_customer(**customer1)

    clear_database()


def create_sample_database():
    clear_database()

    cm.database.create_tables([
        cm.Customer
    ])
    bo.add_customer(**customer1)
    bo.add_customer(**customer2)
    bo.add_customer(**customer3)
    bo.add_customer(**customer4)

    cm.database.close()


def test_search_customer():
    create_sample_database()

    test_customer = bo.search_customer("3")

    assert test_customer["email_address"] == customer3["email_address"]

    clear_database()


def test_search_customer_missing():
    create_sample_database()

    assert bo.search_customer("8") == dict()

    clear_database()


def test_delete_customer():
    create_sample_database()

    number_of_customer2s = (cm.Customer.select().where(cm.Customer.customer_id == "2").count())
    assert number_of_customer2s == 1

    bo.delete_customer("2")
    new_number_of_customer2s = (cm.Customer.select().where(cm.Customer.customer_id == "2").count())
    assert new_number_of_customer2s == 0

    clear_database()


def test_delete_customer_missing():
    create_sample_database()

    number_of_customers = (cm.Customer.select().count())
    assert number_of_customers == 4

    bo.delete_customer("9")

    new_number_of_customers = (cm.Customer.select().count())
    assert new_number_of_customers == 4

    clear_database()


def test_update_customer_credit():
    create_sample_database()

    bo.update_customer_credit("1", 5000)

    target_customer = cm.Customer.get(cm.Customer.customer_id == 1)

    assert target_customer.credit_limit == 5000

    clear_database()


def test_update_customer_credit_missing():
    create_sample_database()

    with pytest.raises(pw.DoesNotExist):
        bo.update_customer_credit("44", 300)

    clear_database()


def test_list_active_customers():
    create_sample_database()

    assert bo.list_active_customers() == 2

    clear_database()


def test_list_active_customers_empty():
    create_empty_database()

    assert bo.list_active_customers() == 0

    clear_database()
