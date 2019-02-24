#Tim Pauley
#Python 220, Assignment 04
#Jan 29 2019
#Update: Feb 20 2019

#Assignment 04: 

from unittest import TestCase
import os
import csv
from builtins import RuntimeError

import config
import basic_operations as bs
from customer_model import Customer, create_cust_table, delete_cust_table, database

#Assignment Notes:
# other tests I would add:
# make sure inactive works, so if I add inactive customers, I can get them and only them back.
# probably should add inactive customers when checking active customers, for that matter. As is,
# could just be giving back the whole list, no matter what and we would not know.
# error checking: is status really a boolean is probably important. other stuff may not be so
# important until we know what they are going to do with the data

'''
This is where I import the test the functions   
'''
from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer
from basic_operations import list_active_customers

'''
This is where I import the modal and customer
'''
from customer_model import Customer
import pytest


'''
Rename fuctional test
'''
ok_customer = {
    'customer_id': 'W3434fd',
    'first_name': 'Suzie',
    'last_name': 'Edgar',
    'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
    'phone_number': '234-123-4567',
    'email_address': 'suzie@hotmail.com',
    'status': True,
    'credit_limit': '40'
}

'''
Rename fuctional test
'''
def add_second_customer():
    second_customer = dict(ok_customer)
    second_customer["customer_id"] = "W3434ff"
    second_customer["first_name"] = "Bob"
    second_customer["email_address"] = 'bob@hotmail.com'
    add_customer(**second_customer)
    return second_customer


'''
Rename fuctional test
'''
def add_third_customer():
    third_customer = dict(ok_customer)
    third_customer["customer_id"] = "M3233bb"
    third_customer["first_name"] = "Jackson"
    third_customer["status"] = False
    add_customer(**third_customer)
    return third_customer

'''
Rename fuctional test
'''
def add_fourth_customer():
    fourth_customer = dict(ok_customer)
    fourth_customer["customer_id"] = "M3233cc"
    fourth_customer["first_name"] = "Michael"
    fourth_customer["status"] = False
    add_customer(**fourth_customer)
    return fourth_customer


'''
Rename fuctional test
'''
def clean_up(customer_id):
    test_customer = Customer.get(Customer.customer_id == customer_id)
    test_customer.delete_instance()


'''
Rename fuctional test
'''
def test_add_ok_customer():
    add_customer(**ok_customer)
    test_customer = Customer.get(
        Customer.customer_id == ok_customer['customer_id'])
    assert test_customer.email_address == ok_customer['email_address']
    assert test_customer.customer_id == ok_customer['customer_id']
    assert test_customer.first_name == ok_customer['first_name']
    assert test_customer.last_name == ok_customer['last_name']
    assert test_customer.phone_number == ok_customer['phone_number']
    assert test_customer.home_address == ok_customer['home_address']
    assert test_customer.status == ok_customer['status']
    assert test_customer.credit_limit == float(ok_customer["credit_limit"])
    clean_up(ok_customer['customer_id'])


'''
Rename fuctional test
'''
def test_credit_limit_float():
    bad_customer = dict(ok_customer)
    bad_customer['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        add_customer(**bad_customer)

'''
Rename fuctional test
'''
def test_add_multiple_customers():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    test_customer = Customer.get(
        Customer.customer_id == ok_customer['customer_id'])
    test_customer1 = Customer.get(
        Customer.customer_id == second_customer["customer_id"])
    assert test_customer != test_customer1
    assert test_customer.first_name == 'Suzie'
    assert test_customer1.first_name == 'Bob'
    clean_up(ok_customer["customer_id"])
    clean_up(second_customer["customer_id"])


'''
Rename fuctional test
'''
def test_search_customer():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    customer_dict = search_customer("W3434ff")
    second_customer["credit_limit"] = float(second_customer["credit_limit"])
    assert customer_dict == second_customer
    clean_up(ok_customer["customer_id"])
    clean_up(second_customer["customer_id"])


'''
Rename fuctional test
'''
def test_search_customer_null():
    add_customer(**ok_customer)
    customer_dict = search_customer("12345")
    assert customer_dict == {}
    customer_dict = search_customer(7)
    assert customer_dict == {}
    customer_dict = search_customer()
    assert customer_dict == {}
    clean_up(ok_customer["customer_id"])

'''
Rename fuctional test
'''
def test_delete_customer():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    delete_customer(second_customer["customer_id"])
    customer_dict = search_customer(second_customer["customer_id"])
    assert customer_dict == {}
    ok_customer["credit_limit"] = float(ok_customer["credit_limit"])
    customer_dict = search_customer(ok_customer["customer_id"])
    assert customer_dict == ok_customer
    clean_up(ok_customer['customer_id'])

'''
Rename fuctional test
'''
def test_delete_not_a_customer():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    delete_customer("12345")
    delete_customer(7)
    delete_customer()
    clean_up(ok_customer['customer_id'])
    clean_up(second_customer['customer_id'])

'''
Rename fuctional test
'''
def test_update_customer_credit():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    update_customer(
        customer_id=second_customer["customer_id"], credit_limit=100.0)
    customer_dict = search_customer(second_customer["customer_id"])
    assert customer_dict["credit_limit"] == 100.0
    clean_up(ok_customer['customer_id'])
    clean_up(second_customer['customer_id'])

'''
Rename fuctional test
'''
def test_update_customer_credit_no_match():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    with pytest.raises(ValueError):
        update_customer(customer_id="12345", credit_limit=100.0)
    clean_up(ok_customer['customer_id'])
    clean_up(second_customer['customer_id'])

'''
Rename fuctional test
'''
def test_list_active_customers():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    third_customer = add_third_customer()
    fourth_customer = add_fourth_customer()
    active_customers = list_active_customers()
    assert active_customers == 2
    test_customer3 = Customer.get(
        Customer.customer_id == third_customer["customer_id"])
    test_customer3.status = True
    test_customer3.save()
    active_customers = list_active_customers()
    assert active_customers == 3
    clean_up(ok_customer['customer_id'])
    clean_up(second_customer['customer_id'])
    clean_up(third_customer['customer_id'])
    clean_up(fourth_customer['customer_id'])
