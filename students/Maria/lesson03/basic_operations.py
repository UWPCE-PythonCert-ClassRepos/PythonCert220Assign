from customer_model import Customer
import peewee as pw
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_customer(customer_id, **kw):
    """
    :param customer_id:
    :param name:
    :param lastname:
    :param home_address:
    :param phone_number:
    :param email_address:
    :param status: must be True or False
    :param credit_limit: Must be a number, no $
    :return: None
    """
    try:
        cust = Customer.create(customer_id=customer_id,
                               first_name=kw['first_name'],
                               last_name=kw['last_name'],
                               home_address=kw['home_address'],
                               phone_number=kw['phone_number'],
                               email_address=kw['email_address'],
                               status=kw['status'],
                               credit_limit=kw['credit_limit'])
        cust.save()
        logger.info("Customersuccessfully added!")

    except Exception as e:
        logging.info(e)
        raise


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


def _delete_table():
    del_cust = Customer.delete()
    del_cust.execute()
