"""
tests
"""
import pytest
from basic_operations import *
from customer_model import Customer

good_customer2 = {
    'customer_id': '2WDIll8IDO',
    'name': 'Suzie2',
    'last_name': 'Edgar',
    'home_address': '122 Brown St., Seattle, WA 98121',
    'phone_number': '122-333-444',
    'email_address': '2suzie@gmail.com',
    'status': 'Active',
    'credit_limit': 40.00}

good_customer = {
    'customer_id': 'WDIll8IDO',
    'name': 'Suzie',
    'last_name': 'Edgar',
    'home_address': '122 Brown St., Seattle, WA 98121',
    'phone_number': '123-333-444',
    'email_address': 'suzie@gmail.com',
    'status': 'Active',
    'credit_limit': 40.00}

bad_customer = {'customer_id':'8675309',
                'name': 'Jenny',
                'last_name': 'Igotyonumber',
                'home_address': 'Beverly Hills Plaza, Compton, Ca. 90210',
                'phone_number': '198-765-4321',
                'email_address': 'Jenny_Igotyonumber@gmail.com',
                'status': 'Active',
                'credit_limit': 40.00}

def test_add_customer():
    add_customer(**good_customer)
    test_customer = Customer.get(Customer.customer_id==good_customer['customer_id'])
    assert test_customer.email_address == good_customer['email_address']

def test_credit_limit_float():
    bad_customer['credit_limit'] = '$40'
    with pytest.raises(ValueError):
        add_customer(**bad_customer)

def test_search_customer():
    '''
	test search func
    '''
    returned_customer = search_customer(good_customer['customer_id'])
    assert returned_customer['name'] == 'Suzie'

def test_search_csv():
    c = search_customer('C000000')
    assert c['name'] == 'Rickey'


def test_search_customer_not_found():
    '''
	test search func if not found
    '''
    returned_customer = search_customer('111111')
    assert returned_customer == {}

def test_delete_customer():
    '''
    test delete func
    '''
    add_customer(**good_customer2)
    test_customer = Customer.get(Customer.customer_id == good_customer2['customer_id'])
    assert test_customer.email_address == good_customer2['email_address']
    deleted = delete_customer(test_customer.customer_id)
    assert deleted == 'customer deleted'

def test_update_customer_credit():
    '''
    test update credit limit func
    '''
    update_customer_credit(good_customer['customer_id'],
                           50)
    p = Customer.get(Customer.customer_id == good_customer['customer_id'])
    assert p.credit_limit == 50

def test_list_active_customers():
    '''
    test count active customers func
    '''
    assert list_active_customers() == 6954

