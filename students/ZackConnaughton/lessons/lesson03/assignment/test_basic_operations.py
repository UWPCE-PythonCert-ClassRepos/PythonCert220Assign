import os
import time
import pytest


from basic_operations import add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers
from customer_model import Customer, create_database


OK_CUSTOMER = {'customer_id': 'BX123456',
               'name': 'Thomas',
               'last_name': 'Deleon',
               'home_address': '37083 Johnson Tunnel\nLake Pamelaland, NV 54352',
               'phone_number': '1-425-555-8080',
               'email_address': 't_deleon@gmail.com',
               'status': True,
               'credit_limit': '200'
               }


def test_create_database():
    create_database()
    assert os.path.isfile('customer.db')
    os.remove('customer.db')


def test_add_customer_good():
    create_database()
    add_customer(**OK_CUSTOMER)
    test_customer = Customer.get(Customer.customer_id == OK_CUSTOMER['customer_id'])
    assert test_customer.email_address == OK_CUSTOMER['email_address']


def test_add_customer_bad():
    bad_customer = dict(OK_CUSTOMER)
    bad_customer['customer_id'] = 'BX654321'
    bad_customer['credit_limit'] = '$40'
    with pytest.raises(ValueError):
        add_customer(**bad_customer)


def test_search_customer_good():
    found_customer = search_customer('BX123456')
    assert found_customer['phone number'] == OK_CUSTOMER['phone_number']

def test_search_customer_bad():
    found_customer = search_customer('BX999999')
    print(found_customer)
    assert found_customer == {}

def test_update_customer_credit():
    update_customer_credit(OK_CUSTOMER['customer_id'], 2000)
    credit_customer = Customer.get(Customer.customer_id == OK_CUSTOMER['customer_id'])
    assert credit_customer.credit_limit == 2000

def test_update_customer_credit_no_customer():
    with pytest.raises(ValueError):
        update_customer_credit('BX999999', 2000)

def test_list_active_customers():
    count_of_customers = list_active_customers()
    assert count_of_customers == 1

def test_delete_customer():
    customer_count = Customer.select().count()
    delete_customer(OK_CUSTOMER['customer_id'])
    assert Customer.select().count() == customer_count - 1
