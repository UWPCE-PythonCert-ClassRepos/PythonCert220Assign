"""
Basic operations for the customer database.
"""

import logging
import csv
import peewee as pw
import customer_model as cm
import create_customers as cc

# pylint: disable-msg=line-too-long
# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=no-value-for-parameter

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)

LOGGER.info("Defining basic operations for the customer database.")


def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    """
    Adds a new customer to the database.
    """
    try:
        with cm.DATABASE.transaction():
            new_customer = cm.Customer.create(
                customer_id=customer_id,
                first_name=first_name,
                last_name=last_name,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info("Successfully added Customer %s: %s %s to the database.", customer_id, first_name, last_name)
    except pw.IntegrityError:
        LOGGER.error("Error adding %s %s. Customer id %s already exists in the database.",
                     first_name, last_name, customer_id)
        raise pw.IntegrityError


def upload_csv(filename):
    """
    Adds customer data from a csv file.
    """
    with open(filename, newline="") as csvfile:
        all_customers = csv.reader(csvfile)
        headers = next(all_customers, None)  # Skip the header row

        with cm.DATABASE.atomic():
            cm.Customer.insert_many(all_customers, headers).execute()


def search_customer(customer_id):
    """
    Returns a dictionary with customer's first name, last name, email address, and phone number.
    If no customer is found, returns an empty dictionary.
    """
    try:
        current_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)

        customer_keys = ["first_name", "last_name", "email_address", "phone_number"]

        customer_values = [current_customer.first_name, current_customer.last_name,
                           current_customer.email_address, current_customer.phone_number]

        customer_dict = dict(zip(customer_keys, customer_values))

        LOGGER.info("Found customer %s: %s %s.", customer_id, current_customer.first_name, current_customer.last_name)

        return customer_dict

    except pw.DoesNotExist:
        LOGGER.error("Search Error: Customer id %s is not in the database.", customer_id)
        return dict()


def delete_customer(customer_id):
    """
    Delete a customer from the database.
    """
    try:
        former_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
        LOGGER.info("Deleting customer %s: %s %s.", customer_id, former_customer.first_name, former_customer.last_name)
        former_customer.delete_instance()
    except pw.DoesNotExist:
        LOGGER.error("Delete Error: Customer id %s is not in the database.", customer_id)
        raise pw.DoesNotExist


def update_customer_credit(customer_id, new_credit_limit):
    """
    Search for an existing customer by id and update their credit limit.
    """
    try:
        update_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
        update_customer.credit_limit = new_credit_limit
        update_customer.save()
        LOGGER.info("Customer %s: %s %s now has a credit limit of %s.", customer_id,
                    update_customer.first_name, update_customer.last_name, new_credit_limit)

    except pw.DoesNotExist:
        LOGGER.error("Update Credit Error: Customer id %s is not in the database.", customer_id)
        raise pw.DoesNotExist


def list_active_customers():
    """
    Returns an integer with the number of customers whose status is currently active.
    """
    total_active = (cm.Customer.select().where(cm.Customer.status == "Active").count())

    LOGGER.info("There are %s active customers in the database.", total_active)

    return total_active


def print_customers():
    """
    Prints all customer info from the database.
    :return:
    """
    all_records = cm.Customer.select()

    for person in all_records:
        print(f"Customer id: {person.customer_id}\nFirst Name: {person.first_name}\nLast Name: {person.last_name}\n"
              f"Home Address: {person.home_address}\nPhone Number: {person.phone_number}\n"
              f"Email Address: {person.email_address}\nStatus: {person.status}\nCredit Limit: ${person.credit_limit}\n")


if __name__ == "__main__":
    cc.main()
