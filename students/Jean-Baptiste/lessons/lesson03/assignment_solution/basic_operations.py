"""
    This is to create a basic operations
"""
import logging
from customers_model import Customer
'This is to add customer'
def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status, credit_limit):
	    try:
	        credit_limit = float(credit_limit)
	    except ValueError as err:
	        logging.error(err)
	        raise
	    new_customer = Customer.create(
	        customer_id = customer_id,
	        first_name = name,
	        last_name = last_name,
	        home_address = home_address,
	        phone_number = phone_number,
	        email_address = email_address,
	        status = status,
	        credit_limit = credit_limit)
            new_customer.save()
            logger.info('Database add successful')
'This is to serach customer'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Working with Customer class to search, find')
logger.info('Find and display by selecting with one Customer name...')

acustomer = Customer.get(Customer.customer_name == 'John')
logger.info(f'{acustomer.first_name} and {acustomer.last_name}, the customer address id is {acustomer.customer_id}, the customer  ' + \
    f' and home address is {acustomer.home_address} and phone number is {acustomer.phone_number}, email is {acustomer.email_address}) + \ 
    f' status is {acustomer.status} with credit limit is {acustomer.credit_limit}, email is {acustomer)
logger.info('Our customer class inherits select(). Specify search with .where()')

database.close()

'This is to delete customer '

def delete_customer(first_name):
            if first_name == 'John':
	    delete_customer.delete()
logger.info('Reading and print all Customer records (but not John; he has been deleted)...')

for customer in Customer:
    logger.info(f'{customer.customer_name} ')

database.close()








	
	
	
