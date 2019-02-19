"""
operations
"""
import logging
from customer_model import Customer
from peewee import fn

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

def search_customer(customer_id):
    try:
        newn_customer = Customer.get(Customer.customer_id == customer_id)
        cstm_dict = {'name': newn_customer.name,
                     'last_name': newn_customer.last_name,
                     'email_address': newn_customer.email_address,
                     'phone_number': newn_customer.phone_number}
    except Exception as e:
        cstm_dict = {}
        return cstm_dict

    return cstm_dict

def delete_customer(customer_id):
    try:
        person = Customer.get(Customer.customer_id == customer_id)
        person.delete_instance()
    except Exception as e:
        print('Customer wasn\'t found.')
    return 'customer deleted'

def update_customer_credit(customer_id, credit_limit):
    try:
        u = Customer.update(credit_limit=credit_limit).where(Customer.customer_id == customer_id)
        u.execute()
    except ValueError:
        print('Customer wasn\'t found.')

def list_active_customers():
    count = Customer.select().where(Customer.status == True).count()
    logging.info(f'{count} customers are currently active')
    return count
