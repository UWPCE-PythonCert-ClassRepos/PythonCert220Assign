"""
    This is to create a basic operations
"""
import peewee as pw
import logging
from customers_model import database, Customer

def model_dictionary(model):
    model_d = {'id': model.id, 'first_name': model.first_name, 'last_name': model.last_name,
    'home_address': model.home_address, 'phone_number': model.phone_number, 'email_address': model.email_address,
    'status': model.status, 'credit_limit': model.credit_limit}
    return model_d

#'This is to add customer'

def add_customer(id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    try:
        credit_limit = float(credit_limit)
        logger.info("The new Customer is successfully added!")
    except ValueError as err:
        logging.error(err)
        raise
    if not database.table_exists('Customer'):
        database.create_tables([Customer])
    new_customer = Customer.create(id=id, first_name=first_name, last_name=last_name,
    home_address=home_address, phone_number=phone_number, email_address=email_address, status=status,
        credit_limit=credit_limit)
    new_customer.save()
    logging.info(f"Added {first_name} to database")
    database.close()
#'This is to serach customer'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Working with Customer class to search, find')
logger.info('Find and display by selecting with one Customer first_name...')
def search_customer(id=None):
    try:
        find_customer_model = Customer.get(Customer.id == id)
    except pw.DoesNotExist as err:
        logging.error(err)
        find_customer_dict = {}
    else:
        find_customer_dict = model_dictionary(find_customer_model)

    return find_customer_dict

#'This is to delete customer '
def delete_customer(id=None):
    delete_customer = Customer.get(Customer.id == id)
    logging.info(" Make sure that this customer will be deleted from our database")
    if delete_customer:
        delete_customer.delete_instance()
        delete_customer.save()
    else:
        logging.error(f"We could not delete {first_name} from the database")
        raise ValueError("Customer not found")

#'This is to update customer '
def update_customer_credit(id, credit_limit):
    update_custumer = Customer.get(Customer.id == id)
    if update_customer:
        update_customer.credit_limit = credit_limit
        update_customer.save()
    else:
        raise ValueError
        logging.info(error)
        logging.info(f"We could not update {first_name} from the database")
        database.close()

#'This is to activate the list of customers'

def list_active_customers():
    #import pdb;pdb.set_trace()
    list_customers = Customer.select().where(Customer.status == True)
    return list_customers.count()




