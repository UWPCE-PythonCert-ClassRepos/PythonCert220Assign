"""
Tests basice_operations.py
"""

import pytest
import peewee as pw
import customer_modle as cm
from basic_operations_refactored import add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers
# from create_customer import create_tables


Customer1 = {'customer_id': 'W3434fd',
                'first_name': 'Suzie',
                'last_name': 'Edgar',
                'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
                'phone_number': '234-123-4567',
                'email_address': 'suzie@hotmail.com',
                'status': True,
                'credit_limit': 40}


Customer2 = {'customer_id': '2',
                'first_name': 'Chris',
                'last_name': 'Seefeld',
                'home_address': '301 Boston Commons Way, Salem, 98028',
                'phone_number': '123-456-4566',
                'email_address': 'Chris@hotmail.com',
                'status': True,
                'credit_limit': 200}


Customer3 = {'customer_id': '3',
                'first_name': 'Ryan',
                'last_name': 'Fermstad',
                'home_address': '808 Honolulu Way, Dimond Head, 80808',
                'phone_number': '765-432-1234',
                'email_address': 'fermy@aol.com',
                'status': False,
                'credit_limit': 300.00}


# def clear_database():
#     database.drop_tables([
#         Customer
#     ])
#     database.close()


# def create_empty_database():
#     clear_database()
#     cm.database.create_tables([
#         cm.Customer
#     ])
#     cm.database.close()


@pytest.fixture(scope="function")
def sample_database_connection():
    DATABASE = create_tables([cm.Customer])
    bo.add_customer(**Customer1)
    bo.add_customer(**Customer2)
    bo.add_customer(**Customer3)
    yield database_connection
    print("Delete database")
    database.drop_tables([cm.Customer])


def test_add_customer(sample_database_connection):

    add_customer(**Customer1)

    test_customer = cm.Customer.get(cm.Customer.customer_id == Customer1['customer_id'])
    assert test_customer.first_name == Customer1['first_name']
    assert test_customer.last_name == Customer1['last_name']
    assert test_customer.home_address == Customer1['home_address']
    assert test_customer.email_address == Customer1['email_address']
    assert test_customer.status == Customer1['status']

    add_customer(**Customer2)

    test_customer = cm.Customer.get(cm.Customer.customer_id == Customer2['customer_id'])
    assert test_customer.first_name == Customer2['first_name']
    assert test_customer.last_name == Customer2['last_name']
    assert test_customer.home_address == Customer2['home_address']
    assert test_customer.email_address == Customer2['email_address']
    assert test_customer.status == Customer2['status']


def test_credit_limit_float(sample_database_connection):
    bad_customer = dict(Customer3)
    bad_customer['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        add_customer(**bad_customer)


def test_search_customer(sample_database_connection):

    add_customer(**Customer3)
    test_customer = cm.Customer.get(cm.Customer.customer_id==Customer3['customer_id'])

    assert test_customer.email_address == Customer3['email_address']


def test_customer_non_existent(sample_database_connection):

    assert search_customer('5') == {}


def test_delete_customer(sample_database_connection):
    add_customer(**Customer3)

    customer_count = cm.Customer.select().count()
    delete_customer(cm.Customer3['customer_id'])
    assert Customer.select().count() == customer_count - 1


def test_delete_customer_missing(sample_database_connection):
    with pytest.raises(pw.DoesNotExist):
        delete_customer("12")


def test_update_customer_credit(sample_database_connection):
    add_customer(**Customer2)

    update_customer_credit("2", "700")
    updated_customer = cm.Customer.get(cm.Customer.customer_id == "2")

    assert updated_customer.credit_limit == 700


def test_update_customer_credit_missing(sample_database_connection):
    with pytest.raises(pw.DoesNotExist):
        bo.update_customer_credit("54", 500)


def test_list_active_customers(sample_database_connection):
    add_customer(**Customer1)
    add_customer(**Customer2)

    assert list_active_customers() == 2


"""
    Used help from student example for this. Couldnt figure out how to test
    a csv file since all we had above was a mock database
"""
@pytest.fixture(scope="function")
def csv_database():
    cm.DATABASE.create_tables([cm.Customer])
    upload_csv("test_customer.csv")

    yield csv_database

    cm.DATABASE.drop_tables([cm.Customer])


def test_csv_add_customer(csv_database):
    add_customer(**Customer1)

    test_customer = cm.Customer.get(cm.Customer.customer_id == "1")
    assert test_customer.phone_number == Customer1["phone_number"]

    with pytest.raises(pw.IntegrityError):
        add_customer(**Customer1)


def test_csv_search_customer(csv_database):
    test_customer = search_customer("C000001")

    assert test_customer["email_address"] == "Alexander.Weber@monroe.com"
    assert search_customer("100") == {}


def test_csv_delete_customer(csv_database):
    delete_customer("C000002")

    with pytest.raises(pw.DoesNotExist):
        delete_customer("C000002")


def test_csv_update_customer_credit(csv_database):
    update_customer_credit("C000003", 100)

    target_customer = cm.Customer.get(cm.Customer.customer_id == "C000003")

    assert target_customer.credit_limit == 100

    with pytest.raises(pw.DoesNotExist):
        update_customer_credit("200", 200)


def test_csv_list_active_customers(csv_database):
    assert list_active_customers() == 4


cm.DATABASE.close()
