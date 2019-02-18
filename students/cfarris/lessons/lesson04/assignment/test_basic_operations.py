#!/usr/bin/env Python3

'''
This pytest suite tests basic functionality of basic_operations.py
'''
from peewee import Model, CharField, BooleanField, FloatField, SqliteDatabase
import pytest
from basic_operations import add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers, batch_enter_customers_to_db
from customer_model import Customer, BaseModel, database
from create_database import create_tables
import os
import config

# note, if you get an integrity error be sure clear your database.

OK_CUSTOMER = {'customer_id': 'ABCD@#',
               'first_name': 'Edgar',
               'last_name': 'Poe',
               'home_address': '1266 South Corrine Court, Walnut Creek CA 98125',
               'phone_number': '123-456-7891',
               'email_address': 'ep@gmail.com',
               'status': True,
               'credit_limit': 40.00}

OK_CUSTOMER_2 = {'customer_id': ' 0U812',
                 'first_name': 'TAMMY',
                 'last_name': 'Faye',
                 'home_address': '1266 South Corrine Court, Walnut Creek CA 98125',
                 'phone_number': '123-456-7891',
                 'email_address': 'Tammy_Faye@gmail.com',
                 'status': True,
                 'credit_limit': 4000.00}

BAD_CUSTOMER = {'customer_id': '8675309',
                'first_name': 'Jenny',
                'last_name': 'Igotyonumber',
                'home_address': 'Beverly Hills Plaza, Compton, Ca. 90210',
                'phone_number': '198-765-4321',
                'email_address': 'Jenny_Igotyonumber@gmail.com',
                'status': True,
                'credit_limit': 40.00}

OK_CUSTOMER_3 = {'customer_id': 'A97654',
                 'first_name': 'Jekyll',
                 'last_name': 'Hyde',
                 'home_address': 'Beverly Hills Plaza, Beverly Hills, Ca. 90210',
                 'phone_number': '908-654-3333',
                 'email_address': 'Jeklyll_Hyde@gmail.com',
                 'status': True,
                 'credit_limit': 40.00}


@pytest.fixture
def set_up_connection():
    test_database = create_tables()
    yield set_up_connection
    print("Delete Database")
    test_database.drop_tables(Customer)
    #os.remove('test.db')


def test_add_ok_customer(set_up_connection):
    '''
    tests a customer can be added to the database.
    '''
    delete_customer(OK_CUSTOMER['customer_id'])  # delete an existing customer
    add_customer(**OK_CUSTOMER)  # now, add them back to the database.
    test_customer = Customer.get(Customer.customer_id == OK_CUSTOMER['customer_id'])
    assert test_customer.email_address == OK_CUSTOMER['email_address']


def test_credit_limit_float(set_up_connection):
    '''
    tests to see that adding a string to 'credit_limit' throws a ValueError
    '''
    BAD_CUSTOMER['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        add_customer(**BAD_CUSTOMER)


def test_search_customer(set_up_connection):
    '''
    Tests customer is retrievable. Will use test supplied OK_CUSTOMER
    '''
    add_customer(**OK_CUSTOMER)
    returned_customer = search_customer(OK_CUSTOMER['customer_id'])
    assert returned_customer['first_name'] == 'Edgar'


def test_search_customer_not_found(set_up_connection):
    '''
    Tests search_customer returns an empty dictionary when customer not found
    '''
    returned_customer = search_customer('bad id')
    assert returned_customer == {}


def test_delete_customer(set_up_connection):
    '''
    Tests delete_customer to verify specified customer was deleted from db
    First add the customer to be deleted, then delete them with joy!
    Using OK_CUSTOMER_2 for this test module only.
    '''
    add_customer(**OK_CUSTOMER_2)
    test_customer_2 = Customer.get(Customer.customer_id == OK_CUSTOMER_2['customer_id'])
    assert test_customer_2.email_address == OK_CUSTOMER_2['email_address']
    delete_results = delete_customer(test_customer_2.customer_id)
    assert delete_results == 'person successfully deleted'


def test_update_customer_credit(set_up_connection):
    '''
    Tests update_customer_credit.
    '''
    add_customer(**OK_CUSTOMER)
    update_customer_credit(OK_CUSTOMER['customer_id'], 75.00)
    test_customer = Customer.get(Customer.customer_id == OK_CUSTOMER['customer_id'])
    assert test_customer.credit_limit == 75.00


def test_list_active_customers(set_up_connection):
    '''
    Test that list_active customers returns the amount of those active.
    First get an accurate count of active customers,
    add a new customerthat is active
    Test to see that the active customers number has increased.
    '''
    num_active = list_active_customers()
    add_customer(**OK_CUSTOMER_3)  # bad customer should work
    num_active_2 = list_active_customers()
    delete_customer(OK_CUSTOMER_3['customer_id'])
    assert (num_active + 1) == num_active_2


def test_batch_enter_customers_to_db(set_up_connection):
    '''
    Tests that one can correctly batch enter customers from a csv file
    '''
    line_count = batch_enter_customers_to_db('lesson04_assignment_data_customer.csv')
    assert line_count == 10001
