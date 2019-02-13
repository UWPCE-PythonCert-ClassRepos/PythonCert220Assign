

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)

    Person:
        1. insert records
        2. display all records
        3. show transactions
        4. show error checking
        5. show logging (to explain what's going on)

"""


# import logging

from customers_model import *
import create_customer as cc
from peewee import SqliteDatabase

DATABASE = SqliteDatabase

logging.info("Defining basic operations for the customer database")


def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    """
    add customer to database
    :type credit_limit: object

    Add a customer to the database
    :param customer_id:
    :param first_name:
    :param last_name:
    :param home_address:
    :param phone_number:
    :param email_address:
    :param status: must be True or False
    :param credit_limit: Must be a number, no $
    :return: None

    """
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise ValueError

    new_customer = Customer.create(
        customer_id=customer_id,
        first_name=first_name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit
    )
    new_customer.save()
    logging.info(f' Customer data successfully added')


def search_customer(customer_id):
    """
    This function will return a dictionary object with first name, last name,
    email address and phone number of a customer
    or an empty dictionary object if no customer was found.
        :param customer_id:
        :return: dictionary object with name, lastname, email address and phone number of a customer
    """
    found_customer_dict = {}
    try:
        found_customer = Customer.get(Customer.customer_id == customer_id)
        if found_customer:
            found_customer_dict = {'first_name': found_customer.first_name,
                                   'last_name': found_customer.last_name,
                                   'email_address': found_customer.email_address,
                                   'phone_number': found_customer.phone_number
                                   }
        logging.info(f'customer exist and {found_customer_dict}')
    except Exception as e:
        logger.info(f'Customer not found and see how the database protects our data and look the error, \n {e}')
        # logger.info(e)

    finally:
        logger.info(f'Finally database closes ')
    return found_customer_dict


def delete_customer(customer_id):
    """
    This function will delete a customer from the sqlite3 database.
        :param customer_id:
    """

    try:
        customer_delete = Customer.get(Customer.customer_id == customer_id)
        logger.info(f' trying to delete record for {Customer.customer_id} & first name {Customer.first_name}')
        customer_delete.delete_instance()

    except Exception as e:
        logger.info('Delete failed because Andrew has Jobs')
        logger.info(f'Delete failed: {Customer.first_name}')
        logger.info(e)
    finally:
        logger.info('database closes')


def update_customer_credit(customer_id, credit):
    """
    This function will search an existing customer by customer_id and update their credit limit or
    raise a ValueError exception if the customer does not exist.

    :param customer_id:
    :param credit:
    :return:
    """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        logger.info(f' Customer with id {customer.customer_id} currently has a credit limit: {customer.credit_limit}')
        customer.credit_limit = credit
        # customer = Customer.update(credit_limit=credit).where(Customer.customer_id == customer_id)
        logger.info('Now we are going to try to update credit limit below')
        # customer.update()
        Customer.update(credit_limit=credit).where(Customer.customer_id == customer_id)
        logger.info(f'And here we can prove by finding current credit limit as {customer.credit_limit }')
        logger.info(f' After Update: {customer.customer_id} now has a credit limit {customer.credit_limit}')

    except Exception as e:
        logger.info('update failed because ....')
        logger.info(f'update failed: {Customer.credit_limit}')
        logger.info(e)
        raise ValueError

    finally:
        logger.info('database closes')


def list_active_customers():
    """
    :return: This function will return an integer with the number of customers whose status is currently active.
    """
    try:
        active_customers = Customer.select().where(Customer.status == 1)
        logger.info(f'here we can finding current active customers {active_customers.status}')
        # logger.info(f'And here we can prove by finding current credit limit as {customer.credit_limit}')
        return active_customers.count()
    except Exception as e:
        logger.info('No active customer ....')
        logger.info(f'update failed: {active_customers.status}')
        logger.info(e)
        raise ValueError


if __name__ == "__main__":
    cc.main()
