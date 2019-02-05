"""
    This is to create a basic operations
"""
import logging
import peewee
from customers_model import Customer
#'This is to add customer'
def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    try:
        new_customer = Customer.create(customer_id=customer_id, first_name=first_name, last_name=last_name, home_address=home_address, phone_number=phone_number, email_address=email_address, status=status, credit_limit=credit_limit)
        logger.info("The new Customer is successfully added!")
        new_customer.save()
    except ValueError as e:
        logging.info(e)
        logging.info(f"Could not add {first_name} to db")
    database.close()
#'This is to serach customer'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Working with Customer class to search, find')
logger.info('Find and display by selecting with one Customer name...')
def search_customer(customer_id):
    output_dict = {}
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        logging.info(" A customer search from the database")
        output_dict['first_name'] = acustomer.first_name
        output_dict['last_name'] = acustomer.last_name
        output_dict['email_address'] = acustomer.email_address
        output_dict['phone_number'] = acustomer.phone_number
        acustomer.save()
    except Exception as e:
        logging.info(e)
    return output_dict
    database.close()

#'This is to delete customer '
def delete_customer(customer_id):
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        logging.info(" Make sure that this customer will be deleted from our database")
        acustomer.delete_instance()
        acustomer.save()
    except Exception as e:
        logging.info(e)
    return output_dict
    database.close()
#'This is to update customer '
def update_customer_credit(customer_id, credit_limit):
    acustumer = Customer.get(Customer.customer_id == customer_id)
    acustumer.credit_limit = credit_limit
    acustomer.save()
 #'This is to activate the list of customers'

def list_active_customers():
    list_customers = Customer.select().where(Customer.status == 1)
    return list_customers.count()












