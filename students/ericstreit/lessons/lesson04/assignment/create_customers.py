"""
#Lesson03
#Customer Database Exercise ##
"""

# !/usr/bin/env python3
# import stuff here
from db_model import *
import logging
logging.basicConfig(level=logging.DEBUG)
# global variables here

# define function
def create_customers(first__name, last__name, home__address, phone__number, email__address,
                     account__status, credit__limit):
    """
    Description of function

    :param arg1: The first very important parameter. And a bit about
                 what it means.
    :param arg2: The second very important parameter. And now some
                 description of how this is used
    etc
    """
    try:
        with db.transaction():
            logging.info(f'opening database: {db}')
            customer = Customer.create(
                    first_name = first__name,
                    last_name = last__name,
                    home_address = home__address,
                    phone_number = phone__number,
                    email_address = email__address,
                    status = account__status,
                    credit_limit = credit__limit)
            customer.save()
            logging.info('Database add successful')
    except Exception as e:
        logging.info(f'Hm, we had an error here?')
        logging.info(e)
    finally:
        db.close()


def customer_query(k):
    db.connect()
    r = Customer.select().where(Customer.first_name == k).get()
    print(r)
    db.close()

# for testing
if __name__=="__main__":
    pass
    #customer_query(1)
