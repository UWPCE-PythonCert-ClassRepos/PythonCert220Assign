from customer_model import Customer
import peewee as pw
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    try:
        cust = Customer.create(customer_id=customer_id,
                               first_name=first_name,
                               last_name=last_name,
                               home_address=home_address,
                               phone_number=phone_number,
                               email_address=email_address,
                               status=status,
                               credit_limit=credit_limit)
        cust.save()
        logger.info("Customersuccessfully added!")

    except Exception as e:
        logging.info(f"Could not add {first_name} to db")
        logging.info(e)


def search_customer(customer_id):
    """
    Return a dictionary object with name, lastname, email address and phone
    number of a customer or an empty dictionary object if no customer was found
    """

    output_dict = {}

    try:
        cust = Customer.get(Customer.customer_id == customer_id)
        logging.info("Cust object exists")
        output_dict['first_name'] = cust.first_name
        output_dict['last_name'] = cust.last_name
        output_dict['email_address'] = cust.email_address
        output_dict['phone_number'] = cust.phone_number
    except Exception as e:
        logging.info(e)

    return output_dict


def delete_customer(customer_id):
    cust = Customer.get(Customer.customer_id == customer_id)
    cust.delete_instance()


def update_customer_credit(customer_id, credit_limit):
    cust = Customer.get(Customer.customer_id == customer_id)
    cust.credit_limit = credit_limit
    cust.save()


def list_active_customers():
    num_custs = Customer.select().where(Customer.status == 1)
    return num_custs.count()
