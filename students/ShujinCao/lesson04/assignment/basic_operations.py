"""
operations
"""
import logging
from customer_model import Customer
from peewee import fn
import itertools

def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise

    new_customer = Customer.create(
        customer_id=customer_id,
        name=name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit)

    new_customer.save()
    logging.info("New customer has been added")

def search_customer(customer_id):
    try:
        newn_customer = Customer.get(Customer.customer_id == customer_id)
        cstm_dict = {'name': newn_customer.name,
                     'last_name': newn_customer.last_name,
                     'email_address': newn_customer.email_address,
                     'phone_number': newn_customer.phone_number,
                     'status': newn_customer.status}
        logging.info("Customer found")
    except Exception as e:
        cstm_dict = {}
        logging.info("Customer not found")

    return cstm_dict

def delete_customer(customer_id):
    try:
        person = Customer.get(Customer.customer_id == customer_id)
        person.delete_instance()
        logging.info('Customer has been deleted')
    except Exception as e:
        logging.info('Customer wasn\'t found.')
    return 'customer deleted'

def update_customer_credit(customer_id, credit_limit):
    try:
        u = Customer.update(credit_limit=credit_limit).where(Customer.customer_id == customer_id)
        u.execute()
        logging.info('Customer credit limit has been updated')
    except ValueError:
        logging.info('Customer wasn\'t found.')

def list_active_customers():
    count = sum(1 for c in Customer.select().where(Customer.status == 'Active'))
    logging.info(f'{count} customers are currently active')
    return count

if __name__ == "__main__":

    search_customer('C000000')
    list_active_customers()
