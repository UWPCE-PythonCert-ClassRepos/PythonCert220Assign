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


def sanitize_csv_headers(df):
    """function to take in headers in any format and make them uniform"""
    mapper = {key: value for key, value in zip(df.columns, ['customer_id',
                                                            'first_name',
                                                            'last_name',
                                                            'home_address',
                                                            'phone_number',
                                                            'email_address',
                                                            'status',
                                                            'credit_limit'])}
    new_df = df.rename(index=str, columns=mapper)
    return new_df

def batch_add_customer(csv):
    """
    Function to add multiple customers to db using a csv
    :param csv: headers must be in this order: customer_id, first_name, last_name, home_address,
                                                phone_number, email_address, status, credit_limit
    """
    df = pandas.read_csv(csv, sep=',', encoding='ISO-8859-1', error_bad_lines=False)
    df = sanitize_csv_headers(df)
    df['phone_number'] = df['phone_number'].apply(fix_crappy_phone_number_formatting)
    new_dict = df.to_dict("records")
    for customer in new_dict:
        add_customer(**customer)
        return True


def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    """function to add single customer to database"""
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise
    new_customer = cm.Customers.create(customer_id = customer_id,
                                    first_name = first_name,
                                    last_name = last_name,
                                    home_address = home_address,
                                    phone_number = phone_number,
                                    email_address = email_address,
                                    status = status,
                                    credit_limit = credit_limit)
    new_customer.save()



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
        if customer.status == "Active":
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
