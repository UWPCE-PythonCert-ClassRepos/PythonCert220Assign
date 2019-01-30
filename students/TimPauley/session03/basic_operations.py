#Tim Pauley
#Assignment 03
#Jan 22 2018

"""
Assignment Description

1. Create a customer model and database that can be used at HP Norton.
At a minimum, the following information needs to be stored:

TABLE SCHEMA

Customer ID.
Name.
Lastname.
Home address.
Phone number.
Email address.
Status (active or inactive customer).
Credit limit.

2. Create a file called basic_operations.py. This file will need to have 
the following functions:

a. 	customer_id
	, name
	, lastname
	, home_address
	, phone_number
	, email_address
	, status
	, credit_limit): This function will add a new customer to the sqlite3 database.

b. search_customer(customer_id): This function will return a 
dictionary object with name, lastname, email address and phone number 
of a customer or an empty dictionary object if no customer was found.

c. delete_customer(customer_id): This function will delete a customer 
from the sqlite3 database.

d. update_customer_credit(customer_id, credit_limit): This function will 
arch an existing customer by customer_id and update their credit limit 
or raise a ValueError exception if the customer does not exist.

e. list_active_customers(): This function will return an integer with 
the number of customers whose status is currently active.

Note: You can have other functions and code as required, but the five 
functions outlined above should be present and using the same amount of 
parameters. This is important, as those functions are how your code gets 
integrated into other sections of the project (such as the Web frontend).

3. Create some functional and unit tests for the model. Store them in 
the tests directory.

4. Develop functionality to deliver the requirements listed above.

5. Develop tests, and show some tests passing. Show other tests failing.

6. Ensure you application will create an empty database if one doesn’t 
exist when the app is first run. Call it customers.db

"""
import logging
import pandas
import peewee
from customers_model import Customer

'''
This function will add a new customer to the sqlite3 database.
'''
def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status, credit_limit):
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise
    new_customer = Customer.create(
        customer_id = customer_id,
        first_name = name,
        last_name = last_name,
        home_address = home_address,
        phone_number = phone_number,
        email_address = email_address,
        status = status,
        credit_limit = credit_limit)
    new_customer.save()

'''
This function will return a 
dictionary object with name, lastname, email address and phone number 
of a customer or an empty dictionary object if no customer was found.
'''
def search_customer(customer_id):
	for data_dict in data_source:
    MyModel.create(**data_dict)


'''
This function will search an existing customer by customer_id and 
update their credit limit or raise a ValueError exception if the 
customer does not exist.
'''
def update_customer_credit(customer_id, credit_limit)
	for data_dict in data_source:
    MyModel.create(**data_dict)
'''
This function will delete a customer from the sqlite3 database.
'''
def delete_customer(customer_id):
	with 
'''
This function will search an existing customer by customer_id & update 
their credit limit or raise a ValueError exception if the customer 
does not exist.
'''
def update_customer_credit(customer_id, credit_limit): 	



