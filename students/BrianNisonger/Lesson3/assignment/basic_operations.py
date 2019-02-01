from peewee import *
from customer_model import Customer
from customer_model import database


def model_to_dict(model):
    model_dict = {
        'customer_id': model.customer_id,
        'name': model.first_name,
        'last_name': model.last_name,
        'home_address': model.home_address,
        'phone_number': model.phone_number,
        'email_address': model.email_address,
        'status': model.status,
        'credit_limit': model.credit_limit
    }
    return model_dict


def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        raise
    if not database.table_exists('Customer'):
        database.create_tables([Customer])
    new_customer = Customer.create(
        customer_id=customer_id,
        first_name=name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit)
    new_customer.save()


def search_customer(customer_id=None):
    find_customer_model = Customer.get_or_none(
        Customer.customer_id == customer_id)
    if find_customer_model:
        find_customer_dict = model_to_dict(find_customer_model)
    else:
        find_customer_dict = {}
    return find_customer_dict


def delete_customer(customer_id=None):
    delete_customer = Customer.get_or_none(Customer.customer_id == customer_id)
    if delete_customer:
        delete_customer.delete_instance()


def update_customer_credit(customer_id=None, credit_limit=None):
    update_customer = Customer.get_or_none(Customer.customer_id == customer_id)
    if update_customer:
        update_customer.credit_limit = credit_limit
        update_customer.save()
    else:
        raise ValueError


def list_active_customers():
    return Customer.select().where(Customer.status == True).count()