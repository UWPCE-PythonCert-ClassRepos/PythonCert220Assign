""" Basic Operations"""
import logging
import csv
import peewee as pw
from customers_model import Customer
import create_customer as cc


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)

LOGGER.info("Basic operations defined for the customer database.")


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
    try:
        with Customer.DATABASE.transaction():
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
    except pw.IntegrityError:
        LOGGER.error("Customer id %s, already exitsts in database. Error adding %s %S",
                    customer_id, first_name, last_name)
    raise pw.IntegrityError

def upload_csv(filename):
    """
        Adds data for customer from csv file
    """
    with open(filename, newline="", encoding="ISO-8859-1") as csvfile:
        all_customers = csv.reader(csvfile)
        header = next(all_customer, None) 

        with Customer.DATABASE.atomic(): # Populates the databse with info
            Customer.insert_many(all_customers, headers).execute


def search_customer(customer_id):
    """
        Search for customer name in database
        :return: Customer info if Ture, empty dict if None
        :param customer_id: customer_id to search for
    """
    find_customer_dict = {}
    LOGGER.info("Search for customer name in database...")
    try:
        find_customer = Customer.get(Customer.customer_id == customer_id)
        if find_customer:

            find_customer_dict = {"first_name": find_customer.first_name,
                                  "last_name": find_customer.last_name,
                                  "email_address": find_customer.email_address,
                                  "phone_number": find_customer.phone_number}

        LOGGER.info('%s %s is in the database. There phone # is %s',
                    find_customer.first_name, find_customer.last_name,
                    find_customer.phone_number)

    except pw.DoesNotExist:
        LOGGER.info('No customer with customer id of %s', Customer.customer_id)
        return find_customer_dict


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
        LOGGER.info("Customer has been deleted")

    except pw.DoesNotExist:
        return None
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
        customer.save()
    except pw.DoesNotExist:
        LOGGER.error("Customer_id of %s does not exist", customer_id)


def list_active_customers():
    """
        Returns an integer with the number of customers whose status is currently active.
    """

    customer_count = Customer.select().where(Customer.status == True).count()
    LOGGER.info('%s customers are currently active', customer_count)

    return customer_count

def return_all_customer_info():
    """
        Prints all customer info
    """
    all_customer_records = Customer.select()



    for persion in all_customer_records:
        print(f"Customer id: {person.customer_id}\nFirst Name: {person.first_name}\nLast Name: {person.last_name}\n"
              f"Home Address: {person.home_address}\nPhone Number: {person.phone_number}\n"
              f"Email Address: {person.email_address}\nStatus: {person.status}\nCredit Limit: ${person.credit_limit}\n")


    if __name__ == "__main__":
        cc.main()

        search_customer("W3434fd")
        list_active_customers()
