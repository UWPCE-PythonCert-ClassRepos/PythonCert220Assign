#!/usr/bin/env Python3

####Assignment 3###
##basic operations for peewee

#Current progress: 
#

import logging
from customer_model import Customer


def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
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
    except Exception as e:
        logging.error(e)
        print('Error occurred retrieving cust: ', e)
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
    except Exception as e:
        logging.error('error finding and deleting customer:', e)
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
        #below isn't correct! Just a placeholder...
        retr_customer = Customer.get(Customer.customer_id == customer_id)
        retr_customer.credit_limit = credit_limit
        retr_customer.save()
        if credit_limit < 0:
            logging.warning('credit_limit parameter is less than 0: ', credit_limit)
    except ValueError as err:
        logging.error('error replacing customers credit limit: ,', err)
        error_statement = 'An error occured while replacing customers credit.\
                         Credit unchanged.'
        print(error_statement)
        return error_statement
    check_customer = Customer.get(Customer.customer_id == customer_id)    
    print(check_customer.customer_id, ' has had their credit limit changed to:', check_customer.credit_limit)
    return 'operation successfully completed'


def list_active_customers():
    '''
    lists active customers
    '''
    count = 0
    for customer in Customer.select().where(Customer.status == True):
        count = count + 1
    print('There are ', count, ' active customers')
    return count



if __name__ == '__main__':

    #added customer below already
    #add_customer('2212','Jerry','Blank','19202 130th Ave, Sun City, Az. 98125', '123-456-6543', 'jb@aol.com', False, 500.00)    
    print("already added customers. name == main is just a placeholder")
    print(search_customer('2212'))  #function returns a dictionary
    #search_customer('1') #confirming it will throw an error because it isn't in database.
    #delete_customer('2212') #works correctly
    update_customer_credit('2212', 20.00)
    list_active_customers()
