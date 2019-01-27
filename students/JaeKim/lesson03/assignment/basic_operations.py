import logging
from customers_model import Customer, Test_Customer
import customers_model as cm


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit,
                 stage='prod'):
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

    if stage == 'prod':
        new_customer = Customer.create(**args)
        new_customer.save()

    if stage == 'dev':
        new_customer = Test_Customer.create(**args)
        new_customer.save()


def search_customer(customer_id, stage='prod'):
    try:
        if stage == 'prod':
            results = Customer.get(cm.customer_id == customer_id)

        if stage == 'dev':
            results = Test_Customer.get(Test_Customer.customer_id == customer_id)
    except Exception:
        return False

    return results


def delete_customer(customer_id, stage='prod'):
    if stage == 'prod':
        customer = Customer.get(cm.customer_id == customer_id)
        customer.delete_instance()

    if stage == 'dev':
        customer = Test_Customer.get(Test_Customer.customer_id == customer_id)
        customer.delete_instance()


def update_customer_credit(customer_id, credit_limit, stage='prod'):
    if stage == 'prod':
        customer = Customer.get(cm.customer_id == customer_id)
        update = customer.update(credit_limit=credit_limit)
        update.execute()

    if stage == 'dev':
        customer = Test_Customer.get(Test_Customer.customer_id == customer_id)
        update = customer.update(credit_limit=credit_limit)
        update.execute()


def list_active_customers(stage='prod'):
    if stage == 'prod':
        results_dict = Customer.select().where(Customer.status == True).dicts()

    if stage == 'dev':
        results_dict = Test_Customer.select().where(Test_Customer.status == True).dicts()

    return results_dict
