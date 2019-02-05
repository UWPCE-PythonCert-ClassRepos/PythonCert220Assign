'''
Basic operations for interacting with customers database
'''


import logging
import peewee as pw
from peewee import DoesNotExist
import assignment.create_customers as cc
from assignment.customers_model import Customer
# import customers_model.Customer as Customer
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert_csv(file_path):
    '''
    Generator for CSV file formatted for Customer model data

    :param file_path: file path for the CSV file
    :yield: CSV line dictionary formatted for Customer model
    '''
    fields = ( 'customer_id', 'first_name', 'last_name', 'home_address',
                'phone_number', 'email_address', 'status', 'credit_limit')
    with open(file_path, 'r') as file:
        csv_file = csv.DictReader(file, fieldnames=fields)
        for index, row in enumerate(csv_file):
            if index == 0:
                continue

            row['phone_number'] = "".join(char for char in row['phone_number'] if char not in  '.()- ')
            row['status'] = bool(row['status'].lower() == 'active')
            row['credit_limit'] = float(row['credit_limit'])
            yield row


def bulk_add_customers(customers):
    '''
    Adds a bulk amount of customers

    :param customers: sequence of dictionaries, expects keys:
        customer_id, first_name, last_name, home_address,phone_number, email_address,
        status, credit_limit
    '''
    batch_size = 120
    customer_list = list()
    db = cc.get_database()
    for index, customer in enumerate(customers, start=1):
        try:
            customer['credit_limit'] = float(customer['credit_limit'])
        except ValueError as err:
            logging.error(err)
            raise ValueError(f"Invalid value: record {index}: invalid credit_limit: '{customer['credit_limit']}'")

        if not isinstance(customer['status'], bool):
            text = f"Invalid value: record {index}: status is not a bool: '{customer['status']}'"
            logging.error(text)
            raise ValueError(text)

        customer_list.append(customer)
        if index % batch_size == 0:
            _insert_customer_list(customer_list, db)
            logger.info(f"Inserted {batch_size} customers")
            customer_list = list()
        
    if len(customer_list) > 0:
        _insert_customer_list(customer_list, db)
        logger.info(f"Inserted {len(customer_list)} customer(s)")

def _insert_customer_list(customer_list, database):
    '''
    Internal function to add customer list with error checking

    :param customer_list: sequence of customer dictionaries to insert
    :param database: database object for the atomic transaction
    '''
    with database.atomic():
        try:
            Customer.insert_many(customer_list).execute()
        except pw.IntegrityError as error:
            logging.error(f"Customer already exists: {str(error)}")
            raise

def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    ''' Add a single customer customer '''
    customer = {
        'customer_id': customer_id,
        'first_name': name,
        'last_name': lastname,
        'home_address': home_address,
        'phone_number': phone_number,
        'email_address': email_address,
        'status': status,
        'credit_limit': credit_limit
    }
    bulk_add_customers((customer,))
    logger.info(f"Added customer: '{customer_id}'")

def search_customer(customer_id=None):
    '''
    Search for a customer

    :param customer_id: customer id to search for
    '''

    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        keys = ("name", "lastname", "email_address", "phone_number")
        values = ("first_name", "last_name", "email_address", "phone_number")
        return { key: getattr(customer, value) for key, value in zip(keys, values) }
    except DoesNotExist:
        logging.info(f"Customer not found: {customer_id}")
        return {}

def delete_customer(customer_id):
    '''
    Deletes a customer if it exists, otherwise throws DoesNotExist error

    :param customer_id: customer_id to search and delete
    '''
    customer = Customer.get(Customer.customer_id == customer_id)
    customer.delete_instance()
    logger.info(f"Deleted customer: {customer_id}")

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
    logger.info(f"Updated customer credit_limit: {customer_id}, {credit_limit}")

def list_active_customers():
    ''' Returns the number of active customers '''
    return Customer.select().where(Customer.status).count()
