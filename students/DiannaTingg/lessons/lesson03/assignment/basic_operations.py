"""
Basic operations for the customer database.
"""

import logging
import customer_model as cm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.info("Defining basic operations for the customer database.")


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
        logger.info(f'Successfully added {first_name} {last_name} to the database.')
    except Exception as add_error:
        logger.error(f"{add_error}: Error adding {first_name} {last_name} to the database.")


def search_customer(customer_id):
    """
    Returns a dictionary object with customer's first name, last name, email address, and phone number.
    If no customer is found, returns an empty dictionary.
    """
    try:
        current_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)

        customer_dict = {"first_name": current_customer.first_name,
                         "last_name": current_customer.last_name,
                         "email_address": current_customer.email_address,
                         "phone_number": current_customer.phone_number}
        logging.info(f"Found customer {customer_id}: {current_customer.first_name} {current_customer.last_name}")
        return customer_dict
    except Exception:
        logging.error("Search Error: That customer id is not in the database.")
        return dict()


def delete_customer(customer_id):
    """
    Delete a customer from the database.
    """
    try:
        former_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
        logging.info(f"Deleting customer {customer_id}: {former_customer.first_name} {former_customer.last_name}.")
        former_customer.delete_instance()
    except Exception:
        logging.error("Delete Error: That customer id is not in the database.")


def update_customer_credit(customer_id, new_credit_limit):
    """
    Search for an existing customer by id and update their credit limit.
    """
    try:
        update_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
        update_customer.credit_limit = new_credit_limit
        logging.info(f"Customer {update_customer.first_name} {update_customer.last_name} "
                     f"now has a credit limit of {new_credit_limit}.")

    except Exception:
        logging.error("Update Credit Error: That customer id is not in the database.")


def list_active_customers():
    """
    Returns an integer with the number of customers whose status is currently active.
    """
    total_active = (cm.Customer.select().where(cm.Customer.active_status == True).count())

    logger.info(f"There are {total_active} active customers in the database.")

    return total_active
