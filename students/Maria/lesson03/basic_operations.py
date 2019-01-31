from customer_model import Customer
import peewee as pw
import logging
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_customer(customer_id, **kw):
    """
    Add a customer to the database
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
    except KeyError as err:
        logging.error(err)
        # I really wanted to do this:
        # raise KeyError("my custom error that is better")
        # but the tests hated it. not sure why, they were fine with it below
        raise
    except Exception as err:
        logging.error(err)
        raise
    logger.info("Customer with id %s successfully added!", customer_id)


def search_customer(customer_id):
    """
    Return a dictionary object with name, lastname, email address and phone
    number of a customer or an empty dictionary object if no customer was found
    """

    output_dict = {}

    try:
        cust = Customer.get(Customer.customer_id == customer_id)
    except pw.DoesNotExist as err:
        logging.error(err)
    else:
        logging.info("Cust object exists")
        output_dict['first_name'] = cust.first_name
        output_dict['last_name'] = cust.last_name
        output_dict['email_address'] = cust.email_address
        output_dict['phone_number'] = cust.phone_number

    return output_dict


def delete_customer(customer_id):

    try:
        cust = Customer.get(Customer.customer_id == customer_id)
    except pw.DoesNotExist as err:
        logging.error(err)
        raise ValueError(config.etext['not_found'].format(customer_id))
    cust.delete_instance()


def update_customer_credit(customer_id, credit_limit):
    cust = Customer.get(Customer.customer_id == customer_id)
    cust.credit_limit = credit_limit
    cust.save()


def list_active_customers():
    num_custs = Customer.select().where(Customer.status == 1)
    return num_custs.count()


def _delete_table():
    """
    delete the customer table
    private function, want people to really think before using it
    """
    del_cust = Customer.delete()
    del_cust.execute()
