import logging
from customer_model import Customer


def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status, credit_limit):
    """This function will add a new customer to the sqlite3 database."""
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise
    new_customer = Customer.create(
        customer_id=customer_id,
        first_name=name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit
    )

    new_customer.save()


def search_customer(customer_id):
    """This function will return a dictionary object with name, lastname,
    email address and phone number of a customer or an empty dictionary object
    if no customer was found."""
    try:
        aperson = Customer.get(Customer.customer_id == customer_id)
    except IndexError as err:
        logging.error(err)
        aperson = []
    return aperson.__dict__


def delete_customer(customer_id):
    """This function will delete a customer from the sqlite3 database."""
    del_customer = Customer.get(Customer.customer_id == customer_id)
    del_customer.delete_instance()


def update_customer_credit(customer_id, credit_limit):
    """This function will search an existing customer by customer_id and \
    update their credit limit or raise a ValueError exception if the customer \
    does not exist."""
    qry = (Customer
           .update({Customer.credit_limit: credit_limit})
           .where(Customer.customer_id == customer_id))
    try:
        qry.execute()
    except ValueError:
        logging.error('Customer id {} does not exist'.format(customer_id))


def list_active_customers():
    """This function will return an integer with the number of customers whose \
    status is currently active."""
    return len(Customer.select().where(Customer.status is True).execute())
