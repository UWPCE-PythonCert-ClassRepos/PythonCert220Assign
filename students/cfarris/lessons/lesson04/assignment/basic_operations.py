#!/usr/bin/env Python3

'''
This scripts provides the functions to interact with
the sqlite3 database via peewee
'''

import peewee as peewee
import logging
from customer_model import Customer
import csv
import sys


log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)  #create a formatter
logger = logging.getLogger()  #calls the logger object
file_handler = logging.FileHandler('basic_operations.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    '''
     Adds customer to customer database
     PARAMS: Multiple fields. customer_id is primary key
     Return: not yet known
    '''
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise  # Credit limit has to be a float to work in our database
    
    try:
        new_customer = Customer.create(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            status=status,
            credit_limit=credit_limit)
        new_customer.save()
    except peewee.IntegrityError as err:
        logging.error(f"Error adding customer: {err},"
                      f" {customer_id}, {first_name},"
                      f"{last_name}")
        print(f"Error adding customer: {customer_id}")
        #raise


def search_customer(customer_id):
    '''
    searches customer.db for customer using primary_key (customer_id)
    PARAM: customer_id
    RETURNS: dictionary object containing name,
             lastname, email address and phone number
             or an empty dictionary object if the customer isnt found.
    '''
    try:
        retr_customer = Customer.get(Customer.customer_id == customer_id)
        cust_dict = {'first_name': retr_customer.first_name,
                     'last_name': retr_customer.last_name,
                     'email_address': retr_customer.email_address,
                     'phone_number': retr_customer.phone_number}
    except Exception as err:
        logging.error(err)
        print('Error occurred retrieving cust: ', err)
        cust_dict = {}
        return cust_dict
    return cust_dict


def delete_customer(customer_id):
    '''
    deletes a customer from customers.db if customer is found.
    '''
    try:
        person = Customer.get(Customer.customer_id == customer_id)
        person.delete_instance()
    except Exception as err:
        logging.error('error finding and deleting customer:', err)
        print('Customer wasn\'t found in database. Database unchanged')
    print('person successfully deleted')
    return 'person successfully deleted'


def update_customer_credit(customer_id, credit_limit):
    '''
    This function searches existing customer by ID and updates
    credit_limit to new value
    A ValueError will be raised if customer does not exist in database.
    '''
    try:
        retr_customer = Customer.get(Customer.customer_id == customer_id)
        retr_customer.credit_limit = credit_limit
        retr_customer.save()
        if credit_limit < 0:
            logging.warning('credit_limit parameter is ',
                            'less than 0: ', credit_limit)
    except ValueError as err:
        logging.error('error replacing customers credit limit: ,', err)
        error_statement = 'An error occured while replacing customers credit.\
                         Credit unchanged.'
        print(error_statement)
        return error_statement
    check_customer = Customer.get(Customer.customer_id == customer_id)
    print(check_customer.customer_id,
          ' has had their credit limit changed to:',
          check_customer.credit_limit)
    return 'operation successfully completed'


def list_active_customers():
    '''
    Returns the number of active customers
    '''
    count = 0
    for customer in Customer.select().where(Customer.status == True):
        count = count + 1
    #count + 1 for customer in Customer.select().where(Customer.status == True)
    print('There are ', count, ' active customers')
    return count


def batch_enter_customers_to_db(file):
    '''
    Accepts a file (TBD) and enters valid data into db
    '''
    line_count = 0
    with open(file, 'r', encoding='unicode_escape') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        #line_count = 0
        for row in csv_reader:
            if line_count == 0:  # capture the headers
                line_count = line_count + 1
                print("headers:", row)
            else:
                line_count = line_count + 1
                str_row = [value.strip() for value in row]
                status = check_customer_status(str_row[0], str_row[6].lower())
                credit_limit = convert_customer_credit_to_float(str_row[0], str_row[7].lower())
                add_customer(str_row[0],
                             str_row[1],
                             str_row[2],
                             str_row[3],
                             str_row[4],
                             str_row[5],
                             status,
                             credit_limit)
        return line_count 


def convert_customer_credit_to_float(customer_id,credit_limit):
    '''
    Accepts customer id (for logging) and credit limit and checks
    credit_limit can be a float. Returns a logging Warning if credit_limit
    cannot be converted to a float.
    Params: Customer_id and credit_limit
    Return: Credit_limit as a float ready to be added into database
    '''
    try:
        credit_limit = float(credit_limit)
    except Exception as e:
        logging.error('Error converting credit limit to float:', e, customer_id, credit_limit)
        print('Error converting credit limit to float:', customer_id, credit_limit)
        raise
    else:
        return credit_limit




def check_customer_status(customer_id,customer_status):
    '''
    Checks a customers reported status and attemts to
    give status a boolean value. If it cannot, it will throw an error
    
    Param: customer_status
    Return: boolean value of customer status
    '''
    if customer_status == 'active':
        return True
    elif customer_status == 'inactive':
        return False
    else:
        logging.warning('bad formatting for Customer status: ', customer_id, customer_status)
        print('bad formatting for Customer status: ', customer_id, customer_status)
       



if __name__ == '__main__':
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
    add_customer(**OK_CUSTOMER_2)                        
    print('basic_operations.py is ready to be used with customers.db')
    list_active_customers()
    delete_customer(' 0U812')
    #batch_enter_customers_to_db('lesson04_assignment_data_customer.csv') #works
