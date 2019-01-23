"""
tests
"""
import pytest
from basic_operations import add_customer
from customer_model import Customer

customer_dict = {
    'customer_id': 'WDIll8IDO'.
    'name': 'Suzie',
    'last_name': 'Edgar',
    'home_address': '122 Brown St., Seattle, WA 98121',
    'phone_address': '123-333-444',
    'email_address': 'suzie@gmail.com',
    'status': True,
    'credit_limit': '$40'}

def test_add_customer():
    add_customer(**customer_dict)
    test_customer = Customer.get(Customer,customer_id==customer_dict['custimer_id'])
    test_customer = Customer.get(Customer.customer_id==customer_id)
    assert test_customer.email_address == email_address

def test_credit_limit_float():
    bad_customer = dict(customer_dict)
    bad_customer['credit_limit'] = '$40'
    with pytest.raise(ValueError):
        add_customer(**bad_customer)
        print(customer_dict)
