import logging
from customers_model import Customer, TestCustomer
import customers_model as cm


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit):
    """
    :param customer_id:
    :param name:
    :param lastname:
    :param home_address:
    :param phone_number:
    :param email_address:
    :param status:
    :param credit_limit:
    :param stage:
    :return:
    """
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise

    args = {
        'customer_id' : customer_id,
        'first_name' : name,
        'last_name' : lastname,
        'home_address' : home_address,
        'phone_number' : phone_number,
        'email_address' : email_address,
        'status' : status,
        'credit_limit' : credit_limit
    }


    new_customer = Customer.create(**args)
    new_customer.save()


def search_customer(customer_id):
    """
    :param customer_id:
    :param stage:
    :return:
    """
    try:
        results = Customer.get(Customer.customer_id == customer_id)
    except Exception:
        return False

    return results


def delete_customer(customer_id):
    """
    :param customer_id:
    :param stage:
    :return:
    """
    customer = Customer.get(Customer.customer_id == customer_id)
    customer.delete_instance()


def update_customer_credit(customer_id, credit_limit):
    """
    :param customer_id:
    :param credit_limit:
    :param stage:
    :return:
    """

    customer = Customer.get(Customer.customer_id == customer_id)
    update = customer.update(credit_limit=credit_limit)
    update.execute()


def list_active_customers():
    """
    :param stage:
    :return:
    """

    results_dict = Customer.select().where(Customer.status == True).dicts()

    return results_dict
