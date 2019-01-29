#!/usr/bin/env Python3
import pytest
from basic_operations import add_customer, search_customer, delete_customer
from customer_model import Customer

##note, if you get an integrity error be sure clear your database. 

ok_customer = {'customer_id': 'ABCD@#',
               'first_name': 'Edgar',
               'last_name': 'Poe',
               'home_address': '1266 South Corrine Court, Walnut Creek CA 98125',
               'phone_number': '123-456-7891',
               'email_address': 'ep@gmail.com',
               'status': True,
               'credit_limit': 40.00}

ok_customer_2 = {'customer_id':' 0U812',
                'first_name': 'TAMMY',
                'last_name': 'Faye',
                'home_address': '1266 South Corrine Court, Walnut Creek CA 98125',
                'phone_number': '123-456-7891',
                'email_address': 'Tammy_Faye@gmail.com',
                'status': True,
                'credit_limit': 4000.00}

bad_customer = {'customer_id':'8675309',
                'first_name': 'Jenny',
                'last_name': 'Igotyonumber',
                'home_address': 'Beverly Hills Plaza, Compton, Ca. 90210',
                'phone_number': '198-765-4321',
                'email_address': 'Jenny_Igotyonumber@gmail.com',
                'status': True,
                'credit_limit': 40.00}


def test_add_ok_customer():
    #add_customer(**ok_customer) #works. but you cannot add more than once!
    test_customer = Customer.get(Customer.customer_id ==ok_customer['customer_id'])
    assert test_customer.email_address == ok_customer['email_address']


def test_credit_limit_float():
    '''
    tests to see that adding a string to 'credit_limit' throws a ValueError
    '''
    bad_customer['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        add_customer(**bad_customer)


def test_search_customer():
    '''
    Tests customer is retrievable. Will use test supplied ok_customer
    '''
    returned_customer = search_customer(ok_customer['customer_id'])
    assert returned_customer['first_name'] == 'Edgar'


def test_search_customer_not_found():
    '''
    Tests search_customer returns an empty dictionary when customer not found
    '''
    returned_customer = search_customer('bad id')
    assert returned_customer == {}

def test_delete_customer():
    '''
    Tests delete_customer to verify specified customer was deleted from db
    First add the customer to be deleted, then delete them with joy!
    '''
    add_customer(**ok_customer_2)
    test_customer_2 = Customer.get(Customer.customer_id == ok_customer_2['customer_id'])
    assert test_customer_2.email_address == ok_customer_2['email_address']
    delete_results = delete_customer(test_customer_2.customer_id)
    assert delete_results == 'person successfully deleted'
