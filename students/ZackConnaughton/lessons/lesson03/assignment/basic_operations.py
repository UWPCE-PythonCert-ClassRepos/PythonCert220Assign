"""
basic operations for customer database manipulation
"""

import logging
from customer_model import Customer, create_database
from peewee import SqliteDatabase

DATABASE = SqliteDatabase

def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status, credit_limit):
    new_customer = Customer.create(
        customer_id=customer_id,
        name=name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit
        )
    new_customer.save()


def search_customer(customer_id):
    found_customer_dict = {}
    try:
        found_customer = Customer.get(Customer.customer_id == customer_id)
        if found_customer:
            found_customer_dict = {'name': found_customer.name, 'lastname': found_customer.last_name, 'email address': found_customer.email_address, 'phone number': found_customer.phone_number}
    except Exception as e:
        print(e)
        pass
    return found_customer_dict

def delete_customer(id):
    customer_to_delete = Customer.get(Customer.customer_id == id)
    customer_to_delete.delete_instance()
    return None  #I know not necessary, but I like to know my function is closed and I am returning nothing on purpose

def update_customer_credit(id, credit):
    try:
        Customer.get(Customer.customer_id == id)
        credit_update = Customer.update(credit_limit=credit).where(Customer.customer_id == id)
        x = credit_update.execute()
    except Exception as e:
        raise ValueError

def list_active_customers():
    customer_count = Customer.select().count()
    return customer_count
