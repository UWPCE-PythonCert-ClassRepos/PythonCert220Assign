import os
import time
import pytest

import config
from basic_operations import add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers, batch_add_customers
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

@pytest.fixture(scope='module')
def setup_database(request):
    create_database()
    def remove_database():
        os.remove('test.db')
    request.addfinalizer(remove_database)


def test_create_database(setup_database):
    assert os.path.isfile('test.db')


def test_add_customer_good(setup_database):
    add_customer(**OK_CUSTOMER)
    test_customer = Customer.get(Customer.customer_id == OK_CUSTOMER['customer_id'])
    assert test_customer.email_address == OK_CUSTOMER['email_address']
    del test_customer


def test_add_customer_bad(setup_database):
    bad_customer = dict(OK_CUSTOMER)
    bad_customer['customer_id'] = 'BX654321'
    bad_customer['credit_limit'] = '$40'
    with pytest.raises(ValueError):
        add_customer(**bad_customer)


def test_batch_add_customers(setup_database):
    customer_file = 'customer.csv'
    batch_add_customers(customer_file)
    test_customer = Customer.get(Customer.customer_id == 'C009999')
    assert test_customer.name == 'Nora'

def test_batch_add_customers_nofile():
    customer_file = "file_that_does_not_exist.csv"
    with pytest.raises(FileNotFoundError):
        batch_add_customers(customer_file)


def test_search_customer_good(setup_database):
    found_customer = search_customer('BX123456')
    assert found_customer['phone number'] == OK_CUSTOMER['phone_number']

def test_search_customer_bad(setup_database):
    found_customer = search_customer('BX999999')
    print(found_customer)
    assert found_customer == {}

def test_update_customer_credit(setup_database):
    update_customer_credit(OK_CUSTOMER['customer_id'], 2000)
    credit_customer = Customer.get(Customer.customer_id == OK_CUSTOMER['customer_id'])
    assert credit_customer.credit_limit == 2000

def test_update_customer_credit_no_customer(setup_database):
    with pytest.raises(ValueError):
        update_customer_credit('BX999999', 2000)

def test_list_active_customers(setup_database):
    count_of_customers = list_active_customers()
    assert count_of_customers == Customer.select().count()

def test_delete_customer(setup_database):
    customer_count = Customer.select().count()
    delete_customer(OK_CUSTOMER['customer_id'])
    assert Customer.select().count() == customer_count - 1
