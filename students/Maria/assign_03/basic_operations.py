import logging
from customers_model import Customer


def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status, credit_limit):
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise
    new_customer = Customer.create(
        customer_id = customer_id,
        first_name = name,
        last_name = last_name,
        home_address = home_address,
        phone_number = phone_number,
        email_address = email_address,
        status = status,
        credit_limit = credit_limit)
    new_customer.save()
