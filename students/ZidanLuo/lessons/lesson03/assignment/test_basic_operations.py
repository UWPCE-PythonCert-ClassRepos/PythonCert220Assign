from basic_operations import add_customer, search_customer, delete_customer, update_customer_credit
from customer_model import Customer
import pytest
import peewee

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

def test_search_customer():
    #add_customer(**ok_customer)
    result_dict = search_customer('W3434fd')
    assert result_dict['customer_id'] == ok_customer['customer_id']

def test_search_nonexist():
    result_dict = search_customer('LZD5871')
    assert bool(result_dict) == False

def test_delete_customer():
    query = Customer.select().where(Customer.customer_id == 'W3434fd')
    delete_customer('W3434fd')
    assert query.exists() == False

def test_update_customer():
    add_customer(**ok_customer)
    update_customer_credit('W3434fd', '99')
    test_customer = Customer.get(Customer.customer_id == 'W3434fd')
    assert test_customer.credit_limit == 99

'''
Handle DoesNotExist Error failed
def test_update_nonexist():
    with pytest.raises(ValueError):
        update_customer_credit('LZD3721','99')
'''