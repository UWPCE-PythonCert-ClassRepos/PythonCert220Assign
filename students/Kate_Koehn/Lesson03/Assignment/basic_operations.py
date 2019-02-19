import customer_model as cm
import logging
import pandas
import peewee
import re



def fix_crappy_phone_number_formatting(phone_number):
    """Function to clean up poorly formatted phone numbers before adding them to the database"""
    m = re.match(r'(\d)?.?(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$', phone_number)
    if m:
        fixed_number = f'+{m.group(1) or "1"}({m.group(2)}){m.group(3)}-{m.group(4)} {"x"+m.group(5) if m.group(5) else ""}'
        return fixed_number


#currently working on getting insert_many to work.
def batch_add_customer(csv):
    df = pandas.read_csv("customer.csv", sep=',', encoding='ISO-8859-1', error_bad_lines=False)
    df['Phone_number'] = df['Phone_number'].apply(fix_crappy_phone_number_formatting)
    add_customers = cm.Customers.insert_many(df, fields=[cm.Customers.customer_id, cm.Customers.first_name,
                                                         cm.Customers.last_name, cm.Customers.home_address,
                                                         cm.Customers.phone_number, cm.Customers.email_address,
                                                         cm.Customers.status, cm.Customers.credit_limit])
    print(df)
    add_customers.execute()



# old code for adding in single customer at a time
# def add_customer():
#     for customer in customers:
#         try:
#             credit_limit = float(credit_limit)
#         except ValueError as err:
#             logging.error(err)
#             raise
#         cm.Customers.create(customer_id = customer_id,
#                             first_name = name,
#                             last_name = last_name,
#                             home_address = home_address,
#                             phone_number = phone_number,
#                             email_address = email_address,
#                             status = status,
#                             credit_limit = credit_limit)
#         customer.save()



def search_for_customer(customer_id):
    """Function to look up a customer record in the database"""
    found_customer = {}
    try:
        customer = cm.Customers.get(cm.Customers.customer_id == customer_id)
        found_customer['first_name'] = customer.first_name
        found_customer['last_name'] = customer.last_name
        found_customer['email_address'] = customer.email_address
        found_customer['phone_number'] = customer.phone_number
    except cm.DoesNotExist as err:
        logging.error(err)
        logging.info("Customer does not exist in the database.")
    return found_customer


def delete_customer(customer_id):
    """Function to delete a customer record from the database"""
    try:
        remove_user = cm.Customers.get(cm.Customers.customer_id == customer_id)
        remove_user.delete_instance()
    except cm.DoesNotExist:
        logging.info("Customer successfully deleted from database.")


def list_active_customers():
    """Function to list active users in database. Status of True = active."""
    active_customers = 0
    for customer in cm.Customers:
        if customer.status == "Active  ":
            active_customers += 1
    return active_customers


def update_customer_credit(customer_id, credit_limit):
    """Function to update a customer credit record in the database"""
    try:
        customer = cm.Customers.get(cm.Customers.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
    except cm.DoesNotExist:
        raise ValueError
