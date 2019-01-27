"""This is the test script for basic operations"""
from unittest import TestCase
from unittest.mock import MagicMock, patch
import pytest
from basic_operations import add_customer, search_customer, \
    update_customer_credit, delete_customer, list_active_customers
from customer_model import Customer

ok_customer = {'customer_id': 'W343d',
               'name': 'Suzie',
               'last_name': 'Edgar',
               'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
               'phone_number': '221-111-2222',
               'email_address': 'suzie@hotmail.com',
               'status': True,
               'credit_limit': 40}

ok_customer2 = {'customer_id': 'DAC899',
                'name': 'Dan',
                'last_name': 'Cornutt',
                'home_address': '1st Browncroft Blvd, Rochester, NY 97235',
                'phone_number': '206-111-2222',
                'email_address': 'suzie@bing.com',
                'status': True,
                'credit_limit': 40000}

bad_customer = {'customer_id': 'BD900',
                'name': 'Bad',
                'last_name': 'Ed',
                'home_address': '123 Browncroft Blvd, Seattle, WA, 97235',
                'phone_number': '221-111-2222',
                'email_address': 'BadEd@hotmail.com',
                'status': False,
                'credit_limit': 10}


def test_add_ok_customer():
    """Adds two customers and tests one is saved in customer.db"""
    add_customer(**ok_customer)
    add_customer(**ok_customer2)
    test_customer = Customer.get(Customer.customer_id ==
                                 ok_customer['customer_id'])
    assert test_customer.email_address == ok_customer['email_address']


def test_search_customer():
    """Searches customer db for customer_id 'W343d'"""
    searched = search_customer('W343d')
    assert searched['__data__']['first_name'] == 'Suzie'


def test_update_credit():
    """Updates credit limit on customer_id 'W343d' to 900 and confirms"""
    update_customer_credit('W343d', 900)
    updated = search_customer('W343d')
    print(updated)
    assert updated['__data__']['credit_limit'] == 900


def test_del_customer():
    """Stores number of active customers, deletes customer, checks current
    active customers is one less"""
    table_len = list_active_customers()
    delete_customer('W343d')
    assert table_len == 1 + list_active_customers()


def test_list_active_customers():
    """Tests for active customers, should be 1"""
    assert list_active_customers() == 1
