#!/usr/bin/env Python3

####Assignment 3###
##basic operations for peewee

#Current progress: on delete customer. Need to finish creating function
#then create tests for it.

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
       retr_customer = Customer.get(Customer.customer_id == customer_id)


if __name__ == '__main__':

    #added customer below already
    #add_customer('2212','Jerry','Blank','19202 130th Ave, Sun City, Az. 98125', '123-456-6543', 'jb@aol.com', False, 500.00)    
    print("already added customers. name == main is just a placeholder")
    search_customer('2212')
    search_customer('1')
    #delete_customer('2212') #works correctly
