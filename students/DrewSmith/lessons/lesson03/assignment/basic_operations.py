'''
Basic operations for interacting with customers database
'''


import logging
from peewee import DoesNotExist
from assignment.customers_model import Customer

def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    ''' Add a customer '''
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise

    if not isinstance(status, bool):
        logging.error(f"Invalid value: status is not a bool: {status}")
        raise ValueError(f"Invalid value: status is not a bool: {status}")

    new_customer = Customer.create(
        customer_id=customer_id,
        first_name=name,
        last_name=lastname,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit
    )
    new_customer.save()

def search_customer(customer_id):
    '''
    Search for a customer

    :param customer_id: customer id to search for
    '''

    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        return {
            "name": customer.first_name,
            "lastname": customer.last_name,
            "email_address": customer.email_address,
            "phone_number": customer.phone_number
        }
    except DoesNotExist:
        return {}

def delete_customer(customer_id):
    '''
    Deletes a customer if it exists, otherwise throws DoesNotExist error

    :param customer_id: customer_id to search and delete
    '''
    customer = Customer.get(Customer.customer_id == customer_id)
    customer.delete_instance()

def update_customer_credit(customer_id, credit_limit):
    '''
    Updates the customer credit amount

    :param customer_id: customer id to search and update
    :param credit_limit: credit limit value to change to
    '''
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise

    try:
        customer = Customer.get(Customer.customer_id == customer_id)
    except DoesNotExist:
        logging.info(f"Customer does not exist: {customer_id}")
        raise ValueError(f"Customer_id does not exist: {customer_id}")

    customer.credit_limit = credit_limit
    customer.save()

def list_active_customers():
    ''' Returns the number of active customers '''
    return Customer.select().where(Customer.status).count()
