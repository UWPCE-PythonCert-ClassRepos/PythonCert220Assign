"""
#Lesson03
#Customer Database Exercise ##
"""

#!/usr/bin/env python3
#import stuff here
from create_db import *
from db_model import *
import logging
#global variables here
logging.basicConfig(level=logging.DEBUG)
#define function

def add_customer(first__name, last__name, home__address, phone__number,
                 email__address, account__status, credit__limit):
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



def search_customer(n):
    """
    Function to return a dict of customer from the db using the customer ID

    :param arg1: the customer ID
    """
    query_dict = {}
    try:
        query = Customer.select().where(Customer.id == n).get()
        # update dict with customer db values
        query_dict[query.id] = (query.first_name, query.last_name, query.email_address,
                                query.phone_number, query.credit_limit)
    except Exception as err:
        logging.error(f'Unable to search for Customer ID: {n} this customer does not exist')
        #logging.error(f'{err}')
    finally:
        # will return dicionary object of query or empty object if query is not matched
        return query_dict
        db.close()



def delete_customer(n):
    """
    Function to remove a customer from the db using the customer ID

    :param arg1: the customer ID
    """
    try:
        query = Customer.get(Customer.id == n)
        logging.info(f'OK, we will delete {query.first_name} from the db')
        query.delete_instance()
    except Exception as err:
        logging.error(f'Customer ID: {n} does not exist')
        #logging.error(f'{err}')
    finally:
        db.close()


def update_customer_credit(n, amount):
    """
    Function to remove a customer from the db using the customer ID

    :param arg1: the customer ID
    """
    try:
        query = Customer.update(credit_limit = amount).where(Customer.id == n)
        logging.info(f'OK, we will update {Customer.first_name} credit limit to ${amount}')
        query.execute()
    except Exception as err:
        logging.error(f'Customer ID: {n} does not exist')
        logging.error(f'{err}')
    finally:
        db.close()


def list_active_customers():
        """
        Function to return the total number of active customers from the db
        """
        try:
            query = Customer.select().where(Customer.status == True)
            return len(query)
        except Exception as err:
            logging.error(f'{err}')
        finally:
            db.close()

#for testing
if __name__=="__main__":
    # create_db()
    # db_model()
    # create_customer()
    add_customer('Tom', 'Natsworthy', '1234 London Traction', '1234567890', 'tom.natsworthy@londontown.com', True, 100.00)
    add_customer('Hester', 'Shaw', '1234 Anchorage Traction', '0987654321', 'hester.shaw@londontown.com', True, 999.00)
    add_customer('Anna', 'Fang', 'Jenny Hanniver Airship', '0987654321', 'anna.fang@jenny.com', True, 2582.00)
    print(search_customer(1))
    print(search_customer(2))
    print(search_customer(3))
    delete_customer(2)
    update_customer_credit(1, 14.23)
    print(search_customer(1))
    print(list_active_customers())
