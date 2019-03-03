#Tim Pauley
#Python 220, Assignment 04
#Jan 29 2019
#Update: Feb 20 2019
#Assignment 04: 

'''
We are not going to develop new functionality in this assignment. 
Rather, we are going to refactor existing code to improve it and make 
it more Pythonic. This is a very common activity in application 
development.

You will already have tests from the lesson 3 assignment that verify 
data is being written to the HP Norton databases. Although we are going 
to change the way data is written to and read from the databases
, the tests should not need to change. 
We are amending the functionality the tests use to make them easier to 
maintain and be more Pythonic.

This development process, where we change internal behavior while 
preserving how that behavior is called, is named refactoring.

So here is our refactoring assignment:

Using comprehensions, iterators / iterables, and generators appropriately
, and the instructor-provided customer data, write data to your customer 
database and read / display it.

Verify existing unit tests still function correctly.
If necessary, update your tests to show the data is being maintained 
correctly in the database.
Add code to log all database data changes (adds, amends, deletes) to a 
file called db.log.
Be sure to consult the lesson 3 assignment for details of the 
functionality.

Submit
You will need to submit basic_operations.py plus any test files you 
develop.
'''

#assignment 03 import model

from customer_model import Customer
import peewee as pw
import logging
import config
import csv
from utils import check_status

#assignment 04 import  model


from peewee import *
from customer_model import Customer
from customer_model import database


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
def add_from_csv(csv_file):
    """
    Given a csv file, add all customers at once
    Must have heading that matches columns (not case-sensitive)
    customer_id
    name
    last_name
    home_address:
    phone_number:
    email_address:
    status: must be True or False
    credit_limit: Must be a number, no $
    """
    headings = None
    with open('customer.csv', 'r', newline='', encoding='ISO-8859-1') as myfile:
        for row in csv.reader(myfile):
            if not headings:
                headings = [heading.lower() for heading in row]
                continue
            add_customer(**{key: value for key, value in zip(headings, row)})
'''

def add_customer(**kwargs):
    try:
        kwargs['credit_limit'] = float(kwargs['credit_limit'])
    except ValueError as err:
        raise
    if not database.table_exists('Customer'):
        database.create_tables([Customer])
    new_customer = Customer.insert(kwargs)
    new_customer.execute()


def search_customer(customer_id=None):
    search_customer = Customer.select().where(
        Customer.customer_id == customer_id).dicts()
    field_names = Customer._meta.sorted_field_names
    if search_customer:
        return {
            field_name: record[field_name]
            for record in search_customer for field_name in field_names
        }
    else:
        return {}


def delete_customer(customer_id=None):
    delete_customer = Customer.get_or_none(Customer.customer_id == customer_id)
    if delete_customer:
        delete_customer.delete_instance()


def update_customer(**kwargs):
    update_customer = Customer.get_or_none(
        Customer.customer_id == kwargs['customer_id'])
    if update_customer:
        insert_dict = {
            kwarg: kwargs[kwarg]
            for kwarg in kwargs if kwarg != 'customer_id'
        }
        update_query = Customer.update(insert_dict).where(
            Customer.customer_id == kwargs['customer_id'])
        update_query.execute()
    else:
        raise ValueError


def list_active_customers():
    return Customer.select().where(Customer.status == True).count()
