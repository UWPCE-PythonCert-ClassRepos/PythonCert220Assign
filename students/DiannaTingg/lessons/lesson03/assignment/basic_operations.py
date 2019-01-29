"""
Basic operations for the customer database.
"""

import logging
import peewee as pw
import create_customers as cc
import customer_model as cm

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

logging.info("Defining basic operations for the customer database.")


# pylint: disable-msg=too-many-arguments
def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address,
                 active_status, credit_limit):
    """
    Adds a new customer to the database.
    """
    try:
        new_customer = cm.Customer.create(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            active_status=active_status,
            credit_limit=credit_limit)
        new_customer.save()
        logging.info('Successfully added %s %s to the database.', first_name, last_name)
    except pw.IntegrityError as add_error:
        logging.error("%s. Error adding %s %s to the database.", add_error, first_name, last_name)
        raise pw.IntegrityError


def search_customer(customer_id):
    """
    Returns a dictionary with customer's first name, last name, email address, and phone number.
    If no customer is found, returns an empty dictionary.
    """
    try:
        current_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)

        customer_dict = {"first_name": current_customer.first_name,
                         "last_name": current_customer.last_name,
                         "email_address": current_customer.email_address,
                         "phone_number": current_customer.phone_number}
        logging.info("Found customer %s: %s %s.", customer_id,
                     current_customer.first_name, current_customer.last_name)

        return customer_dict
    except pw.DoesNotExist:
        logging.error("Search Error: That customer id is not in the database.")
        return dict()


def delete_customer(customer_id):
    """
    Delete a customer from the database.
    """
    try:
        former_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
        logging.info("Deleting customer %s: %s %s.", customer_id,
                     former_customer.first_name, former_customer.last_name)
        former_customer.delete_instance()
    except pw.DoesNotExist:
        logging.error("Delete Error: That customer id is not in the database.")


def update_customer_credit(customer_id, new_credit_limit):
    """
    Search for an existing customer by id and update their credit limit.
    """
    try:
        update_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
        update_customer.credit_limit = new_credit_limit
        update_customer.save()
        logging.info("Customer %s %s now has a credit limit of %s.",
                     update_customer.first_name, update_customer.last_name, new_credit_limit)

    except pw.DoesNotExist:
        logging.error("Update Credit Error: That customer id is not in the database.")
        raise pw.DoesNotExist


def list_active_customers():
    """
    Returns an integer with the number of customers whose status is currently active.
    """
    total_active = (cm.Customer.select().where(cm.Customer.active_status).count())

    logging.info("There are %s active customers in the database.", total_active)

    return total_active


if __name__ == "__main__":
    cc.main()
