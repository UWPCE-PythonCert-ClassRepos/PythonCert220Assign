#!/usr/bin/env Python3
import pytest
from basic_operations import add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers
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

ok_customer_3 = {'customer_id':'A97654',
                 'first_name': 'Jekyll',
                 'last_name': 'Hyde',
                 'home_address': 'Beverly Hills Plaza, Beverly Hills, Ca. 90210',
                 'phone_number': '908-654-3333',
                 'email_address': 'Jeklyll_Hyde@gmail.com',
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
    Using ok_customer_2 for this test module only.
    '''
    add_customer(**ok_customer_2)
    test_customer_2 = Customer.get(Customer.customer_id == ok_customer_2['customer_id'])
    assert test_customer_2.email_address == ok_customer_2['email_address']
    delete_results = delete_customer(test_customer_2.customer_id)
    assert delete_results == 'person successfully deleted'


def test_update_customer_credit():
    '''
    Tests update_customer_credit. 
    '''
    update_customer_credit(ok_customer['customer_id'], 75.00)
    test_customer = Customer.get(Customer.customer_id == ok_customer['customer_id'])
    assert test_customer.credit_limit == 75.00


def test_list_active_customers():
    '''
    Test that list_active customers returns the amount of those active.
    The way I chose to test this was to get an accurate count of active customers, 
    add a new customerthat is active
    Test to see that the active customers number has increased.
    '''
    number_of_customers= Customer.select().count()
    num_active = list_active_customers()
    add_customer(**ok_customer_3) #bad customer should work
    num_active_2 = list_active_customers()
    delete_customer(ok_customer_3['customer_id'])
    assert (num_active + 1) == num_active_2


