'''
Tests the basic_operations module
'''

import logging
from pytest import fixture
from pytest import raises
import datetime
import assignment.create_customers as cc
# Use Test environment database
cc.get_database(env="test")

import assignment.basic_operations as bo
from assignment.customers_model import Customer

def logging_setup():
    log = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('db.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logging_setup()

customer_id_list = ("search_customer", "delete_customer_good", "update_credit", "active_customers")

customer_data = {
    'name': 'Suzie',
    'lastname': "Edgar",
    'home_address': "123 Browncroft Blv, Rochester, NY 97235",
    'phone_number': '123-456-7890',
    'email_address': 'suzie@hotmail.com',
    'status': True,
    'credit_limit': 40
}

def data_setup():
    for customer_id in customer_id_list:
        customer = dict(customer_data)
        customer["customer_id"] = customer_id
        customer["first_name"] = customer_data["name"]
        customer["last_name"] = customer_data["lastname"]
        del customer["name"]
        del customer["lastname"]
        yield customer

@fixture(autouse=True)
def setup_teardown():
    ''' Fixture to execute before and after tests '''
    db = cc.get_database()
    db.drop_tables([Customer])
    db.create_tables([Customer])
    
    data = data_setup()
    bo.bulk_add_customers(data)

    yield


def test_add_csv_bulk():
    '''
    Adds the contents of the test data csv to the database
    This tests the bulk_add_customers and convert_csv methods
    '''
    bo.bulk_add_customers(bo.convert_csv('lesson04_assignment_data_customer.csv'))
    assert Customer.select().count() == 10000 + len(customer_id_list)

def test_add_customer_ok():
    ''' Add a new valid customer '''
    customer_id = "add_ok"
    ok_customer = dict(customer_data)
    ok_customer['customer_id'] = customer_id
    bo.add_customer(**ok_customer)

    result = Customer.get(Customer.customer_id == customer_id)
    assert result.first_name == ok_customer["name"]
    assert result.last_name == ok_customer["lastname"]
    assert result.home_address == ok_customer["home_address"]
    assert result.phone_number == ok_customer["phone_number"]
    assert result.email_address == ok_customer["email_address"]
    assert result.status == ok_customer["status"]
    assert result.credit_limit == float(ok_customer["credit_limit"])

def test_add_customer_credit_limit_float():
    ''' Add customer with an invalid credit limit '''
    bad_customer = dict(customer_data)
    bad_customer['customer_id'] = "cred_float"
    bad_customer['credit_limit'] = '$40'

    with raises(ValueError):
        bo.add_customer(**bad_customer)

def test_add_customer_bad_status():
    ''' Add a customer with an invalid status '''
    bad_customer = dict(customer_data)
    bad_customer['customer_id'] = "bad_status"
    bad_customer['status'] = "not a bool"

    with raises(ValueError):
        bo.add_customer(**bad_customer)

def test_search_customer():
    ''' Search for an expected customer '''
    search_good = dict(customer_data)
    customer_id = "search"
    search_good['customer_id'] = customer_id

    bo.add_customer(**search_good)
    result = bo.search_customer(customer_id)
    
    assert isinstance(result, dict)
    assert result["name"] == search_good["name"]
    assert result["lastname"] == search_good["lastname"]
    assert result["email_address"] == search_good["email_address"]
    assert result["phone_number"] == search_good["phone_number"]

def test_search_customer_missing():
    ''' search for a missing customer '''
    result = bo.search_customer("search_bad")    
    assert result == {}

def test_delete_customer_ok():
    ''' delete and verify customer '''   
    bo.delete_customer("delete_customer_good")
    result = bo.search_customer("delete_customer_good")    
    assert result == {}

def test_update_customer_credit_good():
    ''' Verify valid credit limit values are udpated '''
    bo.update_customer_credit("update_credit", 2000.0)
    result = Customer.get(Customer.customer_id == "update_credit")
    assert result.credit_limit == float(2000.0)

    bo.update_customer_credit("update_credit", "25")
    result = Customer.get(Customer.customer_id == "update_credit")
    assert result.credit_limit == float("25")

def test_update_customer_credit_bad():
    ''' Verify a ValueError is raised when an 
    invalid credit_limit value is used '''
    with raises(ValueError):
        bo.update_customer_credit("update_credit", "$789")

def test_list_active_customers():
    ''' test list_active_customers count '''
    result = bo.list_active_customers()
    assert result == len(customer_id_list)
    customer = Customer.get(Customer.customer_id == "active_customers")
    customer.status = False
    customer.save()

    result = bo.list_active_customers()
    assert result == len(customer_id_list) - 1

