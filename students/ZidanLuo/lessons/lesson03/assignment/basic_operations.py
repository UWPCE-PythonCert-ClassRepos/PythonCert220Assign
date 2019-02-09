import logging
from customer_model import Customer
import peewee


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


def search_customer(customer_id):
    '''
    Thi function will return the information of the customer
    with the specified customer id
    :param: customer_id
    :return a dict object with the information of the particular customer
    '''
    default_dict = {}
    try:
        requested_customer = Customer.get_by_id(customer_id)
    except peewee.DoesNotExist as err:
        logging.error(err)
        return default_dict
    customer_dict = {
        "customer_id":requested_customer.customer_id,
        "first_name":requested_customer.first_name,
        "last_name":requested_customer.last_name,
        "home_address":requested_customer.home_address,
        "phone_number":requested_customer.phone_number,
        "email_address":requested_customer.email_address,
        "status":requested_customer.status,
        "credit_limit":requested_customer.credit_limit
    }
    return customer_dict


def delete_customer(customer_id):
    '''
    This function will delete a customer from the database
    :param:customer_id
    :return:none
    '''
    customer = Customer.get(Customer.customer_id == customer_id)
    customer.delete_instance()

def update_customer_credit(customer_id, credit_limit):
    '''
    This function will search an existing customer by customer_id and update
    their credit limit or raise a ValueError exception if the customer does 
    not exist
    :param:customer_id as as a string and credit_limit as a float
    :return:None
    '''
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
    except ValueError as err:
        logging.error(err)
        raise
    customer.credit_limit = credit_limit
    customer.save()