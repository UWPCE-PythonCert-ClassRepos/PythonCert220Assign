"""
basic operations for customer database manipulation
"""

import logging
from peewee import SqliteDatabase
from customer_model import Customer

DATABASE = SqliteDatabase

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
file_handler = logging.FileHandler('db.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(log_format))

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status, credit_limit):
    logging.debug('Adding customer')
    new_customer = Customer.create(
        customer_id=customer_id,
        name=name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit
        )
    new_customer.save()
    logging.info('Added customer %s to database', customer_id)


class customer_data:
    def __init__(self, file):
        logging.debug('Creating customer_data class instance with %s', file)
        try:
            self.csvfile = open(file)
            self.csvfile.readline()
        except FileNotFoundError:
            logging.critical('Could not find file %s', file)
            raise FileNotFoundError

    def __iter__(self):
        return self

    def __next__(self):
        customer_info = self.csvfile.readline()
        if customer_info:
            output = customer_info.rstrip().split(',')
            return output
        raise StopIteration

def batch_add_customers(file):
    customer_info = customer_data(file)
    for customer in customer_info:
        add_customer(*customer)
    return True


def search_customer(customer_id):
    logging.debug('Searching for customer %s', customer_id)
    found_customer_dict = {}
    try:
        found_customer = Customer.get(Customer.customer_id == customer_id)
        if found_customer:
            found_customer_dict = {'name': found_customer.name, 'lastname': found_customer.last_name, 'email address': found_customer.email_address, 'phone number': found_customer.phone_number}
    except Exception as e:
        print(e)
        pass
    return found_customer_dict

def delete_customer(id):
    logging.debug('deleting customer %s', id)
    customer_to_delete = Customer.get(Customer.customer_id == id)
    customer_to_delete.delete_instance()
    logging.info('Deleted customer %s', id)
    return None  #I know not necessary, but I like to know my function is closed and I am returning nothing on purpose

def update_customer_credit(id, credit):
    logging.debug('Updating credit for customer %s', id)
    try:
        Customer.get(Customer.customer_id == id)
        credit_update = Customer.update(credit_limit=credit).where(Customer.customer_id == id)
        x = credit_update.execute()
        logging.info('Updated customer %s credit to %f', id, credit)
    except Exception as e:
        raise ValueError

def list_active_customers():
    customer_count = Customer.select().count()
    return customer_count
