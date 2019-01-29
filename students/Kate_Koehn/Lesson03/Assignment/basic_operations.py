import customer_model as cm
import logging

def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status, credit_limit):
    try:
        credit_limit = float(credit_limit)
    except ValueError as err:
        logging.error(err)
        raise
    new_customer = cm.Customers.create(customer_id = customer_id,
                                    first_name = name,
                                    last_name = last_name,
                                    home_address = home_address,
                                    phone_number = phone_number,
                                    email_address = email_address,
                                    status = status,
                                    credit_limit = credit_limit)
    new_customer.save()


def search_for_customer(customer_id):
    found_customer = {}
    try:
        customer = cm.Customers.get(cm.Customers.customer_id == customer_id)
        found_customer['first_name'] = customer.first_name
        found_customer['last_name'] = customer.last_name
        found_customer['email_address'] = customer.email_address
        found_customer['phone_number'] = customer.phone_number
        return found_customer
    except cm.DoesNotExist:
        return {}


def delete_customer(customer_id):
    try:
        remove_user = cm.Customers.get(cm.Customers.customer_id == customer_id)
        remove_user.delete_instance()
    except cm.DoesNotExist:
        print("Customer successfully deleted from database.")


def list_active_customers():
    active_customers = 0
    for customer in cm.Customers:
        if customer.status == True:
            active_customers += 1
    return active_customers


def update_customer_credit(customer_id, credit_limit):
    try:
        customer = cm.Customers.get(cm.Customers.customer_id == customer_id)
        customer.credit_limit = credit_limit
    except cm.DoesNotExist:
        raise ValueError
