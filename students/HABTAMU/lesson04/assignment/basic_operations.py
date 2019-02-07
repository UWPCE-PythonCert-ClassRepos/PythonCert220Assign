

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


import logging
import csv
from customers_model import *
import create_customer as cc
from peewee import SqliteDatabase


# Create a custom logger
logger = logging.getLogger(__name__ + '.basic_operation')
logger.setLevel(logging.DEBUG)

# Create handlers
f_handler = logging.FileHandler('db.log')

# Create formatter and add it to handlers
f_format = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s')
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(f_handler)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(f_format)

logging.info("Defining basic operations for the customer database")

# def read_csv_data():
#     with open('lesson04_assignment_data_customer.csv', newline='') as csvfile:
#         customer_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in spamreader:
#             print(', '.join(row))


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
    # for arg in args:
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
        logger.error(f'Customer not found and see how the database protects our data and look the error, \n {e}')
        logger.error(e)

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
        logger.error('Delete failed because Andrew has Jobs')
        logger.error(f'Delete failed: {Customer.first_name}')
        logger.exception(e)
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
        credit = float(credit)
    except ValueError as err:
        logger.error(err)
        raise

    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        logger.info(f' Current credit limit: for a Customer with id {customer.customer_id} is {customer.credit_limit}')
        # customer = Customer.update(credit_limit=credit).where(Customer.customer_id == customer_id)
        logger.info(f' Now we are going to try to update credit limit below {credit}')
        # customer.update()

        Customer.update(credit_limit=credit).where(Customer.customer_id == customer_id).execute()
        customer.credit_limit = credit
        customer.save()
        logger.info(f' After Update customer with id: {customer.customer_id} now has a credit limit {customer.credit_limit}')
        # customer.save()
    except Exception as e:
        logger.error(f'update failed customer_id does not exist: {Customer}')
        logger.exception(e)
    #
    # customer.credit_limit = credit
    # customer.save()
    logger.info('database closes')


def list_active_customers():
    """
    :return: This function will yield customer_id with the number of customers whose status is currently active.
    """
    try:
        active_customers = Customer.select().where(Customer.status == True)
        for customer in active_customers:
            logger.info(f'here we can finding current active customers {active_customers}')
            yield customer.customer_id
    except Exception as e:
        logger.error('No active customer ....')
        logger.error(f'update failed: {active_customers.status}')
        logger.exception(e)
        raise ValueError


if __name__ == "__main__":
    cc.main()
