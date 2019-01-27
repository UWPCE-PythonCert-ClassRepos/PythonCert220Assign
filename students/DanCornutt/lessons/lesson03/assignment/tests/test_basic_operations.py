"""This is the test script for basic operations"""
from unittest import TestCase
from unittest.mock import MagicMock, patch
import pytest
from basic_operations import add_customer, search_customer, \
    update_customer_credit, delete_customer
from customer_model import Customer

ok_customer = {'customer_id': 'W343d',
               'name': 'Suzie',
               'last_name': 'Edgar',
               'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
               'phone_number': '221-111-2222',
               'email_address': 'suzie@hotmail.com',
               'status': True,
               'credit_limit': 40}

bad_customer = {'customer_id': 'BD900',
                'name': 'Bad',
                'last_name': 'Ed',
                'home_address': '123 Browncroft Blvd, Seattle, WA, 97235',
                'phone_number': '221-111-2222',
                'email_address': 'BadEd@hotmail.com',
                'status': False,
                'credit_limit': 10}


def test_add_ok_customer():
    add_customer(**ok_customer)
    test_customer = Customer.get(Customer.customer_id ==
                                 ok_customer['customer_id'])
    assert test_customer.email_address == ok_customer['email_address']


def test_search_customer():
    searched = search_customer('W343d')
    assert searched['__data__']['first_name'] == 'Suzie'


def test_update_credit():
    update_customer_credit('W343d', 900)
    updated = search_customer('W343d')
    print(updated)
    assert updated['__data__']['credit_limit'] == 900


def test_del_customer():
    delete_customer('W343d')
    assert search_customer('W343d') == []
