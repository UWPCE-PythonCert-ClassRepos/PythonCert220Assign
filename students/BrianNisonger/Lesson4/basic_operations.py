from peewee import *
from customer_model import Customer
from customer_model import database


def add_customer(**kwargs):
    try:
        kwargs['credit_limit'] = float(kwargs['credit_limit'])
    except ValueError as err:
        raise
    if not database.table_exists('Customer'):
        database.create_tables([Customer])
    new_customer = Customer.insert(kwargs)
    new_customer.execute()


def search_customer(customer_id=None):
    search_customer = Customer.select().where(
        Customer.customer_id == customer_id).dicts()
    field_names = Customer._meta.sorted_field_names
    if search_customer:
        return {
            field_name: record[field_name]
            for record in search_customer for field_name in field_names
        }
    else:
        return {}


def delete_customer(customer_id=None):
    delete_customer = Customer.get_or_none(Customer.customer_id == customer_id)
    if delete_customer:
        delete_customer.delete_instance()


def update_customer(**kwargs):
    update_customer = Customer.get_or_none(
        Customer.customer_id == kwargs['customer_id'])
    if update_customer:
        insert_dict = {
            kwarg: kwargs[kwarg]
            for kwarg in kwargs if kwarg != 'customer_id'
        }
        update_query = Customer.update(insert_dict).where(
            Customer.customer_id == kwargs['customer_id'])
        update_query.execute()
    else:
        raise ValueError


def list_active_customers():
    return Customer.select().where(Customer.status == True).count()
