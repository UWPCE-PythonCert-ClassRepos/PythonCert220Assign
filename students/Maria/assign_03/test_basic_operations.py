from basic_operations import add_customer
from customers_model import Customer
import pytest

ok_customer = {'customer_id': 'W3434fd',
               'name': 'Suzie',
               'last_name': 'Edgar',
               'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
               'phone_number': '234-123-4567',
               'email_address': 'suzie@hotmail.com',
               'status': True,
               'credit_limit': '40'}

def test_add_ok_customer():
    add_customer(**ok_customer)
    test_customer = Customer.get(Customer.customer_id==ok_customer['customer_id'])
    assert test_customer.email_address == ok_customer['email_address']

def test_credit_limit_float():
    bad_customer = dict(ok_customer)
    bad_customer['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        add_customer(**bad_customer)
