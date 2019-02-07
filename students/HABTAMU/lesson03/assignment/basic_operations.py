

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

from customers_model import Customer as cls_Customer
import logging

from peewee import SqliteDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('Customer.db')

CUSTOMER_ID = 0
FIRST_NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
STATUS = 6
CREDIT_LIMIT = 7


# def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
#     """
#     add customer to database
#     :type credit_limit: object
#     customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit
#     """
#
#     customers = [
#         #
#         # ('123', 'Andrew', 'John','123th 32nd NE,SEA, 98101, WA', '123-131-3331','andrew_john@uw.edi', 'True', '3,320.00'),
#         # ('234', 'And', 'Joe', '321th 2nd NE, SEA, 98101, WA', '300-131-3331', 'and@uw.edi', 'True', '2,220.00'),
#         # ('345', 'Joe', 'La', '12th 2nd NE, SEA, 98101, WA', '434-131-3331', 'joe@uw.edi', 'True', '20,220.00')
#         (customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit)
#     ]
#
#     logger.info('Creating customer records: iterate through the list of tuples')
#     logger.info('Prepare to explain any errors with exceptions')
#     logger.info('and the transaction tells the database to rollback on error')
#
#     try:
#         database.connect()
#         database.execute_sql('PRAGMA foreign_keys = ON;')
#         for customer in customers:
#             with database.transaction():
#                 new_customer = cls_Customer.create(
#                     customer_id = customer[CUSTOMER_ID],
#                     first_name = customer[FIRST_NAME],
#                     last_name = customer[LAST_NAME],
#                     home_address = customer[HOME_ADDRESS],
#                     phone_number = customer[PHONE_NUMBER],
#                     email_address = customer[EMAIL_ADDRESS],
#                     status = customer[STATUS],
#                     credit_limit = customer[CREDIT_LIMIT]
#                     )
#                 new_customer.save()
#         logger.info('Database add successful')
#
#         logger.info('Print the Customer records we just added ...')
#         for added_customer in cls_Customer:
#             logger.info(f'customer whose id {added_customer.customer_id} known to be with his first name ' +\
#                         f'{added_customer.first_name} lives in {added_customer.home_address} just added')
#     except Exception as e:
#             logger.info(f'Error creating = {customer[FIRST_NAME]}')
#             logger.info(e)
#             logger.info('see how the database protects our data')
#
#     finally:
#         logger.info('database closes')
#         database.close()


# def search_customer(customer_id):
#     """
#     This function will return a dictionary object with name, lastname,
#     email address and phone number of a customer
#     or an empty dictionary object if no customer was found.
#         :param customer_id:
#         :return: dictionary object with name, lastname, email address and phone number of a customer
#     """
#
#     try:
#         database.connect()
#         database.execute_sql('PRAGMA foreign_keys = ON;')
#
#         a_customer = cls_Customer.get(cls_Customer.customer_id == '234')
#         with database.transaction():
#             for customer in cls_Customer.select().where(cls_Customer.customer_id == '234'):
#                 logger.info(f' Here is the search item returned with dict below \n ' +\
#                             f'\n FIRST_NAME: {a_customer.first_name} ' +\
#                             f'\n LAST_NAME: {a_customer.last_name}, ' +\
#                             f'\n EMAIL_ADDRESS: {a_customer.email_address} ' +\
#                             f'\n PHONE_NUMBER: {a_customer.phone_number}')
#     except Exception as e:
#             logger.info(f'Error finding = {customer[FIRST_NAME]}')
#             logger.info(e)
#             logger.info('see how the database protects our data')
#
#     finally:
#         logger.info('database closes')
#         database.close()
#
# def delete_customer(customer_id):
#     """
#     This function will delete a customer from the sqlite3 database.
#         :param customer_id:
#     """
#
#     try:
#         with database.transaction():
#             a_customer = cls_Customer.get(cls_Customer.customer_id == '123')
#             logger.info(f'Trying to delete as customer with customer id {a_customer.customer_id} and his first name was {a_customer.first_name}')
#             a_customer.delete_instance()
#
#     except Exception as e:
#         logger.info('Delete failed because Andrew has Jobs')
#         logger.info(f'Delete failed: {a_customer.first_name}')
#         logger.info(e)
#     finally:
#         logger.info('database closes')
#         database.close()

#
# def update_customer_credit(customer_id, credit_limit):
#     """
#     This function will search an existing customer by customer_id and update their credit limit or
#     raise a ValueError exception if the customer does not exist.
#
#     :param customer_id:
#     :param credit_limit:
#     :return:
#     """
#     try:
#         database.connect()
#         database.execute_sql('PRAGMA foreign_keys = ON;')
#         # a_customer = cls_Customer.get(cls_Customer.customer_id == '345')
#         a_customer = cls_Customer.get(cls_Customer.customer_id == customer_id)
#         with database.transaction():
#             # for customer in cls_Customer.select().where(cls_Customer.customer_id == '345'):
#             for customer in cls_Customer.select().where(cls_Customer.customer_id == a_customer):
#                 logger.info(f' customer with id {customer.customer_id} have a credit limit: {customer.credit_limit}')
#                 # if customer.customer_id == '345':
#                 logger.info('Update the credit limit here')
#                 customer.credit_limit = credit_limit
#                 customer.save()
#                 # else:
#                 #     logger.info(f'Not giving a credit limit to {customer.customer_id}')
#
#             logger.info(f'And here is where we prove it by finding current credit limit as {a_customer.credit_limit }')
#             # a_customer = cls_Customer.get(a_customer.customer_id == '345')
#             logger.info(f'{customer.customer_id} now has a credit limit  of {customer.credit_limit}')
#
#     except Exception as e:
#         logger.info('update failed because ....')
#         logger.info(f'update failed: {a_customer.credit_limit}')
#         logger.info(e)
#     finally:
#         logger.info('database closes')
#         database.close()

def list_active_customers():
    """
    :return: This function will return an integer with the number of customers whose status is currently active.
    """
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            for customer in cls_Customer.select().where(cls_Customer.status == 1):
                logger.info(f'customers whose first name is {customer.first_name} current status is active')
    except Exception as e:
        logger.info('there could be no active ')
        logger.info(e)
    finally:
        logger.info('database closes')
        database.close()



if __name__ == '__main__':
    # add_customer('567', 'Simon', 'Derike', '3rd 2nd NE,SEA, 98111, WA', '765-131-3331', 'Simon@uw.edi', False, 5320.00)
    # search_customer(234)
    # delete_customer(123)
    # update_customer_credit(345, 7213.00)
    list_active_customers()
