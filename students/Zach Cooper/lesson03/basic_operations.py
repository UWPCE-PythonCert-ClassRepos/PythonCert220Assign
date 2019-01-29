""" Basic Operations"""
import logging
import peewee as pw
from customers_model import Customer


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    """
        Returns new customer with **kwargs info
    """
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise
    new_customer = Customer.create(
        customer_id=customer_id,
        first_name=first_name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit)
    new_customer.save()

    LOGGER.info('Customer database add successful')
    LOGGER.info('%s %s has been created', Customer.first_name,
                Customer.last_name)


def search_customer(customer_id):
    """
        Search for customer name in database
        :return: Customer info if Ture, empty dict if None
        :param customer_id: customer_id to search for
    """

    LOGGER.info("Search for customer name in database...")
    try:
        find_customer = Customer.get(Customer.customer_id == customer_id)

        customer_dict = {"first_name": find_customer.first_name,
                         "last_name": find_customer.last_name,
                         "email_address": find_customer.email_address,
                         "phone_number": find_customer.phone_number}

        LOGGER.info('%s %s is in the database. There phone # is %s',
                    find_customer.first_name, find_customer.last_name,
                    find_customer.phone_number)
        return customer_dict
    except pw.DoesNotExist:
        LOGGER.info('No customer with customer id of %s', Customer.customer_id)
        return {}


def delete_customer(customer_id):
    """
        Deletes customer from database
        :return: empty dict if custome doesnt exist
        :param customer_id: customer_id to search and delete for
    """
    LOGGER.info("Creating new customer named Tom and then deleting him")
    try:
        customer_remove = Customer.get(Customer.customer_id == customer_id)
        customer_remove.delete_instance()

    except pw.DoesNotExist:
        return {}
    LOGGER.info("Customer successfully deleted in database")


def update_customer_credit(customer_id, credit_limit):
    """
        Updates the customer credit limit
        :param cusomer_id: credit_limit to update new limit
    """

    LOGGER.info("Updating customer credit limit")
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
    except pw.DoesNotExist:
        LOGGER.error("Customer_id of %s does not exist", customer_id)

    customer.save()


def list_active_customers():
    """
        Returns an integer with the number of customers whose status is currently active.
    """

    customer_count = Customer.select().where(Customer.status == True).count()
    LOGGER.info('%s customers are currently active', customer_count)
    return customer_count
