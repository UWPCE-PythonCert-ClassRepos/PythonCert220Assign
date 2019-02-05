#Tim Pauley
#Python 220, Assignment 04
#Jan 29 2019

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

#assignment 03

from customer_model import Customer
import peewee as pw
import logging
import config
import csv
from utils import check_status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def add_customer(customer_id, **kw):
    """
    Add a customer to the database
    :param customer_id:
    :param name:
    :param lastname:
    :param home_address:
    :param phone_number:
    :param email_address:
    :param status: must be True or False, active or inactive
    :param credit_limit: Must be a number, no $
    :return: None
    """
    try:
        cust = Customer.create(customer_id=customer_id,
                               first_name=kw['name'],
                               last_name=kw['last_name'],
                               home_address=kw['home_address'],
                               phone_number=kw['phone_number'],
                               email_address=kw['email_address'],
                               status=check_status(kw['status']),
                               credit_limit=kw['credit_limit'])
        cust.save()
    except KeyError as err:
        logging.error(err)
        raise ValueError(config.etext['no_save'].format(customer_id))
    except Exception as err:
        logging.error(err)
        raise
    logger.info("Customer with id %s successfully added!", customer_id)


def search_customer(customer_id):
    """
    Return a dictionary object with name, lastname, email address and phone
    number of a customer or an empty dictionary object if no customer was found
    """

    output_dict = {}

    try:
        cust = Customer.get(Customer.customer_id == customer_id)
    except pw.DoesNotExist as err:
        logging.error(err)
    else:
        my_attrs = ['first_name', 'last_name', 'email_address', 'phone_number']
        output_dict = {cust_attr: getattr(cust, cust_attr) for cust_attr in my_attrs}
        logging.info("Cust object exists")
    return output_dict


def delete_customer(customer_id):

    try:
        cust = Customer.get(Customer.customer_id == customer_id)
    except Customer.DoesNotExist as err:
        logging.error(err)
        raise ValueError(config.etext['not_found'].format(customer_id))
    cust.delete_instance()


def update_customer_credit(customer_id, credit_limit):
    # this should be more general, and should have error handling
    cust = Customer.get(Customer.customer_id == customer_id)
    cust.credit_limit = credit_limit
    cust.save()


def list_active_customers():
    num_custs = Customer.select().where(Customer.status == 1)
    return num_custs.count()

